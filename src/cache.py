
class Cache:
    def __init__(self):
        pass

    def read(self, address, timestamp):
        raise NotImplementedError()

    def write(self, address, timestamp, value):
        raise NotImplementedError()

    def evict(self, address, timestamp):
        raise NotImplementedError()


class NoCache(Cache):
    def __init__(self):
        pass

    def read(self, address, timestamp):
        return None

    def write(self, address, timestamp, value):
        return None

    def evict(self, address, timestamp):
        return None


class PushEvictCache(Cache):
    def __init__(self):
        self.storage = {}

    def read(self, address, timestamp):
        return self.storage.get(address)

    def write(self, address, timestamp, value):
        self.storage[address] = value

    def evict(self, address, timestamp):
        if address in self.storage.keys():
            self.storage.pop(address)


class TtlCache(Cache):
    def __init__(self, ttl_duration):
        self.storage = {}
        self.ttl_duration = ttl_duration

    def read(self, address, timestamp):
        result = self.storage.get(address)
        if result is None:
            return None
        if result[1] < timestamp:
            return None
        return result[0]

    def write(self, address, timestamp, value):
        self.storage[address] = (value, timestamp + self.ttl_duration)

    def evict(self, address, timestamp):
        pass

