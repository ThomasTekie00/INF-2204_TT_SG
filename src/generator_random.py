import sys
import random

def show_help():
    print("usage: program [keymax] [writeratio] [naccess] [seed]")

def main():
    # set up vars
    if len(sys.argv) != 5:
        show_help()
        return
    
    if sys.argv[1].startswith("h"):
        show_help()
        return
    
    keymax = int(sys.argv[1])
    writeratio = float(sys.argv[2])
    naccess = int(sys.argv[3])
    seed = int(sys.argv[4])

    random.seed(seed) # every good story ...

    # prepare formatting
    fill_len = len(str(keymax))
    
    for i in range(naccess):
        key = random.randrange(keymax)
        skey = str(key).zfill(fill_len)
        
        val = random.randrange(keymax)
        sval = str(val).zfill(fill_len)
        
        if random.random() < writeratio:
            print(f"WRITE \t{skey}\t{sval}")
        else:
            print(f"READ  \t{skey}\t---------")

if __name__ == "__main__":
    main()
