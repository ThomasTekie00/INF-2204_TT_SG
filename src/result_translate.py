
from tabulate import tabulate



def read_file(res):
    ttl_row = []
    push_row = {}
    

    with open(res, "r") as results:
        for line in results:
            if not line.strip():
                continue

            dist, writes, keymax, strategy, throughput, ttl, hit, fresh = line.split()
            writes = float(writes)
            keymax = int(keymax)
            throughput = int(throughput)
            ttl = float(ttl)
            hit = float(hit)
            fresh = float(fresh)


            if strategy == "ttl":
                ttl_row.append({
                    "dist": dist,
                    "writeratio": writes,
                    "keymax": keymax,
                    "throughput": throughput,
                    "TTL": ttl,
                    "window": throughput * ttl,
                    "hitratio": hit,
                    "freshness": fresh,
                    "useful": hit * fresh,
                })

            elif strategy == "pushevict":
                push_row[(dist, writes, keymax)] = {
                    "hitratio": hit,
                    "freshness": fresh,
                    "useful": hit * fresh,
                }

    return ttl_row, push_row


if __name__ == "__main__":
    ttl_row, push = read_file("results.txt")

    table = []
    for key in sorted(push):
        dist, writes, keymax = key
        p = push[key]

        table.append([dist, writes, keymax, "PushEvict", "-",
                      f"{p['hitratio']:.1%}",
                      f"{p['freshness']:.1%}",
                      f"{p['useful']:.1%}"])

        for i in ttl_row:
            if (i["dist"], i["writeratio"], i["keymax"]) == key:
                table.append(["", "", "", "TTL", int(i["window"]),
                              f"{i['hitratio']:.1%}",
                              f"{i['freshness']:.1%}",
                              f"{i['useful']:.1%}"])

    head = ["dist", "writes", "keys", "strategy", "window",
            "hit", "fresh", "useful"]

    print()
    print("Dist: Key distribution -> Random = uniform, zipf = a few popular keys")
    print("Writes: write ratio, share of requests that are writes: 30% and 70%")
    print("Keys: Number of distinct keys")
    print("Strategy: PushEvict, writes evicts the key or TTL, the entry expires")
    print("Window: TTL window in requests, throughput * TTL")
    print("Hit: Amount of reads gotten from the cache")
    print("Fresh: Amount of cache hits that are not stale(Old data)")
    print("Useful: All of reads answered correctly from the cache: Hit * freshness")
    print(" Pushevict will also have hitratio == usefulness ")
    print()



    print(tabulate(table, headers=head, floatfmt=".2f"))

