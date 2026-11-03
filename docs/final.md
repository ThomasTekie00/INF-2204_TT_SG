# further work // limitations // discussion

* not representative of a real system
* simulated runtime != ral runtime on hardware
* assumes 4,000,000 keys for 1gig system with 256 byte entries (not real)
* assume single threaded, does not regard concurrency

* Warmup: When the simulation starts, the cache is empty -> The first READs are misses. This isnt the stragety problem, but because nothing is saved yet. IF we include the start, the hit ratio is going to look bad -> So to combat this we wwant to check the cache when its on normal drift, meaning we let the cache fill up without them being counted in for the hits/misses.

* The warmup is equal to the amount of keymax:
* n = 5 -> Total lines = 20 000 000 -> Warm up = 4 000 000 -> 20% of the line is warmup

* n = 20 -> Total lines = 80 000 000 -> Warm up = 4 000 000 -> 5% of the wamrup