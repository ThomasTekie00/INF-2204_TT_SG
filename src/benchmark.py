import sys
import cache
import api

def show_help():
    print("usage: benchmark trace strategy throughput ttl")
    print("trace :: output from generator.py as a text-file")
    print("Strategy :: ['nocache' | 'pushevict' | 'ttl']")
    print("Throughput :: integer number of api accesses per second")
    print("ttl :: float for TTL duration in seconds")
    return

def run_simulation(trace, benchmark_api, timestep):
    simulation_time = 0
    for line in trace.splitlines():
        command = line.split()
        method = command[0]
        address = command[1]
        value = command[2]
        
        if method == "READ":
            addr, data, is_hit, is_valid = benchmark_api.read(address, simulation_time)

        if method == "WRITE":
            addr, data, is_hit, is_valid = benchmark_api.write(address, simulation_time, value)

        s = f"API-Query={method}\t"
        s += f"ADDRESS={addr}\t"
        s += f"DATA={data}\t"
        s += f"CACHE_HIT={is_hit}\t"
        s += f"CACHE_VALID={is_valid}\t"
        s += f"SIM_TIME={simulation_time}"
        print(s)
        simulation_time += timestep

def main():

    if len(sys.argv) != 5:
        show_help()
        return    

    if sys.argv[1].startswith("h"):
        show_help()
        return    

    trace_file = sys.argv[1]
    caching_strategy = sys.argv[2]
    throughput = int(sys.argv[3])
    ttl_duration = float(sys.argv[4])

    
    with open(trace_file, "r") as f:
        trace = f.read()

    benchmark_api = None
    if caching_strategy == "pushevict":
        benchmark_api = api.API(cache.PushEvictCache())
    elif caching_strategy == "nocache":
        benchmark_api = api.API(cache.NoCache())
    elif caching_strategy == "ttl":
        benchmark_api = api.API(cache.TtlCache(ttl_duration))
    if benchmark_api is None:
        show_help()
        return

    timestep = 1 / throughput
    run_simulation(trace, benchmark_api, timestep)

if __name__ == "__main__":
    main()
