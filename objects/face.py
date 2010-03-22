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
import matplot3dext.objects.tetrahedron

"""matplot3dext faces."""


class Face:
	"""matplot3dext faces.  Find their face renderers from the lines used for
	their creation."""

	def __init__(self, line1, line2, line3):
		"""Create new face between LINE1, LINE2, and LINE3.  Loads renderers
		from the lines.  Extracts the points from the lines too.  The lines 
		are matplot3dext.objects.line.Line instances."""

		self.attached_tetrahedra = set()

		self.attached_lines = set([line1, line2, line3])

		# Find the points ...

		self.attached_points = set()
		for line in self.attached_lines:
			self.attached_points |= line.attached_points

		# Attach to the lines ...

		for line in self.attached_lines:
			line.attach_face(self)

		# Initialise the renderers ...

		self.update_renderers_from_lines()

	def update_renderers_from_lines(self):
		"""Loads the renderers from the lines."""

		self.renderers_face = set()
		for line in self.attached_lines:
			self.renderers_face |= line.renderers_face

	#
	# Connection methods ...
	#

	def add_tetrahedron(self, tetrahedron):
		"""Attach Tetrahedron TETRAHEDRON."""

		self.attached_tetrahedra.add(tetrahedron)

	def remove_tetrahedron(self, tetrahedron):
		"""Remove Tetrahedron TETRAHEDRON."""

		self.attached_tetrahedra.remove(tetrahedron)

	# 
	# Subdivision methods ...
	#

	def subdivide(self, subdivision):
		"""Perform a subdivison task on this Face."""

		assert(subdivision.ndim == 2)

		# Find the attached lines.
		line1, line2, line3 = self.attached_lines

		# Find the attached points, and be able to associate them with the
		# lines.
		point23, = line1.attached_points & line2.attached_points
		point13, = line1.attached_points & line3.attached_points
		point12, = line2.attached_points & line3.attached_points

		new_point = subdivision.get_subdivision_point()
		
		new_line23 = matplot3dext.objects.line.Line(point23, new_point)
		new_line13 = matplot3dext.objects.line.Line(point13, new_point)
		new_line12 = matplot3dext.objects.line.Line(point12, new_point)

		new_face1 = Face(line1, new_line13, new_line12)
		new_face2 = Face(line2, new_line23, new_line12)
		new_face3 = Face(line3, new_line13, new_line23)

		self.replace_by([new_face1, new_face2, new_face3])

	def replace_by(self, new_faces):
		"""Replace this Face by Face instances NEW_FACES."""

		# For all attached tetrahetra, subdivide them ...

		for tetrahedron in self.attached_tetrahedra:

			# Find the surrounding faces.
			face1, face2, face3 = tetrahedron.attached_faces - set([self])
			
			# Create new tetrahedra.
			new_tetrahedra = []
			for new_face in new_faces:
				new_tetrahedra.append(matplot3dext.object.tetrahedra.\
						Tetrahedron(face1, face2, face3, new_face)

			# Replace the existing tetrahedron with the new ones.
			tetrahedron.replace_by(new_tetrahedra)

		self.destroy()
	
	#
	# Freeing memory ...
	#

	def destroy(self):
		"""Resolves references loops."""

		del self.attached_lines
		del self.attached_points
