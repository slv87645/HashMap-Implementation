# Name: Steven Vu
# Description: Hash Table implementation with Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        updates a key/value pair in the hash map

        param key: identifying value for object
        param value: data for object

        returns: nothing
        """

        # resize table if load factor is greater than or equal to 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # find index
        index = self._hash_function(key) % self._capacity

        # if key exists in hash map, replace value with passed value
        containsKey = self._buckets[index].contains(key)
        if containsKey:
            containsKey.value = value

        # if key does not exist, add key/value pair
        else:
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets

        :returns: integer value
        """
        # initialize counter
        emptyBuckets = 0

        # check if each bucket is empty, increment counter if true
        for _ in range(self._capacity):
            bucket = self._buckets[_]
            if bucket.length() == 0:
                emptyBuckets += 1

        return emptyBuckets

    def table_load(self) -> float:
        """
        returns: load factor of hash map as float value
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        clears contents of hash map
        """
        # create new empty buckets
        newBuckets = DynamicArray()
        for _ in range(self._buckets.length()):
            newBuckets.append(LinkedList())

        self._buckets = newBuckets
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table and rehashes the links

        param new_capacity: new capacity of hash table that needs to be prime or be changed to prime

        :returns: nothing
        """
        if new_capacity < 1:
            return

        # create new buckets and check if new capacity is a prime number
        newBuckets = DynamicArray()
        if new_capacity == 2:
            self._capacity = new_capacity
            self._size = 0
        else:
            new_capacity = self._next_prime(new_capacity)
            self._capacity = new_capacity
            self._size = 0
        for _ in range(new_capacity):
            newBuckets.append(LinkedList())

        # set newBuckets as data member to enable put method
        oldBuckets = self._buckets
        self._buckets = newBuckets

        # rehash key/value pairs from oldBuckets
        for bucket_index in range(oldBuckets.length()):
            bucket = oldBuckets[bucket_index]

            if bucket.length() != 0:
                for node in bucket:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        returns value associated with key

        param key: identifier for a value

        :returns: value of key
        """
        # calculate index
        index = self._hash_function(key) % self._capacity

        # iterate through nodes of linked list in bucket
        for node in self._buckets[index]:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        checks if key is in hash map

        param key: value to be searched for in map

        :returns: True if key is found, otherwise False
        """
        if self._size == 0:
            return False

        # calculate index and use linkedlist contains method
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        removes the given key and its value from hash map

        param key: key to be removed

        :returns: nothing
        """
        if not self.contains_key(key):
            return

        index = self._hash_function(key) % self._capacity
        self._buckets[index].remove(key)
        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns tuple pairing of key/value pairs in a dynamic array

        :returns: dynamic array object
        """
        # creates new dynamic array
        newDA = DynamicArray()

        # iterates through nodes of each bucket and adds key value pairs to new array
        for bucketIndex in range(self._capacity):
            bucket = self._buckets[bucketIndex]
            if bucket.length() != 0:
                for node in bucket:
                    keyValues = (node.key, node.value)
                    newDA.append(keyValues)

        return newDA


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    determines the mode(s) and its frequency in an array

    param da: array to be searched

    returns DynamicArray: array containing tuple of mode(s) and its frequency
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # Adds each element in passed array to hash map as the key with value being current count
    for index in range(da.length()):
        element = da[index]
        if map.contains_key(element):
            count = map.get(element) + 1
            map.put(element, count)
        else:
            map.put(element, 1)

    # Finds the maximum frequency
    maxFrequency = 0
    kvArray = map.get_keys_and_values()
    for index in range(kvArray.length()):
        keyValue = kvArray[index]
        frequency = keyValue[1]
        if frequency > maxFrequency:
            maxFrequency = frequency

    # Add elements with max frequency to array
    modes = DynamicArray()
    kvArray = map.get_keys_and_values()
    for index in range(kvArray.length()):
        keyValue = kvArray[index]
        if keyValue[1] == maxFrequency:
            modes.append(keyValue[0])

    return modes, maxFrequency

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
