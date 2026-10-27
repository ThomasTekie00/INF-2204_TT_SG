import sys
import cache
import api

def show_help():
    print("usage: benchmark trace strategy")
    print("Strategy :: [nocache | pushevict]")
    return

def main():
    caching_strategy = None
    file_path = None

    if len(sys.argv) >= 2:
        if sys.argv[1].startswith("h"):
            show_help()
            return    
        file_path = sys.argv[1]

    if len(sys.argv) >= 3:
        caching_strategy = sys.argv[2]

    if caching_strategy is None:
        show_help()
        return
    if file_path is None:
        show_help()
        return
    
    with open(file_path, "r") as f:
        data = f.read()

    benchmark_api = None
    if caching_strategy == "pushevict":
        benchmark_api = api.API(cache.PushEvictCache())
    if caching_strategy == "nocache":
        benchmark_api = api.API(cache.NoCache())
    if benchmark_api is None:
        show_help()
        return


    for line in data.splitlines():
        command = line.split()
        method = command[0]
        address = command[1]
        value = command[2]
        
        if method == "READ":
            result = benchmark_api.read(address)
            print(f"read: {result[0]} {result[1]} {result[2]} {result[3]} ")
        
        elif method == "WRITE":
            result = benchmark_api.write(address, value)

if __name__ == "__main__":
    main()
