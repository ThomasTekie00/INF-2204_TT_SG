
class Cache:
    def __init__(self):
        pass

    def read(self, address):
        raise NotImplementedError()

    def write(self, address, value):
        raise NotImplementedError()

    def evict(self, address):
        raise NotImplementedError()


class NoCache(Cache):
    def __init__(self):
        pass

    def read(self, address):
        return None

    def write(self, address, value):
        return None

    def evict(self, address):
        return None


class PushEvictCache(Cache):
    def __init__(self):
        self.storage = {}

    def read(self, address):
        return self.storage.get(address)

    def write(self, address, value):
        self.storage[address] = value

    def evict(self, address):
        if address in self.storage.keys():
            self.storage.pop(address)

