#!/bin/bash

set -euo pipefail

writeratio=(0.3 0.7)
keymax_values=(10000 1000 100)
naccess=1000000
select=(random zipf)
seeds=(1020180774 546407847 927367142 1894350560 913529236)

ttl=(5)
tp=(1000 10000 50000 100000 200000)

format="%-10s %-7s %-7s %-9s %-9s %-12s %-8s\n"
printf "$format" DISTRIBUTION WRITES KEYS ACCESS SEED TRACE TIME
rm -f results.txt translated.txt


for writes in "${writeratio[@]}"; do
    for keymax in "${keymax_values[@]}"; do
        for s in "${select[@]}"; do
            for seed in "${seeds[@]}"; do
                trace="trace_${s}_w${writes}_k${keymax}_seed${seed}"
                start=$SECONDS
                python3 generator.py $keymax $s $writes $naccess $seed > "$trace"

                res=$(python3 benchmark.py "$trace" nocache 50000 0 | python3 counter.py)
                echo "$s $writes $keymax nocache 50000 0 $res $seed" >> results.txt

                # PushEvict does not depend on time, so one run per trace is enough
                res=$(python3 benchmark.py "$trace" pushevict 50000 0 | python3 counter.py)
                echo "$s $writes $keymax pushevict 50000 0 $res $seed" >> results.txt

                for through in "${tp[@]}"; do
                    for time in "${ttl[@]}"; do
                        res=$(python3 benchmark.py "$trace" ttl $through $time | python3 counter.py)
                        echo "$s $writes $keymax ttl $through $time $res $seed" >> results.txt
                    done
                done

                rm "$trace"
                printf "$format" "$s" "$writes" "$keymax" "$naccess" "$seed" "$trace" "$((SECONDS - start))s"
            done
        done
    done
done

python3 result_translate.py >> translated.txt