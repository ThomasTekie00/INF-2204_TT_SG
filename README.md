# Running the experiments

The experiments can be ran from a shell script,
ensure you run it from the src directory and have installed all requirements.
the following can be pasted into a terminal from the project root.

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src/
./tracer.sh
```

# Running the trace generator

To create a new trace to run you can either format it manually, or generate one
using the trace generator.

```shell
python3 src/generator.py [args] > file
```

we recomend piping the output to a file, as the filename is needed by the benchmark
if you are confused about how the generator works you can use

```shell
python3 src/generator.py h
```

to get a display of the expected arguments.

tracefiles have a format of

`[READ/WRITE] [KEY] [VALUE]`
where READ or WRITE are the literal strings, KEY is an integer and VALUE is an integer.
note that for the literal string READ, the integer VALUE is ignored. and can be replace with any symbol.


# Running the benchmark

to run the benchmark you need a tracefile, the benchmark can then be ran using

```shell
python3 src/benchmark.py [TRACEFILE] [ARGS] > file
```

use `python3 src/benchmark.py h` for help with the remaining arguments.
we recomend piping the output to a file for easier parsing.

# Validating the benchmark
small manual traces exist that trigger specific behaviour for a givven cache.
these are found in `manual_traces/*` and can be executed with any configuration

invalid read -> cache hit but data is wrong
missed read -> cache miss
valid read -> cache hit and data is correct

**t1** `python3 src/benchmark.py manual_traces/t1.trace ttl 3 1` runs a TTL
cache over trace 1, the expected output is a write, missed read, and valid read.

**t2** `python3 src/benchmark.py manual_traces/t2.trace ttl 6 1` runs a TTL
cache over trace 2, the expected output is a write, missed read, and valid read.
new write, invalid read, and invalid read.

**t2** `python3 src/benchmark.py manual_traces/t2.trace pushevict 6 1` runs a TTL
cache over trace 2, the expected output is a write, missed read, and valid read.
new write, missed read, and valid read.


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
