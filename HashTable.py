class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, package):
        key = package.id
        index = self._hash(key)
        for item in self.table[index]:
            if item.id == key:
                item.__dict__.update(package.__dict__)
                return
        self.table[index].append(package)

    def lookup(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item.id == key:
                return item
        return None

    def all_packages(self):
        return [package for bucket in self.table for package in bucket]
