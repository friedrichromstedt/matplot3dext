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

# Developed since: Mar 2010

"""Normalisation of objects onto the range [0.0, 1.0].  Used to retrieve
values for colormapping."""


class Norm:
	"""Abstract interface of Norms."""

	def _normalise(self, point):
		"""Internal function actually implementing normalisation, must return
		some real value, which will be clipped to [0.0, 1.0] by
		.normalise()."""

		raise NotImplementedError('Derived must overload.')

	def normalise(self, object):
		"""OBJECT is an object to be normalised.  Returns the object 
		normalised to the range [0.0, 1.0]."""

		# Retrieve the value (some real number).
		raw_normalised = self._normalise(point)

		# Clip the real number to [0.0, 1.0].
		if raw_normalised < 0:
			return 0.0
		elif raw_normalised > 1:
			return 1.0
		else:
			return raw_normalised
