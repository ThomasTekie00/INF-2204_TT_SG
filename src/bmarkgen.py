traces = 4
throughput = [10000, 1000000]
ttl = [0.3, 30]
strategy = ["ttl", "pushevict"]

for t in range(traces):
    for tp in throughput:
        for s in strategy:
            if s == "ttl":
                for tl in ttl:
                    print(f"trace {t} strategy={s} throughput={tp} ttl={tl}")
            else:
                    print(f"trace {t} strategy={s} throughput={tp} ttl=0")