# use of existing hash function djb
def djb2(key):
    hash_value = 5381
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # hash * 33 + c
    return hash_value

class Node:
    # represents a node in the hash table
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# function to create an empty hash table of given size
def create_table(size):
    return [None] * size

# function to hash a key and map it to an index in the table
def hash_key(key, size):
    return djb2(key) % size

# insert into table function
def insert(table, key, value):
    index = hash_key(key, len(table))
    node = table[index]

    if node is None:
        table[index] = Node(key, value)
        return

    prev = None
    while node is not None:
        if node.key == key:
            node.value = value
            return
        prev = node
        node = node.next

    prev.next = Node(key, value)

# lookup from table function
def lookup(table, key):
    index = hash_key(key, len(table))
    node = table[index]

    while node is not None:
        if node.key == key:
            return node.value
        node = node.next

    return None

# delete from table function
def delete(table, key):
    index = hash_key(key, len(table))
    node = table[index]
    prev = None

    while node is not None:
        if node.key == key:
            if prev is None:
                table[index] = node.next
            else:
                prev.next = node.next
            return True
        prev = node
        node = node.next

    return False

# function to get the number of all key value pairs
def table_size(table):
    size = 0
    for node in table:
        while node is not None:
            size += 1
            node = node.next
    return size

# function to resize hash table when needed
def resize_table(table, resize_factor):
    new_size = int(len(table) * resize_factor)
    new_table = create_table(new_size)
    for node in table:
        while node is not None:
            insert(new_table, node.key, node.value)
            node = node.next
    return new_table

# generator function to yield key-value pairs stored in the hash table
def items(table):
    for node in table:
        while node is not None:
            yield (node.key, node.value)
            node = node.next

# function to count word frequencies in a text and populate a hash table
def count_word_frequencies(text, table_size_multiplier=0.2):
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    table_size = int(len(words) * table_size_multiplier)
    table = create_table(table_size)

    for word in words:
        frequency = lookup(table, word)
        if frequency is None:
            insert(table, word, 1)
        else:
            insert(table, word, frequency + 1)

    return table

# Example usage
filename = "The Alien Intelligence.txt"
with open(filename, "r", encoding="utf-8") as file:
  text = file.read()
hash_table = count_word_frequencies(text)


# Tests to see if each function works

# to get items of the tabel (all of the words in the book "The Alien Intelligence")
for key, value in items(hash_table):
    print(f"{key}: {value}")
    
# insert
print(insert(hash_table, "Arizona", 1)) 

# lookup
print(lookup(hash_table, "Arizona"))    

# delete
print(delete(hash_table, "Arizona"))    

# get length of hash table
print(len(hash_table))

# get the number of key value pairs
print(table_size(hash_table))
