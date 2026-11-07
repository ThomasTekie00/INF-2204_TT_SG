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
In this paper we take a simulated experimental approach to comparing the cost
and tradeoffs in a `GET/SET` system, The aim is to asses the tradeoffs 
between hard and soft cohesion caching in a reproducible manner that is independent
of underlying systems.

We evaluate two policies for caching, these being push-based eviction and
TTL. And build our assumptions around small write-heavy services in web-applications.
Our underlying assumption through this work is that certain systems might be more
interested in "fresh" data, that is data for which a cache returns the most recently
written value, and we try to highlight some of the potential costs in terms
of cache-hit ratios and a metric of "usefulness" that we argue carries significance
for such systems.

# Related work
We build on our previous work, that is available in the Github repository alongside
the source files for our experiments and simulations. Further several articles
exist, as for instance surveys, case studies and theoretical foundations for
evaluating cache-behavior in different systems. We compliment the existing research
in this field by providing both an overview of the specific question relating to 
concrete "costs" of hard cohesion, evaluating a metric considering both overall cache hit ratios
to the "correctness" of retrieved data, and by providing reproducible results through
simulations.

# Terms and Definitions
A `GET/SET` system is some system in which we can arbitrarily store data using
a `GET` or a `SET` operation. Examples include SQL Databases, NoSQL Databases,
Maps, Dictionaries, Off-the-shelf caching-solutions like memcached, and storage-api's.

In our simulation there are two types of storage, the cache, and the underlying storage.
our underlying storage is some arbitrary `GET/SET` system that will always be correct.
when a `SET` operation is performed, we perform that operation directly on our storage.

when a `GET` operation is performed, this is performed first towards our cache,
the cache then returns whatever entry it holds, or defers to storage if no valid entry is
found, this defering to storage is a **cache miss**, the inverse is a **cache hit**.
our cache-hit-ratio is defined as the number of cache hits over all `GET` operations.

each item is stored alongside some key, and can be retrieved using that same key.
we consider the "correctness" of our data to be a binary question. if a `GET` operation
on some key provides the most recent data that was supplied in a `SET` operation;
our data is correct. the ratio of correct keys from `GET` operations over all 
`GET` operations is considered the **freshness** of a system.

The **usefulness** of our system is defined as the number of correct cache hits.
and is calculated given `FRESHNESS * HIT-RATIO`. 

a write-heavy service is assumed to be a service in which at least 30% of the
`GET` and `SET` operations are `SET` operations \[1].

# Design and implementation

Our simulation encapsulates a "core", consisting of an arbitrary `GET/SET` api
with some cache implementation, and the experimental pipeline consists of constructing
a pregenerated access-pattern or trace, feed this into our simulation core, and then
reporting the status of each request as it occurs.

## Simulation Core

## Trace Generation

## Benchmarking

# Results and discussion

# Limitations
* not representative of a real system
* simulated runtime != real runtime on hardware
* limited key space to force reuse, real systems have larger key-sizes
* assumes continous time, does not regard the fact that some requests take longer than others.
* assume single threaded, does not regard concurrency

# Conclusion

# Sources

\[1] twemcached - twitter paper
