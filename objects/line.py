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

import matplot3dext.objects.face

"""matplot3dext lines."""


class Line:
	"""matplot3dext lines.  Find their line and face renderers from the 
	points used for their creation."""

	def __init__(self, point1, point2, world):
		"""Create new line between POINT1 and POINT2.  Load renderers from
		the points.  POINT1 and POINT2 are matplot3dext.objects.point.Point
		instances."""

		# Initialise attributes ...

		self.attached_faces = set()
		self.attached_points = set([point1, point2])

		# Attach to the points ...

		point1.attach_line(self)
		point2.attach_line(self)

		# Initialise the renderers ...
		
		self.update_renderers_from_points()

		# Calculate visibility ...

		self.visible = True
		for point in self.attached_points:
			self.visible = self.visible and point.visible

		world.add_line(self)

		# Check if we intersect some nearby face ...

		starting_point = None

		if point1.visible:
			starting_point = point1
			target_point = point2

		elif point2.visible:
			starting_point = point2
			target_point = point1

		if starting_point is not None:
			# Check if we intersect with any of the opposite faces of the 
			# tetrahedra attached to {starting_point}.  We exclude the
			# tetrahedra attached to {target_point}, to avoid checking 
			# against adjacent faces in the last step.

			for tetrahedron in \
					starting_point.attached_tetrahedra - \
					target_point.attached_tetrahedra:
				point1, point2, point3 = tetrahedron.attached_points - \
						set([starting_point])
				opposite_face, = \
						point1.attached_faces & \
						point2.attached_faces & \
						point3.attached_faces

				intersection = world.intersect(self, opposite_face)
				if intersection is not None:
					# This will destroy self by subdivision:
					intersection.intersect()

					return

		else:
			# This means that all of our two points are invisible, it follows 
			# that we are completetly outside world.  Then, check with /all/ 
			# faces of the world.

			for face in world.faces:
				intersection = world.intersect(self, face)
				if intersection is not None:
					# We will be destroyed by this by subdivision:
					intersection.intersect()

					return

			# If we had no intersection with the existing world, we are
			# completely obsolete:
			self.destroy()

	def update_renderers_from_points(self):
		"""Loads the renderers from the points, and updates faces attached."""

		point1, point2 = self.attached_points

		self.renderers_line = \
				point1.renderers_line & point2.renderers_line

		self.renderers_face = \
				point1.renderers_face & point2.renderers_face

		for face in self.attached_faces:
			face.update_renderers_from_lines()

	#
	# Connection methods ...
	#

	def attach_face(self, face):
		"""Attach Face FACE.  Do not update the face's renderers.  Assume
		the lines attached to the face & to .attached_points are already
		attached to self.  Do not attach the FACE to the Points attached to
		self."""

		self.attached_faces.add(face)

	def detach_face(self, face):
		"""Detach Face FACE.  Do not detach the face from .attached_points
		(when called from the FACE's .destroy(), this would detach the face
		two times from each of the .attached_points, because there are always 
		two Lines attached to FACE and to some Point)."""
		
		self.attached_faces.remove(face)

	#
	# Subdivision methods ...
	#

	def subdivide(self, subdivision, new_point):
		"""Perform a subdivision task on this Line."""

		assert(subdivision.ndim == 1)

		point1, point2 = self.attached_points

		line1 = Line(point1, new_point)
		line2 = Line(point2, new_point)

		self.replace_by([line1, line2], subdivision.world)

		return new_point

	def replace_by(self, new_lines, world):
		"""Replace this Line by Line instances NEW_LINES."""
	
		# For all attached faces, subdivide them ...
		#
		# We must 1. subdivide and 2. .destroy(), and not vice versa, because
		# destroying self first, would destroy also all Faces attached.

		for face in self.attached_faces:
			
			# Find the extern lines.
			ext_line1, ext_line2 = face.attached_lines - set([self])

			# Find the extern point.
			ext_point, = ext_line1.attached_points & ext_line2.attached_points
			
			# Find the new intern points.
			int_points = set()
			for new_line in new_lines:
				int_points |= new_line.attached_points - self.attached_points

			# Create the new face edges.
			for int_point in int_points:
				# Nowhere stored except than in connectivity:
				tmp_line = Line(ext_point, int_point)

			# Create the new faces.
			new_faces = []
			for new_line in new_lines:
				# Find the two bounding edges:
				point1, point2 = new_line.attached_points
				ext_edge1, = point1.attached_lines & ext_point.attached_lines
				ext_edge2, = point2.attached_lines & ext_point.attached_lines

				# Create the new face:
				new_faces.append(matplot3dext.objects.face.Face(
					new_line, ext_edge1, ext_edge2))

			# Replace the existing face with the new faces.
			face.replace_by(new_faces, world)

		self.destroy(world)
		
	#
	# Freeing memory ...
	#
	 
	def destroy(self):
		"""Resolve reference loops.  Destroy all attached faces.  Detach the 
		line from all attached points."""
		
		for point in self.attached_points:
			point.detach_line(self)

		for face in self.attached_faces:
			face.destroy()

		self.attached_points = set()
		self.attached_faces = set()

		world.remove_line(self)
