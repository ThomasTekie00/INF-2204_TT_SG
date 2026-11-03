import sys

def counter(trace, warmup=0):
    cache_hits = 0
    total_reads = 0
    fresh_hits = 0

    for i, line in enumerate(trace):
        if i < warmup:
            continue

        if "API-Query=READ" in line:
            total_reads += 1

            if "CACHE_HIT=True" in line:
                cache_hits += 1

                if "CACHE_VALID=True" in line:
                    fresh_hits += 1

    hit_ratio = cache_hits / total_reads if total_reads else 0
    freshness = fresh_hits / cache_hits if cache_hits else 0

    return hit_ratio, freshness


#KPIs
warmup = 4000000

if __name__ == "__main__":
    hit_ratio, freshness = counter(sys.stdin, warmup)
    print(hit_ratio, freshness)