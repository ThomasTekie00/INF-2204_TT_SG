# A simulated approach to experimental analysis of tradeoffs between hard and soft cohesion caching strategies


This repo contains a simulation that compares three caching strategies on synthetic write heavy workloads:
* NoCache: Every read goes to storage, where the hitratio is 0, so its not run 
* TTL (Soft cohesion): a write only updates storage. A cached entry is served till the timer runs out
* PushEvict (Hard cohesion): a write updates storage and evicts the key from the cache

For each run we measure the hit ratio and the freshness

# Files

| File          | Purpose |
| ------------- | ------------- |
| generator.py  | Writes a trace of READ/WRITE operations to stdout |
| cache.py, api.py  |  |
| benchmark.py |                     |
| counter.py | Reads a benchmark log on stdin and prints hit_ratio, freshness|
| tracer.sh  | Runs the whole experiment and appends the results to results.txt |
| results_translate.py | Reads results.txt and prints the tabell |


# Requirements
* Python 3
* tabulate (pip install tabulate)
* Bash

# Running the experiment
```
# This will run the experiment and create a translated file: translated.py
# With the result tabell

./tracer.sh

#To view the file from the terminal
cat translated.py

```
1. generates a trace with generator.py -> 1 000 000 access, seed 1
2. runs benchmark.py for TTL and PushEvict at each throughput
3. pipes the log through counter.py and appends the results to results.txt
4. Deletes the trace

At the end it runs results_translate.py, which writes the summary to translated.txt. The table can also be printed again with python3 results_translate.py

# Parameters

| Parameters | Value |
|------------|--------|
| Write ratio | 0.3 and 0.7 |
| Keymax values | 100, 1 000, 10 000 |
| Accesses per trace | 1 000 000 |
| Throughput | 50.000, 100.000, 200 000 |
| Distrubtion | Random and Zipf |
| Seed | 1 |
| TTL (Simulated seconds) | 5  |

# Single step through
```
python3 generator.py <keys> <random|zipf> <writeratio> <accesses> <seed> > trace

python3 benchmark.py trace <nocache|pushevict|ttl> <throughput> <ttl seconds> | python3 counter.py


```

# Output format
Each line of results.txt is one run:
```
<dist> <write ratio> <keys> <strategies> <throughput> <ttl> <hitratio> <freshness>

```
result_transplate.py groups these by strategy and prints:
| Column | Meaning |
|---------|---------|
|      dist  | Key distribution -> Random = uniform, zipf = a few popular keys        |
|   writes      | write ratio, share of requests that are writes: 30% and 70%         |
|  keys        |Number of distinct keys         |
| strategy | PushEvict, writes evicts the key or TTL, the entry expires|
| window | TL window in requests, throughput * TTL| 
| hitratio |Amount of reads gotten from the cache |
|freshness | Amount of cache hits that are not stale(Old data)| 
|Usefulness | All of reads answered correctly from the cache: Hit * freshness Pushevict will also have hitratio == usefulness |

For PushEvict, freshness is always 100%, so usefulness equals hit


# Reproduceibility
* The simulation uses a simulated clock, not the wall clock so the same trace and the same settings will give the same result on any machine. The hardware only affects how long a runs takes.