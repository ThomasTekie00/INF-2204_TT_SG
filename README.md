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