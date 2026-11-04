---
title: A simulated approach to experimental analysis of tradeoffs between hard and soft cohesion caching strategies
subtitle: INF-2204 | UiT | Fall 26
author:
        - Simon Gilbu
        - Thomas Tekkie
papersize: a4
geometry: "top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm"
classoption: twocolumn
numbersections: true
---

# Introduction
In this paper we take a simulated experimental approach to benchmarking different
strategies for caching in a `GET/SET` system, The aim is to asses the tradeoffs 
between hard and soft cohesion caching in a reproducible manner that is independent
of underlying systems.

We evaluate two policies for caching, these being push-based eviction and
TTL. And build our assumptions around small write-heavy services in web-applications.


# Terms and Definitions
A `GET/SET` system is some system in which we arbitrarily can store data using
a `GET` or a `SET` operation. Examples include SQL Databases, NoSQL Databases,
Maps, Dictionaries, Off-the-shelf caching-solutions like memcached, and storage-api's.

a write-heavy service is assumed to be a service in which at least 30% of the
`GET` and `SET` operations are `SET` operations \[1].

# Related Works

# Design



# Methodology

## Traces

In order to generate access patterns two different approaches are used;

**RANDOM:** we distribute our keys we wish to access inside a random distribution 
where each key is equally likely given a range `[0..N]`.

**ZIPFIAN:** we distribute the keys we wish to access inside a zipfian distribution 
where each keys likelihood is givven as `(N / ((a+1) ^ s )) / N` for each `a` in the 
range `[0..N]`. where s is a factor determining the curve for our distribution

Each trace is generated with a limited number of "accesses", each access represents
either a `GET` or a `SET` operation, we use the values `5 * N` and `20 * N` based on
assumptions about our **RANDOM** distribution. for `5 * N` accesses we would 'touch'
each key 5 times, the "first" touch of a key will function as a "warmup" of our cache
system, that means in the `5 * N` case, we expect the first `1 / 5` or 20% of our
activity to be targeting a "cold" or "unpopulated" cache. for the `20 * N` case
this accounts for an assumed 5% of our run.

Traces are set to touch `4,000,000` keys, Many VPS services such as linode/akamai
and 

## Cache Access Simulation


# Results and discussion

# Limitations

* not representative of a real system
* simulated runtime != ral runtime on hardware
* assumes 4,000,000 keys for 1gig system with 256 byte entries (not real)
* assume single threaded, does not regard concurrency

# Conclusion

# Sources

\[1] twemcached - twitter paper