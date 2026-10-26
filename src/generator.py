import sys
import random


def main():
    random.seed(0xCAFEBABE) # every good story ...
    
    KEYMAX = 1000000
    WRITERATIO = 0.30
    NACCESS = 10000000



    # set up vars
    if len(sys.argv) >= 2:
        KEYMAX = int(sys.argv[1])
    if len(sys.argv) >= 3:
        WRITERATIO = float(sys.argv[2])
    if len(sys.argv) >= 4:
        NACCESS = int(sys.argv[3])

    for i in range(NACCESS):
        key = random.randrange(KEYMAX)
        skey = str(key).zfill(9)
        
        val = random.randrange(KEYMAX)
        sval = str(val).zfill(9)
        
        if random.random() < WRITERATIO:
            print(f"WRITE \t{skey}\t{sval}")
        else:
            print(f"READ  \t{skey}\t---------")


if __name__ == "__main__":
    main()
    
