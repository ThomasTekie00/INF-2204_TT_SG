# A simulated approach to experimental analysis of tradeoffs between hard and soft cohesion caching strategies


This repo contains a simulation that compares three caching strategies on synthetic write heavy workloads:
* NoCache (Baseline): every read goes to storage, nothing is cached
* TTL (Soft cohesion): a write only updates storage. A cached entry is served till the timer runs out
* PushEvict (Hard cohesion): a write updates storage and evicts the key from the cache

For each run we measure the hit ratio and the freshness

## Files

| File          | Purpose |
| ------------- | ------------- |
| generator.py  | Writes a trace of READ/WRITE operations to stdout |
| cache.py, api.py  | The cache strategies (NoCache, TTL, PushEvict) and the API in front of storage |
| benchmark.py | Runs a trace through a cache with a simulated clock and prints a log of every operation |
| counter.py | Reads a benchmark log on stdin and prints hit_ratio, freshness |
| tracer.sh  | Runs the whole experiment and appends the results to results.txt |
| result_translate.py | Reads results.txt and prints the table |


## Requirements
* Python 3
* tabulate (pip install tabulate)
* Bash

## Running the experiments

The experiments are run with `tracer.sh`, which must be run from the `src` directory.
The following can be pasted into a terminal from the project root:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src/
./tracer.sh

# This will run the experiment and create a translated file: translated.txt
# With the result table

# To view the file from the terminal
cat translated.txt

```

Note: `tabulate` is only installed in the venv, so the venv must be active when `tracer.sh` runs, otherwise the last step fails.

For every combination of write ratio, keymax and distribution, and for each of the 5 seeds, `tracer.sh`:
1. Generates a trace with generator.py -> 1 000 000 accesses
2. Runs benchmark.py once with NoCache and once with PushEvict, and once with TTL at each throughput
3. Pipes the log through counter.py and appends the results to results.txt
4. Deletes the trace

This gives 7 runs per trace, 420 runs in total.
At the end it runs result_translate.py, which writes the summary to `translated.txt`.

### Parameters

| Parameters | Value |
|------------|--------|
| Write ratio | 0.3 and 0.7 |
| Keymax values | 100, 1 000, 10 000 |
| Accesses per trace | 1 000 000 |
| Throughput | 1 000, 10 000, 50 000, 100 000, 200 000 |
| Distribution | Random and Zipf |
| Seeds | 1020180774, 546407847, 927367142, 1894350560, 913529236 |
| TTL (Simulated seconds) | 5  |

NoCache and PushEvict do not depend on time, so they are only run once per trace (throughput 50 000).


### Output format
Each line of results.txt is one run:
```
<dist> <write ratio> <keys> <strategy> <throughput> <ttl> <hitratio> <freshness> <seed>

```
result_translate.py groups the lines by distribution, write ratio, keys and seed, and prints one block per seed.
| Column | Meaning |
|---------|---------|
| dist  | Key distribution -> Random = uniform, zipf = a few popular keys |
| writes | Write ratio, share of requests that are writes: 30% and 70% |
| keys | Number of distinct keys |
| seed | Seed used to generate the trace |
| strategy | NoCache, no cache is used. PushEvict, writes evicts the key or TTL, the entry expires |
| window | TTL window in requests, throughput * TTL |
| hit | Amount of reads gotten from the cache |
| fresh | Amount of cache hits that are not stale(Old data) |
| useful | All of reads answered correctly from the cache: Hit * freshness. Pushevict will also have hitratio == usefulness |


## Running the benchmark

To run the benchmark you need a tracefile, the benchmark can then be run using

```shell
python3 src/benchmark.py [TRACEFILE] [ARGS] > file
```

Use `python3 src/benchmark.py h` for help with the remaining arguments.
We recommend piping the output to a file for easier parsing.

### Running the trace generator

To create a new trace to run you can either format it manually, or generate one
using the trace generator.

```shell
python3 src/generator.py [args] > file
```

We recommend piping the output to a file, as the filename is needed by the benchmark.
If you are confused about how the generator works you can use

```shell
python3 src/generator.py h
```

to get a display of the expected arguments.

Tracefiles have a format of

`[READ/WRITE] [KEY] [VALUE]`
where READ or WRITE are the literal strings, KEY is an integer and VALUE is an integer.
Note that for the literal string READ, the integer VALUE is ignored, and can be replaced with any symbol.


### Single step through
```shell
python3 generator.py <keys> <random|zipf> <writeratio> <accesses> <seed> > trace
python3 benchmark.py trace <nocache|pushevict|ttl> <throughput> <ttl seconds> | python3 counter.py
```


## Validating the benchmark
Small manual traces exist that trigger specific behaviour for a given cache.
These are found in `manual_traces/*` and can be executed with any configuration

invalid read -> cache hit but data is wrong
missed read -> cache miss
valid read -> cache hit and data is correct

**t1** `python3 src/benchmark.py manual_traces/t1.trace ttl 3 1` runs a TTL
cache over trace 1, the expected output is a write, missed read, and valid read.

**t2** `python3 src/benchmark.py manual_traces/t2.trace ttl 6 1` runs a TTL
cache over trace 2, the expected output is a write, missed read, and valid read.
new write, invalid read, and invalid read.

**t2** `python3 src/benchmark.py manual_traces/t2.trace pushevict 6 1` runs a PushEvict
cache over trace 2, the expected output is a write, missed read, and valid read.
new write, missed read, and valid read.

**t2** `python3 src/benchmark.py manual_traces/t2.trace nocache 6 1` runs NoCache
over trace 2, the expected output is that every read is a missed read and returns the newest data.

**t2 (TTL expiry)** `python3 src/benchmark.py manual_traces/t2.trace ttl 1 1.5` runs a TTL
cache with 1 access per second and a TTL of 1.5 seconds. The entry cached at time 1.0 expires at 2.5,
so the expected output is a write, missed read, and valid read.
new write, missed read (the entry has expired), and valid read with the new data.

### Validating the counter
The log can be piped through counter.py to check that hit ratio and freshness are counted correctly:

```shell
python3 src/benchmark.py manual_traces/t2.trace ttl 6 1 | python3 src/counter.py        # 0.7500 0.3333
python3 src/benchmark.py manual_traces/t2.trace pushevict 6 1 | python3 src/counter.py  # 0.5000 1.0000
python3 src/benchmark.py manual_traces/t2.trace nocache 6 1 | python3 src/counter.py    # 0.0000 0.0000
```

For TTL, 3 of 4 reads are hits and 1 of those 3 hits is fresh.
For PushEvict, 2 of 4 reads are hits and both are fresh.
NoCache has no hits, and counter.py returns 0 instead of dividing by zero.



## Reproducibility
* The simulation uses a simulated clock, not the wall clock so the same trace and the same settings will give the same result on any machine. The hardware only affects how long a run takes.
* The seeds are fixed in `tracer.sh`, so running the whole experiment again gives the same numbers.
