
from collections import defaultdict

class HashMap:
    def __init__(self, initial_capacity=20):
        self.table = defaultdict(list)
        self.capacity = initial_capacity

    def insert(self, key, item):
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return

        bucket_list.append([key, item])

    def lookup(self, key):
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None

    def remove(self, key):
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for i, pair in enumerate(bucket_list):
            if key == pair[0]:
                del bucket_list[i]
                return