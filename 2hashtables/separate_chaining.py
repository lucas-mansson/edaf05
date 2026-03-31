import sys

# read words from input, one word per line
# then use a dictionary to count which word is most frequent
# but sometimes try to remove the word
# and then print the most frequent word and if there are multiple
# most frequent take the first one in alphabetical order

class SeparateChainingHashTable:

    def __init__(self) -> None:
        self.table = [[]]
        self.size = 1
        self.count = 0

        return

    # Get the value by key
    def get(self, key):
        i, j = self._get_indices(key)
        if j == -1:
            return None

        return self.table[i][j][1]

    # Updates the value for key or adds if it doesnt exist
    def set(self, key, value):
        # Check that a is not too big
        if self.count / self.size > 0.75:
            self._resize(self.size*2)

        i, j = self._get_indices(key)
        if j == -1:
            # Key does not exist, add to list
            self.table[i].append((key, value))
            self.count += 1
            return 

        self.table[i][j] = (key, value) # Update value if key exists
        return

    # Returns a boolean that indicates whether the key exists
    def contains(self, key):
        return self.get(key) is not None

    # Deletes the element if exists and 
    # returns boolean indicating whether it was deleted
    def delete(self, key):
        i, j = self._get_indices(key)
        if j == -1:
            return False

        del self.table[i][j]
        self.count -= 1
        
        if self.count / self.size < 0.25:
            self._resize(self.size // 2)

        return True

    def keys(self):
        return [k for l in self.table for (k, _) in l]

    def values(self): 
        return [v for l in self.table for (_, v) in l]

    # Helper function that returns indices (i, j), 
    # where i is the "array" index and j is the "List" index
    # or -1 for list if it does not exist
    def _get_indices(self, key):
        i = self._hash(key)
        for j, (k, _) in enumerate(self.table[i]):
            if k == key:
                return i, j

        return i, -1

    def _hash(self, value):
        return hash(value) % self.size

    def _resize(self, new_size):
        curr_table = self.table
        self.size = new_size
        self.count = 0
        self.table = [[] for _ in range(self.size)]

        for l in curr_table:
            for k, v in l:
                self.set(k, v)
        return


d = SeparateChainingHashTable()

i = 0

for line in sys.stdin:
	word = line.strip()
	is_present = d.contains(word)
	remove_it = i % 16 == 0

	if is_present:
		if remove_it:
			d.delete(word)
		else:
			count = d.get(word)
			d.set(word, count + 1)
	elif not remove_it:
		d.set(word, 1)
	i += 1

(count, word) = max(zip(d.values(), d.keys()))

for k in d.keys():
	if d.get(k) == count and k < word:
		word = k

print(word, count)
