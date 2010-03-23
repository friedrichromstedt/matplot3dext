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

# Developed since: Mar 22

import numpy
import matplot3dext.objects.point

"""Subdivisions describe an subdivision task.  They contain a coordinate
in object-specific base and support projection operations.  They store also
the renders to apply to the newly created objects."""


class Subdivion:
	"""Subdivisions describe an subdivision task.  They contain a coordinate
	in object-specific base and support projection operations.  They store 
	also the renders to apply to the newly created objects. 
	
	This is the base class for all subdivisions."""

	def __init__(self, 
			coordinates,
			base_point, end_points,
			renderers_point, renderers_line, renderers_face,
			tol):
		"""COORDINATE is measured from BASE_POINT towards the END_POINTS list.  
		All points are matplot3dext.objects.point.Point instances.  A 
		coordinate is zero when it endpoint component is zero, and 1.0 when 
		its endpoint component is 1.0.  TOL is the coordinate-absolute 
		tolerance used when deciding whether a coordinate is 0 or 1.
		
		RENDERERS_POINT, RENDERERS_LINE, RENDERERS_FACE are sets of 
		renderes to apply."""
		
		self.coordinates = numpy.asarray(coordinates)
		self.base_point = base_point
		self.end_points = end_points

		# Initialise attributes ...

		self.tol = tol

		self.ndim = len(self.coordinates)
		assert(self.ndim == len(self.end_points))

		self.renderers_point = renderers_point
		self.renderers_line = renderers_line
		self.renderers_face = renderers_face

	#
	# Coordinate checking methods ...
	#

	def coordinate_is_zero(self, coordinate_idx):
		"""Checks whether coordinate COORDINATE_IDX is zero."""

		return abs(self.coordinates[coordinate_idx]) <= self.tol

	def coordinate_is_unity(self, coordinate_idx):
		"""Checks whether coordinate COORDINATE_IDX is unity."""

		return abs(self.coordinates[coordinate_idx] - 1) <= self.tol

	def basepoint_neglectable(self):
		"""Checks whether the base point can be neglected."""

		return abs(self.coordinates.sum() - 1) <= self.tol

	#
	# Point resolving method ...
	#

	def get_subdivision_point(self):
		"""Returns a new point with the renderers set."""

		base_position = self.base_point.position

		translation_matrix = \
				numpy.asarray([end_point.position - base_position for \
						end_point in self.end_points])
		
		new_point_translation = \
				numpy.dot(translation_matrix, self.coordinates)

		new_point_position = base_position + new_point_translation

		new_point = matplot3dext.objects.point.Point(new_point_position,
				renderers_point = self.renderers_point,
				renderers_line = self.renderers_line,
				renderers_face = self.renderers_face)

	#
	# Coordinate neglection methods ...
	#

	def neglect_coordinte(self, coordinate_idx, new_base_point):
		"""Returns a new Subdivision, neglecting coordinate COORDINATE_IDX."""

		# That's easy, simply neglect the according COORDINATE_IDX ...
	
		new_coordinates = numpy.hstack((
				self.coordinates[:coordinate_idx],
				self.coordinates[coordinate_idx + 1:]))
		
		new_end_points = \
				self.end_points[:coordinate_idx] + \
				self.end_points[coordinate_idx + 1:]

		return Subdivision(
				coordinates = new_coordinates,
				base_point = new_base_point,
				end_points = new_end_points,
				renderers_point = self.renderers_point,
				renderers_line = self.renderers_line,
				renderers_face = self.renderers_face,
				tol = self.tol)
	
	def neglect_base_point(self):
		"""Returns a new Subdivision, neglecting the .base_point."""

		# Using the last end_point as new base_point ...

		new_coordinates = self.coordinates[:-1]

		new_base_point = self.end_points[-1]

		new_end_points = self.end_points[:-1]

		return Subdivision(
				coordinates = new_coordinates,
				base_point = new_base_point,
				end_points = new_end_points,
				renderers_point = self.renderers_point,
				renderers_line = self.renderers_line,
				renderers_face = self.renderers_face,
				tol = self.tol)

	#
	# Reduce method ...
	#

	def reduce(self):
		"""Reduce as far as possible, then find the object to subdivide,
		and call its .subdivide method."""

		# Check for negnectable end_points ...

		for coordinate_idx in xrange(self.ndim):
			if self.coordinate_is_zero(coordinate_idx):
				# Use self.base_point as new_base_point.
				reduced = self.neglect_coordinate(coordinate_idx,
						new_base_point = self.base_point)
				return reduced.reduce()
			elif self.coordinate_is_unity(coordinate_idx)
				# Use the end_point as new_base_point.
				reduced = self.neglect_coordinate(coordinate_idx,
						new_base_point = self.end_points[coordinate_idx])
				return reduced.reduce()

		# The Subdivision cannot be further reduced ...

		if self.ndim == 0:
			self.base_point.subdivide(self)

		elif self.ndim == 1:
			# Find the connecting line.
			line, = self.base_point.attached_lines & \
					self.end_points[0].attached_lines

			line.subdivide(self)

		elif self.ndim == 2:
			# Find the common face.
			line1, line2, line3 = \
					self.base_point.attached_lines & \
					self.end_points[0].attached_lines & \
					self.end_points[1].attached_lines

			face, = \
					line1.attached_faces & \
					line2.attached_faces & \
					line3.attached_faces

			face.subdivide(self)

		elif self.ndim == 3:
			# Find the common tetrahedron.

			line1, line2, line3, line4, line5, line6 = \
					self.base_point.attached_lines & \
					self.end_points[0].attached_lines & \
					self.end_points[1].attached_lines & \
					self.end_points[2].attached_lines

			face1, face2, face3, face4 = \
					line1.attached_faces & \
					line2.attached_faces & \
					line3.attached_faces & \
					line4.attached_faces & \
					line5.attached_faces & \
					line6.attached_faces

			tetrahedron, = \
					face1.attached_tetrahedra & \
					face2.attached_tetrahedra & \
					face3.attached_tetrahedra & \
					face4.attached_tetrahedra

			tetrahedron.subdivide(self)

		else:
			raise RuntimError("Subdivision of > 3-dimensional object.")

	# 
	# Base point switching ...
	#
	
	def switch_basepoint(self, new_base_point):
		"""Switch the base_point in-place to NEW_BASEPOINT."""

		if new_base_point is not self.base_point:
			end_point_idx = self.end_points.index(new_base_point)

			self.coordinates[end_point_idx] *= -1

			self.end_points[end_point_idx] = self.base_point

			self.base_point = new_base_point

		# else:  Nothing to do.
