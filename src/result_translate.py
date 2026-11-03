def read_results(file):
    results = []

    with open(file) as file:
        for line in file:
            dist, writes, n, strategy, tp, ttl, hit, fresh = line.split()
            results.append({
                "dist": dist, "writes": float(writes), "n": int(n),
                "strategy": strategy, "tp": int(tp), "ttl": float(ttl),
                "hit": float(hit), "fresh": float(fresh),
            })

    return results


if __name__ == "__main__":
    results = read_results("results.txt")

    for i in results:
        print(i["dist"], i["writes"], i["n"], i["strategy"], i["hit"], i["fresh"])