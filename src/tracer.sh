#!/bin/bash

set -o pipefail

writeratio=(0.3 0.7)
m=(5 20)
keymax=4000000
select=(random zipf)
seed=1

ttl=(0.3 30)
tp=(10000 1000000)

for writes in "${writeratio[@]}"; do
    for n in "${m[@]}"; do
        for s in "${select[@]}"; do
            naccess=$((keymax * n))
            trace="trace_${s}_w${writes}_n${n}"
            echo "$trace  naccess=$naccess  seed=$seed"
            python3 generator.py $keymax $s $writes $naccess $seed > "$trace"

            for through in "${tp[@]}"; do
                for time in "${ttl[@]}"; do
                    res=$(python3 benchmark.py "$trace" ttl $through $time | python3 counter.py)
                    echo "$s $writes $n ttl $through $time $res" >> results.txt
                done
                res=$(python3 benchmark.py "$trace" pushevict $through 0 | python3 counter.py)
                echo "$s $writes $n pushevict $through 0 $res" >> results.txt
            done

            rm "$trace"
        done
    done
done
