
class HashTable:
    def __init__(self, capacity=20):
        #Initialize the HashTable with a specific capacity (default is 20).
        #The table is an array of lists (buckets), where each bucket holds key-value pairs.
        self.capacity = capacity
        self.table = [[] for _ in range(self.capacity)]

    def insert(self, key, item):
        #Insert key-value pair into hash table.
        #If key already exists, update the value.
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return

        bucket_list.append([key, item])

    def lookup(self, key):
        #Look up a value by key in the hash table.
        #Returns the value if the key is found, otherwise returns None.
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None

    def remove(self, key):
        #Remove a key-value pair from the hash table by key.
        bucket = hash(key) % self.capacity
        bucket_list = self.table[bucket]

        for i, pair in enumerate(bucket_list):
            if key == pair[0]:
                del bucket_list[i]
                return