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

# Last changed: 2010 Mar 22
# Developed since: Mar 2010

import numpy
import matplot3dext.norms.interface

"""Normalisation of mplot3dext points onto the range [0.0, 1.0].  Used to 
retrieve values for colormapping."""


class ProjectionPointNorm(matplot3dext.norms.interface.Norm):
	"""Normalises points by projecting their position onto a 3d direction.  
	The normalisation result is the same on all planes perpendicular to the 
	direction given.  Limits are set by two 3-vectors, for both the resulting 
	scalar level can be set.  This means, one specifies via the two points in 
	fact two planes through the points with the direction as normal."""

	def __init__(self, 
			direction, 
			base0, base1, 
			norm0 = None, norm1 = None):
		"""DIRECTION is a 3-vector giving the normalisation direction.  BASE0
		specifies the plane of normalisation result NORM0, BASE1 the plane of
		result NORM1.  NORM0 defaults to 0.0, NORM1 to 1.0."""
	
		if norm0 is None:
			norm0 = 0.0
		if norm1 is None:
			norm1 = 1.0

		# Store initial values.
		self.norm0 = norm0
		self.norm1 = norm1
		self.direction = numpy.asarray(direction)

		# Calculate projection parameters.
		self.set_base(base0, base1, norm0, norm1)

	def set_base(self, base0, base1, norm0 = None, norm1 = None):
		"""BASE0 specifies the plane of normalisation result NORM0, BASE1 the 
		plane of result NORM1.  If NORM0 or NORM1 are not given, they default 
		to the current value.  The direction is unchanged."""
	
		if norm0 is None:
			norm0 = self.norm0
		if norm1 is None:
			norm1 = self.norm1

		# Store the points ...

		self.base0 = numpy.asarray(base0)
		self.base1 = numpy.asarray(base1)

		self.norm0 = norm0
		self.norm1 = norm1

		# Project the points onto .direction ...

		self.projection0 = numpy.dot(self.direction, self.base0)
		self.projection1 = numpy.dot(self.direction, self.base1)
		
		self.projection_delta = self.projection1 - self.projection0

		# Set state indicator ...

		if self.projection_delta == 0:
			# No scaling possible, linear slope is \infty.
			self.state = 'impossible'
		else:
			self.state = 'ok'

	def _normalise(self, point):
		"""Project the matplot3dext point POINT onto .direction and scale 
		according to the base set."""

		if self.state == 'impossible':
			# No scaling possible.
			return 0.0

		else:
			projection = numpy.dot(self.direction, point.position)

			# Map [.projection0, .projection1] onto [.norm0, .norm1].
			normalised = \
					self.norm0 * (self.projection1 - projection) / \
							self.projection_delta + \
					self.norm1 * (projection - self.projection0) / \
							self.projection_delta

			return normalised

	def set_direction(self, direction):
		"""DIRECTION is a 3-vector giving the normalisation direction."""

		self.direction = numpy.asarray(direction)
		
		# Update the projection parameters ...

		self.set_base(self.base0, self.base1)
