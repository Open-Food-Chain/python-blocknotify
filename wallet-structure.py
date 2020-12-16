class walletStructure:
	arrayOfArrays = []

	def add(self, data):
		self.arrayOfArrays = self.arrayOfArrays + [ data ]
	
	def find(self, name):
		for x in range(0, len(self.arrayOfArrays)):
			if name == self.arrayOfArrays[x][0]:
				return self.arrayOfArrays[x]
		
		return False

	def update(self, name, field, newData):
		for x in range(0, len(self.arrayOfArrays)):
			if name == self.arrayOfArrays[x][0]:
				self.arrayOfArrays[x][field] = newData
				return True

		return False


