import sys
import random
import itertools

zipf_cache = {}
def zipf(max, s=1.0):
    r = zipf_cache.get(max, None)

    if r is None:
        a = [i for i in range(max+1)]
        n = len(a)
        w = [1.0 / ((i + 1) ** s) for i in range(n)]
        w = list(itertools.accumulate(w))
        zipf_cache[max] = (a,w)
    else:
        a, w = r[0], r[1]

    return random.choices(a, cum_weights=w)[0]

def show_help():
    print("usage: program [keymax] [distribution] [writeratio] [naccess] [seed]")
    print("distribution must be either 'random' or 'zipf'")

def main():
    # set up vars
    if len(sys.argv) != 6:
        show_help()
        return
    
    if sys.argv[1].startswith("h"):
        show_help()
        return
    
    keymax = int(sys.argv[1])
    distribution = sys.argv[2]
    writeratio = float(sys.argv[3])
    naccess = int(sys.argv[4])
    seed = int(sys.argv[5])

    r_func = None
    if distribution == "random":
        r_func = random.randrange
    elif distribution == "zipf":
        r_func = zipf
    else:
        show_help()
        return

    random.seed(seed) # every good story ...

    # prepare formatting
    fill_len = len(str(keymax))
    
    for i in range(naccess):
        key = r_func(keymax)
        skey = str(key).zfill(fill_len)
        
        val = random.randrange(keymax)
        sval = str(val).zfill(fill_len)
        
        if random.random() < writeratio:
            print(f"WRITE \t{skey}\t{sval}")
        else:
            print(f"READ  \t{skey}\t---------")

if __name__ == "__main__":
    main()
