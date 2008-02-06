import operator

#n-dimensional array class. more than 2 dimensions not tested
class array:
	def __init__(self, *size):
		self.size = size
		self.array = [0 for i in xrange(reduce(operator.mul, size))]
	
	def ndim2flat(self, key):
		if len(key) != len(self.size):
			raise TypeError()
		for i, n in enumerate(key):
			if n >= self.size[i] or n < 0:
				raise IndexError()

		index = key[0]
		for i in range(1, len(key)):
			index += key[i] * reduce(operator.mul, self.size[:i])
		return index
	
	def __getitem__(self, key):
		index = self.ndim2flat(key)
		return self.array[index]

	def __setitem__(self, key, value):
		index = self.ndim2flat(key)
		self.array[index] = value
