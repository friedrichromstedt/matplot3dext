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

import matplot3dext.objects.line
import matplot3dext.objects.face

"""matplot3dext tetrahedra."""


class Tetrahedron:
	"""matplot3dext tetrahedra."""

	def __init__(self, face1, face2, face3, face4):
		"""Create new tetrahedron between FACE1..4.  Extracts the lines and
		the points from the faces too.  The faces are matplot3dext.objects.\
		face.Face instances."""

		self.attached_faces = set([face1, face2, face3, face4])

	#
	# Subdivision methods ...
	#
	
	def subdivide(self, subdivision):
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

		# Create the new point.
		new_point = subdivision.get_subdivision_point()
		
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
				new_tetrahedron3, new_tetrahedron4])

	def replace_by(self, new_tetrahedra):
		"""Replace this Tetrahdedron by Tetrahedron instances 
		NEW_TETRAHEDRA."""
		
		# All done.  Just destroy self.

		self.destroy()

	#
	# Freeing memory ...
	#

	def destroy(self):
		"""Resolve the reference loops.  Detach the Tetrahedron from all 
		Faces attached."""
		
		for face in self.attached_faces:
			face.detach_tetrahedron(self)

		self.attached_faces = set()
