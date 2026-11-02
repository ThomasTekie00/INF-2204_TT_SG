import sys
import random

zipf_cache = {}
# bounded selection of random variable based on zipfian distribution
def zipf(max):
    d = zipf_cache.get(max, None)

    if d is None:
        d = []
        for idx, value in enumerate(range(0, max)):
            for _ in range(0, (max / (2 * (idx + 1)))):
                d.append(value)
        zipf_cache[max] = d
    
    return random.choice(d)

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
