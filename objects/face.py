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

import matplot3dext.objects.line
import matplot3dext.objects.tetrahedron

"""matplot3dext faces."""


class Face:
	"""matplot3dext faces.  Find their face renderers from the lines used for
	their creation."""

	def __init__(self, line1, line2, line3, world):
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

		# Attach to the points ...

		for point in self.attached_points:
			point.attach_face(self)

		# Initialise the renderers ...

		self.update_renderers_from_lines()

		# Calculate visibility ...

		self.visible = True
		for line in self.attached_lines:
			self.visible = self.visible and line.visible

		world.add_face(self)

		# Check if we intersect some nearby line ...

		# Check if we can accelerate the process.
		accelerated = False

		if point1.visible:
			accelerated = True
			starting_point = point1
			excluded_lines = point2.attached_lines + point3.attached_lines

		elif point2.visible:
			accelerated = True
			starting_point = point2
			excluded_lines = point1.attached_lines + point3.attached_lines

		elif point3.visible:
			accelerated = True
			starting_point = point3
			excluded_lines = point1.attached_lines + point2.attached_lines

		if accelerated:
			# We can check in the nearby neighbourhood.

			for face in starting_point.attached_faces:
				opposite_line, = face.attached_lines - \
						starting_point.attached_lines

				if opposite_line in excluded_lines:
					continue

				intersection = world.intersect(self, opposite_line)
				
				if intersection is not None:
					# This will destroy self:
					intersection.intersect()

					return

		else:
			# We must check against /all/ lines in the world.

			for line in world.lines:
				intersection = world.intersect(self, line)

				if intersection is not None:
					# This will destroy self:
					intersection.intersect()

					return
			
			# We had no intersection, hence we are obsolete.
			self.destroy()

	def update_renderers_from_lines(self):
		"""Loads the renderers from the lines."""

		line1, line2, line3 = self.attached_lines
		
		self.renderers_face = \
				line1.renderers_face & \
				line2.renderers_face & \
				line3.renderers_face

	#
	# Connection methods ...
	#

	def attach_tetrahedron(self, tetrahedron):
		"""Attach Tetrahedron TETRAHEDRON.  Do not attach the TETREHEDRON to
		any of the objects attached to this Face.  Assume that the common
		Faces and Lines of self and the TETRAHEDRON are already attached to
		the Face."""

		self.attached_tetrahedra.add(tetrahedron)

	def detach_tetrahedron(self, tetrahedron):
		"""Remove Tetrahedron TETRAHEDRON.  Do not detach the TETREHEDRON from
		any of the objects attached to this Face."""

		self.attached_tetrahedra.remove(tetrahedron)

	# 
	# Subdivision methods ...
	#

	def subdivide(self, subdivision, new_point):
		"""Perform a subdivison task on this Face."""

		assert(subdivision.ndim == 2)

		# Find the attached lines.
		line1, line2, line3 = self.attached_lines

		# Find the attached points, and be able to associate them with the
		# lines.
		point23, = line2.attached_points & line3.attached_points
		point13, = line1.attached_points & line3.attached_points
		point12, = line1.attached_points & line2.attached_points
		
		new_line23 = matplot3dext.objects.line.Line(point23, new_point)
		new_line13 = matplot3dext.objects.line.Line(point13, new_point)
		new_line12 = matplot3dext.objects.line.Line(point12, new_point)

		new_face1 = Face(line1, new_line13, new_line12)
		new_face2 = Face(line2, new_line23, new_line12)
		new_face3 = Face(line3, new_line13, new_line23)

		self.replace_by([new_face1, new_face2, new_face3], subdivison.world)

		return new_point

	def replace_by(self, new_faces, world):
		"""Replace this Face by Face instances NEW_FACES."""

		# For all attached tetrahetra, subdivide them ...

		for tetrahedron in self.attached_tetrahedra:

			# Find the extern faces.
			ext_face1, ext_face2, ext_face3 = \
					tetrahedron.attached_faces - set([self])
			
			# Find the extern point.
			ext_point, = \
					ext_face1.attached_points & \
					ext_face2.attached_points & \
					ext_face3.attached_points

			# Find the new intern lines.
			int_lines = set()
			for new_face in new_faces:
				int_lines |= new_face.attached_lines - self.attached_lines

			# Find the new intern points.
			int_points = set()
			for int_line in int_lines:
				int_points |= int_line.attached_points - self.attached_points

			# Create the new extern lines.
			for int_point in int_points:
				# Stored in connectivity:
				tmp_line = matplot3dext.objects.line.\
						Line(int_point, ext_point)

			# Create the new extern faces.
			for int_line in int_lines:
				# Find the two bounding edges:
				int_point1, int_point2 = int_line.attached_points
				ext_edge1, = \
						int_point1.attached_lines & \
						ext_point.attached_lines
				ext_edge2, = \
						int_point2.attached_lines & \
						ext_point.attached_lines

				# Create the new face, stored in connectivity:
				tmp_face = Face(int_line, ext_edge1, ext_edge2)

			# Create new tetrahedra.
			new_tetrahedra = []
			for new_face in new_faces:
				# Find the three bounding faces:
				line1, line2, line3 = new_face.attached_lines
				ext_face1, = line1.attached_faces & ext_point.attached_faces
				ext_face2, = line2.attached_faces & ext_point.attached_faces
				ext_face3, = line3.attached_faces & ext_point.attached_faces

				# Add the tetrahedron:
				new_tetrahedra.append(matplot3dext.objects.tetrahedra.\
						Tetrahedron(new_face, 
							ext_face1, ext_face2, ext_face3))

			# Replace the existing tetrahedron with the new ones.
			tetrahedron.replace_by(new_tetrahedra, world)

		self.destroy(world)
	
	#
	# Freeing memory ...
	#

	def destroy(self, world):
		"""Resolves references loops.  Detach the Face from all Lines
		attached.  Detach the Face from all Points attached."""
			
		for line in self.attached_lines:
			line.detach_face(self)
	
		for point in self.attached_points:
			point.detach_face(self)

		self.attached_lines = set()
		self.attached_points = set()

		world.remove_face(self)
