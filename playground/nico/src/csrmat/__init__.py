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
			return (
				Node(self._csrMat._colIndex[cols], self._csrMat._data[cols])
				for cols in range(
					self._csrMat._rowIndex[self._nRow],
					self._csrMat._rowIndex[self._nRow+1]
				)
			)
		else:
			raise StopIteration
		

class Node(tuple):
	def __new__(cls, *args, **kwargs):
		if args:
			if len(args) == 1:
				self = tuple.__new__(cls, args[0])
				self._x = args[0][0]
				self._d = args[0][1]

			elif len(args) == 2:
				self = tuple.__new__(cls, args)
				self._x = args[0]
				self._d = args[1]
			else:
				raise ValueError("first x, then d")
		elif kwargs:
			if len(kwargs) == 2:
				if not "x" in kwargs:
					raise ValueError("missing x kwarg")
				if not "d" in kwargs:
					raise ValueError("missing d kwarg")

				self = tuple.__new__(cls, (kwargs["x"], kwargs["d"]))
				self._x = kwargs["x"]
				self._d = kwargs["d"]
			else:
				raise ValueError("missing x and d kwarg")
		else:
			raise ValueError("missing x and d")

		return self

	@property
	def x(self):
		return self._x

	@property
	def d(self):
		return self._d


class CSRMat:
	def __init__(self, matrix, none=None):
		if not isinstance(matrix, (list, tuple)):
			raise TypeError("matrix is not a list nor a tuple")

		rowIndexEnd = 0
		data = []
		colIndex = []
		rowIndex = []
		lenRow = 0

		for row in matrix:
			x = 0
			rowIndex.append(rowIndexEnd)

			if len(row) > lenRow:
				lenRow = len(row)

			for mem in row:
				if mem != none:
					colIndex.append(x)
					data.append(mem)
					rowIndexEnd += 1
				x += 1

		rowIndex.append(rowIndexEnd)


		self._none = none
		self._shape = (len(matrix), lenRow)
		self._data = tuple(data)
		self._colIndex = np.array(colIndex, dtype=np.uint16)
		self._rowIndex = np.array(rowIndex, dtype=np.uint16)

	@property
	def asdict(self):
		return {
			"data":		list(self._data),
			"colIndex":	list(self._colIndex),
			"rowIndex":	list(self._rowIndex),
		}

	@asdict.setter
	def asdict(self, value):
		try:
			self._data = tuple(value["data"])
			self._colIndex = np.array(value["colIndex"], dtype=np.uint16)
			self._rowIndex = np.array(value["rowIndex"], dtype=np.uint16)
		except Exception:
			raise ValueError(
				"expeted dict with 'data', 'colIndex', and 'rowIndex'"
			)

	@property
	def none(self):
		return self._none

	@property
	def shape(self):
		return self._shape

	def __getitem__(self, indices):

		if isinstance(indices, int):
			return tuple((
				Node(self._colIndex[cols], self._data[cols])
				for cols in range(
					self._rowIndex[indices],
					self._rowIndex[indices+1]
				)
			))

		elif isinstance(indices, tuple):
			if len(indices) == 1:
				return self[indices[0]]

			elif len(indices) == 2:
				cols = indices[1]
				rows = indices[0]

				if isinstance(rows, slice):
					start = rows.start if rows.start else 0
					stop = rows.stop if rows.stop else self._shape[1]
					step = rows.step if rows.step else 1

					rows = range(start, stop, step)

				elif rows == None or rows == Ellipsis:
					rows = range(self._shape[0])

				elif not hasattr(rows, "__iter__"):
					rows = (rows,)

				if isinstance(cols, int):
					if len(rows) == 1:
						for x, d in self[rows[0]]:
							if x == cols:
								return d
							elif x > cols:
								break

						return self._none
					else:
						return tuple((self[y, cols] for y in rows))

				elif isinstance(cols, slice):
					start = cols.start if cols.start else 0
					stop = cols.stop if cols.stop else self._shape[1]
					step = cols.step if cols.step else 1

					if len(rows) == 1:
						return tuple(
							(self[rows[0], x] for x in range(start, stop, step))
						)
					
					else:
						return tuple(
							(tuple(
								(self[y, x] for x in range(start, stop, step))
							) for y in rows)
						)

				elif cols == None or cols == Ellipsis:
					if len(rows) == 1:
						return tuple(
							(self[rows[0], x] for x in range(self._shape[1]))
						)
						
					else:
						return tuple(
							(tuple(
								(self[y, x] for x in range(self._shape[1]))
							) for y in rows)
						)
						

				elif hasattr(cols, "__iter__"):
					if len(rows) == 1:
						return tuple((self[rows[0], x] for x in cols))
					else:
						return tuple(tuple((self[y, x] for x in cols)) for y in rows)

				else:
					raise IndexError(
						"only integers, slices (`:`), ellipsis (`...`) and \
						integer iterables are valid indices"
					)
			else:
				raise IndexError("IndexError: too many indices for CSRMatrix")

		elif isinstance(indices, slice):
			start = indices.start if indices.start else 0
			stop = indices.stop if indices.stop else self._shape[0]
			step = indices.step if indices.step else 1

			return tuple((self[y] for y in range(start, stop, step)))

		elif indices == None or indices == Ellipsis:
			return tuple((self[y] for y in range(self._shape[0])))

		elif hasattr(indices, "__iter__"):
			return tuple((self[y] for y in indices))

		else:
			raise IndexError(
				"only integers, slices (`:`), ellipsis (`...`) and \
				integer iterables are valid indices"
			)

	def __iter__(self):
		return CSRMatIterator(self)

	def __str__(self):
		msg = "%s((\n"%type(self).__qualname__

		for row in self[:,:]:

			msg += "  %s\n"%str(tuple(row))

		msg += "))"

		return msg

	def __repr__(self):
		return "<"+str(self)+">"
