# 4mill og 16mill for 1 og 4 gig ram ved 250 bytes per cache entry
keymax = [4000000]
writeratio = [0.3 , 0.7] # 30% = "high write" twemcache
seed = 1
gen = ["random", "zipf"]
naccess_multi = [5, 20] # 5 gir 20% oppvarming først, 20 gir 5% oppvarming


cfg = 0
for k in keymax:
    for w in writeratio:
        for m in naccess_multi:
            for g in gen:
                cfg += 1
                print(f"config {cfg} keymax={k} distribution={g} writeratio={w} naccess={k*m} seed={seed}") 
