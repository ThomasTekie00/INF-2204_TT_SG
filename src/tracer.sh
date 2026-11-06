#!/bin/bash

set -euo pipefail

writeratio=(0.3 0.7)
keymax_values=(10000 1000 100)
naccess=1000000
select=(random zipf)
seed=1

ttl=(5)
tp=(50000 100000 200000)

format="%-7s %-6s %-3s %-8s %-9s %-5s %-22s %s\n"
printf "$format" TYPE WRITES N KEYS ACCESS SEED TRACE TIME


for writes in "${writeratio[@]}"; do
    for keymax in "${keymax_values[@]}"; do
        for s in "${select[@]}"; do
            trace="trace_${s}_w${writes}_k${keymax}"
            start=$SECONDS
            python3 generator.py $keymax $s $writes $naccess $seed > "$trace"

            for through in "${tp[@]}"; do
                for time in "${ttl[@]}"; do
                    res=$(python3 benchmark.py "$trace" ttl $through $time | python3 counter.py)
                    echo "$s $writes $keymax ttl $through $time $res" >> results.txt
                done
                res=$(python3 benchmark.py "$trace" pushevict $through 0 | python3 counter.py)
                echo "$s $writes $keymax pushevict $through 0 $res" >> results.txt
            done

            rm "$trace"
            printf "$format" "$s" "$writes" "$keymax" "$keymax" "$naccess" "$seed" "$trace" "$((SECONDS - start))s"
        done
    done
done

python3 result_translate.py >> translated.txt