import numpy as np

class CSRMatIterator:
	def __init__(self, csrMat):
		self._nRow = -1
		self._csrMat = csrMat

	def __iter__(self):
		return self

	def __next__(self):
		self._nRow += 1
		if self._nRow < self._csrMat.shape[0]:
			return self._csrMat._dataXcolIndex[
				self._csrMat._rowIndex[self._nRow]:
				self._csrMat._rowIndex[self._nRow+1]
			]
		else:
			raise StopIteration
		

class CSRMat:
	def __init__(self, matrix, null=None):
		if not isinstance(matrix, (list, tuple)):
			raise TypeError("matrix is not a list nor a tuple")

		rowIndexEnd = 0
		x = 0
		auxDataXcolIndex = []
		auxRowIndex = []
		lenRow = 0

		for row in matrix:
			if not isinstance(row, (list, tuple)):
				raise TypeError("matrix is not a list nor a tuple")
			if len(row) > lenRow:
				lenRow = len(row)

			x = 0
			auxRowIndex.append(rowIndexEnd)

			for mem in row:
				if mem != null:
					auxDataXcolIndex.append([mem, x])
					rowIndexEnd += 1
				x += 1

		auxRowIndex.append(rowIndexEnd)


		self.null = null
		self.shape = (len(matrix), lenRow)
		self._dataXcolIndex = np.array(auxDataXcolIndex, dtype=object)
		self._rowIndex = np.array(auxRowIndex, dtype=object)

	def __getitem__(self, indices):
		if isinstance(indices, list):
			return np.array([self[i] for i in indices])
		elif not isinstance(indices, tuple):
			if not isinstance(indices, int):
				raise IndexError(
					"only integers and list are valid indices"
				)
			elif indices >= self.shape[0]:
				raise IndexError(
					"SparseMatrix index out of range"
				)
			else:
				return self._dataXcolIndex[
					self._rowIndex[indices]:self._rowIndex[indices+1]
				]
		elif len(indices) == 1:
			return self[indices[0]]
		elif len(indices) == 2:
			if isinstance(indices[1], int):
				if indices[1] >= self.shape[1]:
					raise IndexError(
						"SparseMatrix index out of range"
					)
				elif isinstance(indices[0], list):
					return np.array([self[y,indices[1]] for y in indices[0]])
				elif isinstance(indices[0], int):
					for mem,j in self[indices[0]]:
						if j == indices[1]:
							return mem
						elif j > indices[1]:
							break
					return self.null
				else:
					raise IndexError(
						"only integers and list are valid indices"
					)
			elif isinstance(indices[1], list):
				return np.array([self[indices[0], x] for x in indices[1]])
			else:
				raise IndexError("only integers and list are valid indices")
		else:
			raise IndexError("IndexError: too many indices for SparseMatrix")

	def __iter__(self):
		return CSRMatIterator(self)
