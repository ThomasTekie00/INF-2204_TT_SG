#!/bin/bash

set -euo pipefail

writeratio=(0.3 0.7)
m=(5 20)
keymax=4000000
select=(random zipf)
seed=1

ttl=(0.3 30)
tp=(10000 1000000)

format="%-7s %-6s %-3s %-8s %-9s %-5s %-22s %s\n"
printf "$format" TYPE WRITES N KEYS ACCESS SEED TRACE TIME


for writes in "${writeratio[@]}"; do
    for n in "${m[@]}"; do
        for s in "${select[@]}"; do
            naccess=$((keymax * n))
            trace="trace_${s}_w${writes}_n${n}"
            start=$SECONDS
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
            printf "$format" "$s" "$writes" "$n" "$keymax" "$naccess" "$seed" "$trace" "$((SECONDS - start))s"
        done
    done
done

python3 result_translate.py