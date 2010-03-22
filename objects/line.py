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

import matplot3dext.objects.face

"""matplot3dext lines."""


class Line:
	"""matplot3dext lines.  Find their line and face renderers from the 
	points used for their creation."""

	def __init__(self, point1, point2):
		"""Create new line between POINT1 and POINT2.  Load renderers from
		the points.  POINT1 and POINT2 are matplot3dext.objects.point.Point
		instances."""

		# Initialise attributes ...

		self.attached_faces = set()
		
		# Store point unresolved for face creation.
		self.attached_points = set([point1, point2])

		# Store points resolved for subdivision.
		self.point1 = point1
		self.point2 = point2

		# Attach to the points ...

		point1.attach_line(self)
		poitn2.attach_line(self)

		# Initialise the renderers ...
		
		self.update_renderers_from_points()

	def update_renderers_from_points(self):
		"""Loads the renderers from the points, and updates faces attached."""

		self.renderers_line = set()
		for point in self.attached_points:
			self.renderers_line |= point.renderers_line

		self.renderers_face = set()
		for point in self.attached_points:
			self.renderers_face |= point.renderers_face
		
		for face in self.attached_faces:
			face.update_renderers_from_lines()

	#
	# Connection methods ...
	#

	def add_face(self, face):
		"""Attach Face FACE.  Do not update the face's renderers."""

		self.attached_faces.add(face)

	def remove_face(self, face):
		"""Remove Face FACE."""

		self.attached_faces.remove(face)

	#
	# Subdivision methods ...
	#

	def subdivide(self, subdivision):
		"""Perform a subdivision task on this Line."""

		assert(subdivision.ndim == 1)

		point1, point2 = self.attached_points
		
		new_point = subdivision.get_subdivision_point()

		line1 = Line(point1, new_point)
		line2 = Line(point2, new_point)

		self.replace_by([line1, line2])

	def replace_by(self, new_lines):
		"""Replace this Line by Line instances NEW_LINES."""

		# For all attached faces, subdivide them ...

		for face in self.attached_faces:
			
			# Find the surrounding lines.
			line1, line2 = face.attached_lines - set([self])

			# Create the new faces.
			new_faces = []
			for new_line in new_lines:
				new_faces.append(matplot3dext.objects.face.Face(
					line1, line2, new_line)

			# Replace the existing face with the new faces.
			face.replace_by(new_faces)

		self.destroy()
		
	#
	# Freeing memory ...
	#
	 
	def destroy(self):
		"""Resolves reference loops.  Destroys all attached facest too."""
		
		for face in self.attached_faces:
			face.destroy()

		del self.attached_faced
		del self.attached_points
		del self.point1, self.point2
