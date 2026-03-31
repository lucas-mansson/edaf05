import sys

# read words from input, one word per line
# then use a dictionary to count which word is most frequent
# but sometimes try to remove the word
# and then print the most frequent word and if there are multiple
# most frequent take the first one in alphabetical order

class LinearProbingHashTable:

    def __init__(self) -> None:
        self.table: list[tuple | None] = [None] * 8
        self.size = 8 # m, length of array
        self.count = 0 # n, nbr of non-null elements

        return

    def get(self, key):
        i = self._hash(key)

        while self.table[i] is not None:
            pair = self.table[i]
            if pair is not None and pair[0] == key:
                return pair[1]
            i = (i + 1) % self.size

        return None

    def set(self, key, value):
        if self.count / self.size >= 0.5:
            self._resize(self.size*2)

        i = self._hash(key)

        pair = self.table[i]
        while pair is not None:
            if pair[0] == key: 
                self.table[i] = (key, value)
                return
            i = (i + 1) % self.size
            pair = self.table[i]

        self.table[i] = (key, value)
        self.count += 1

        return

    # Deletes the element if exists and 
    # returns boolean indicating whether it was deleted
    def delete(self, key):
        i = self._find_index(key)
        if i < 0:
            return False
        
        while True:
            self.table[i] = None
            self.count -= 1
            j = i

            while True:
                i = (i + 1) % self.size
                pair = self.table[i]
                if pair == None:
                    return True

                k = self._hash(pair[0])
                
                if not ((j < k and k <= i) or (i < j and ((j < k) or k <= i))):
                    self.table[j] = self.table[i]
                    break

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        return [pair[0] for pair in self.table if pair is not None]

    def values(self): 
        return [pair[1] for pair in self.table if pair is not None]

    def _hash(self, value) -> int:
        return hash(value) % self.size

    def _resize(self, new_size):
        curr_table = self.table
        self.size = new_size
        self.count = 0
        self.table = [None for _ in range(self.size)]

        for pair in curr_table:
            if pair is not None:
                self.set(pair[0], pair[1])
        return

    def _find_index(self, key):
        i = self._hash(key)
        pair = self.table[i]
        while pair is not None:
            if pair[0] == key:
                return i
            i = (i + 1) % self.size
            pair = self.table[i]

        return -1


d = LinearProbingHashTable()

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
