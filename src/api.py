import cache

class API:
    def __init__(self, cache):
        self.storage = {}
        self.cache = cache

    def read(self, address):
        """Returns a tuple (address, result, is_hit, is_valid)"""
        storage_result = self.storage.get(address, None)
        cache_result = self.cache.read(address)

        result = cache_result
        is_hit = cache_result is not None
        is_valid = cache_result == storage_result
        
        if not is_hit:
            self.cache.write(address, storage_result)
            result = storage_result

        return (address, result, is_hit, is_valid)

    def write(self, address, data):
        """Returns a tuple (address, written_data, ---, ---)"""
        self.storage[address] = data
        self.cache.evict(address)
        return (address, data, None, None)