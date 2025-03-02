class HashTable:

    # source: "C950 - Webinar-1 Let's Go Hashing (30 min)"
    # time and space complexity O(n) - appending [] to a table n times
    def __init__(self, initial_capacity = 13):
        # initializing table
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # time complexity O(n) - loop through bucket list for matching key
    # space complexity O(1)
    def insert(self, key, package):
        # determine which bucket the [key, package] pair goes into
        bucket = hash(key) % len(self.table)

        # this is the list of pairs within a given bucket
        bucket_list = self.table[bucket]

        # update package if its key is already present in the bucket_list
        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = package
                return True

        # otherwise add a new pair to the end of the bucket_list
        key_value = [key, package]
        bucket_list.append(key_value)
        return True

    # look-up function that uses a key(id) to return the associated value(package object)
    # time complexity O(n)
    # space complexity O(1)
    def lookup(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # check if key(id) is in the bucket
        for key_value in bucket_list:
            if key_value[0] == key:
                # yes - returns the value(package object)
                return key_value[1]
        # no - returns None
        return None