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

import numpy
import matplot3dext.objects.line
import matplot3dext.objects.face

"""matplot3dext tetrahedra."""


class Tetrahedron:
	"""matplot3dext tetrahedra."""

	def __init__(self, face1, face2, face3, face4, world):
		"""Create new tetrahedron between FACE1..4.  Extracts the lines and
		the points from the faces too.  The faces are matplot3dext.objects.\
		face.Face instances."""

		self.attached_faces = set([face1, face2, face3, face4])

		# Attach to the faces ...

		for face in self.attached_faces:
			face.attach_tetrahedron(self)

		# Attach to all points ...

		self.attached_points = set()
		for face in self.attached_faces:
			self.attached_points |= face.attached_points

		for point in self.attached_points:
			point.attach_tetrahedron(self)

		# Create the inverse coordinate matrix ...

		line1, line2, line3, line4, line5, line6 = \
				face1.attached_lines | face2.attached_lines | \
				face3.attached_lines | face4.attached_lines

		self.base_point, \
				self.end_point1, self.end_point2, self.end_point3 = \
				line1.attached_points | line2.attached_points | \
				line3.attached_points | line4.attached_points | \
				line5.attached_points | line6.attached_points

		self.end_points = [self.end_point1, self.end_point2, self.end_point3]

		self.base = self.base_point.position
		self.ends = numpy.asarray(
				[self.end_point1.position,
				 self.end_point2.position,
				 self.end_point3.position]) - self.base
		self.coordinate_matrix = numpy.linalg.inv(self.ends.T)

		world.add_tetrahedron(self)

	#
	# Subdivision methods ...
	#
	
	def subdivide(self, subdivision, new_point):
		"""Perform a subdivision task on this Tetrahedron."""

		assert(subdivision.ndim == 3)

		# Find the attached faces.
		face1, face2, face3, face4 = self.attached_faces

		# Find the attached lines, and be able to associate them with the
		# faces.
		line12, = face1.attached_lines & face2.attached_lines
		line13, = face1.attached_lines & face3.attached_lines
		line14, = face1.attached_lines & face4.attached_lines
		line23, = face2.attached_lines & face3.attached_lines
		line24, = face2.attached_lines & face4.attached_lines
		line34, = face3.attached_lines & face4.attached_lines

		# Find the attached points, and be able to associate them with the 
		# faces.
		point123, = line12.attached_points & line13.attached_points
		point124, = line12.attached_points & line14.attached_points
		point134, = line13.attached_points & line14.attached_points
		point234, = line23.attached_points & line24.attached_points

		# Create the new lines.
		new_line123 = matplot3dext.objects.line.Line(point123, new_point)
		new_line124 = matplot3dext.objects.line.Line(point124, new_point)
		new_line134 = matplot3dext.objects.line.Line(point134, new_point)
		new_line234 = matplot3dext.objects.line.Line(point234, new_point)

		# Create the new faces.
		new_face12 = matplot3dext.objects.face.Face(
				line12, new_line123, new_line124)
		new_face13 = matplot3dext.objects.face.Face(
				line13, new_line123, new_line134)
		new_face14 = matplot3dext.objects.face.Face(
				line14, new_line124, new_line134)
		new_face23 = matplot3dext.objects.face.Face(
				line23, new_line123, new_line234)
		new_face24 = matplot3dext.objects.face.Face(
				line24, new_line124, new_line234)
		new_face34 = matplot3dext.objects.face.Face(
				line34, new_line134, new_line234)

		# Create the new tetrahedra.
		#
		# Make a sketch to understand what's going on now.
		new_tetrahedron1 = Tetrahedron(
				face1, new_face12, new_face13, new_face14)
		new_tetrahedron2 = Tetrahedron(
				face2, new_face12, new_face23, new_face24)
		new_tetrahedron3 = Tetrahedron(
				face3, new_face13, new_face23, new_face34)
		new_tetrahedron4 = TetrahedroN(
				face4, new_face14, new_face24, new_face34)

		self.replace_by([new_tetrahdron1, new_tetrahedron2, 
				new_tetrahedron3, new_tetrahedron4], subdivision.world)

		return new_point

	def replace_by(self, new_tetrahedra, world):
		"""Replace this Tetrahdedron by Tetrahedron instances 
		NEW_TETRAHEDRA."""
		
		# All done.  Just destroy self.

		self.destroy(world)

	def inside(self, position):
		"""Returns the coordinates if 3-vector POSITION is inside, else 
		returns None."""

		delta = position - self.base
		
		coordinates = numpy.dot(self.coordinate_matrix, delta)

		if (coordinates >= 0).all() and (coordinates.sum() <= 1):
			return coordinates

	#
	# Freeing memory ...
	#

	def destroy(self, world):
		"""Resolve the reference loops.  Detach the Tetrahedron from all 
		Faces attached."""
		
		for face in self.attached_faces:
			face.detach_tetrahedron(self)

		for point in self.attached_points:
			point.detach_detrahedron(self)

		self.attached_faces = set()
		self.attached_points = set()

		# self.point1 etc. do not result in a reference loop.

		world.remove_tetrahedron(self)
