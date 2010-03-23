# Copyright (c) 2010 Friedrich Romstedt <www.friedrichromstedt.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""matplot3dext Intersection objects."""


class Intersection:
	"""Intersection objects hold two matplot3dext.objects.subdivision.\
	Subdivision objects.  They reduce them, and call the .subdivide() 
	methods in the appropriate order."""

	def __init__(self, subdivision1, subdivision2):
		"""SUBDIVISION1 and SUBDIVISION2 are Subdivision instances."""

		self.subdivision1 = subdivision1.reduce()
		self.subdivision2 = subdivision2.reduce()

		if self.subdivision1.ndim == 0 and self.subdivision2.ndim == 0:
			raise RuntimeError("Cannot intersect two Subdivisions which reduce both to ndim = 0.")

	def intersect(self):
		"""Subdivide 0-dimensional subdivision preferentially, and use the
		resulting subdivision point as subdivision point for the second
		subdivision."""

		if self.subdivison2.ndim == 1:
			# Reverse order.

			subdivision_point = self.subdivision2.subdivide()
			self.subdivision1.subdivide(subdivision_point)

		else:
			# Normal order.

			subdivision_point = self.subdivision1.subdivide()
			self.subdivision2.subdivide(subdivision_point)

	def exceute(self):
