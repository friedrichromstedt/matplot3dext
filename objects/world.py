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

import matplot3dext.objects.point
import matplot3dext.objects.line
import matplot3dext.objects.face
import matplot3dext.objects.tetrahedron

"""matplot3dext world(s)."""


class World:
	"""matplot3dext world class.  Holds all Points, Lines, Faces, and
	Tetrahedrons of a world."""

	def __init__(self, 
			xlim, ylim, zlim,
			renderers_point, renderers_line, renderers_face):
		"""Initialise the world covered to XLIM = (xstart, xstop), YLIM and 
		ZLIM.  The default renderers are RENDERERS_POINT, RENDERERS_LINE, and
		RENDERERS_FACE."""
		
		# Initialise the attributes ...

		self.points = []
		self.lines = []
		self.faces = []
		self.tetrahedra = []

		# Initialise the cube ...

		(x1, x2) = xlim
		(y1, y2) = ylim
		(z1, z2) = zlim

		# Create the points of the cube.
		point111 = matplot3dext.objects.point.Point(
				[x1, y1, z1],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point112 = matplot3dext.objects.point.Point(
				[x1, y1, z2],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point121 = matplot3dext.objects.point.Point(
				[x1, y2, z1],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point122 = matplot3dext.objects.point.Point(
				[x1, y2, z2],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point211 = matplot3dext.objects.point.Point(
				[x2, y1, z1],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point212 = matplot3dext.objects.point.Point(
				[x2, y1, z2],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point221 = matplot3dext.objects.point.Point(
				[x2, y2, z1],
				renderers_point, renderers_line, renderers_face,
				world = self)

		point222 = matplot3dext.objects.point.Point(
				[x2, y2, z2],
				renderers_point, renderers_line, renderers_face,
				world = self)

		# Create the connecting lines of the cube.
		#
		# You should make a sketch now.
		A = point111
		B = point211
		C = point121
		D = point112
		E = point122
		F = point212
		G = point221
		H = point222

		AB = matplot3dext.objects.line.Line(A, B, world = self)
		AC = matplot3dext.objects.line.Line(A, C, world = self)
		AD = matplot3dext.objects.line.Line(A, D, world = self)
		AE = matplot3dext.objects.line.Line(A, E, world = self)
		AF = matplot3dext.objects.line.Line(A, F, world = self)
		AG = matplot3dext.objects.line.Line(A, G, world = self)
		BF = matplot3dext.objects.line.Line(B, F, world = self)
		BG = matplot3dext.objects.line.Line(B, G, world = self)
		CE = matplot3dext.objects.line.Line(C, E, world = self)
		CG = matplot3dext.objects.line.Line(C, G, world = self)
		DE = matplot3dext.objects.line.Line(D, E, world = self)
		DF = matplot3dext.objects.line.Line(D, F, world = self)
		EF = matplot3dext.objects.line.Line(E, F, world = self)
		EG = matplot3dext.objects.line.Line(E, G, world = self)
		EH = matplot3dext.objects.line.Line(E, H, world = self)
		FG = matplot3dext.objects.line.Line(F, G, world = self)
		FH = matplot3dext.objects.line.Line(F, H, world = self)
		GH = matplot3dext.objects.line.Line(G, H, world = self)

		# Create the faces of the surface and in the interior of the cube.
		ABF = matplot3dext.objects.face.Face(AB, AF, BF, world = self)
		ABG = matplot3dext.objects.face.Face(AB, AG, BG, world = self)
		ACE = matplot3dext.objects.face.Face(AC, AE, CE, world = self)
		ACG = matplot3dext.objects.face.Face(AC, AG, CG, world = self)
		ADE = matplot3dext.objects.face.Face(AD, AE, DE, world = self)
		ADF = matplot3dext.objects.face.Face(AD, AF, DF, world = self)
		AEF = matplot3dext.objects.face.Face(AE, AF, EF, world = self)
		AEG = matplot3dext.objects.face.Face(AE, AG, EG, world = self)
		AFG = matplot3dext.objects.face.Face(AF, AG, FG, world = self)
		BFG = matplot3dext.objects.face.Face(BF, BG, FG, world = self)
		CEG = matplot3dext.objects.face.Face(CE, CG, EG, world = self)
		DEF = matplot3dext.objects.face.Face(DE, DF, EF, world = self)
		EFG = matplot3dext.objects.face.Face(EF, EG, FG, world = self)
		EFH = matplot3dext.objects.face.Face(EF, EH, FH, world = self)
		EGH = matplot3dext.objects.face.Face(EG, EH, GH, world = self)
		FGH = matplot3dext.objects.face.Face(FG, FH, GH, world = self)

		# Create the tetrahedra between the surfaces.
		ABGF = matplot3dext.objects.tetrahedron.Tetrehedron(
				ABG, ABF, AGF, BGF, world = self)
		ACEG = matplot3dext.objects.tetrahedron.Tetrahedron(
				ACE, ACG, AEG, CEG, world = self)
		ADEF = matplot3dext.objects.tetrahedron.Tetrahedron(
				ADE, ADF, AEF, DEF, world = self)
		AEFG = matplot3dext.objects.tetrahedron.Tetrahedron(
				AEF, AEG, AFG, EFG, world = self)
		EFGH = matplot3dext.objects.tetrahedron.Tetrahedron(
				EFG, EFH, EGH, FGH, world = self)

	#
	# World content management ...
	#

	def add_point(self, point):
		self.points.append(point)

	def remove_point(self, point):
		self.points.remove(point)

	def add_line(self, line):
		self.lines.append(line)
	
	def remove_line(self, line):
		self.lines.remove(line)

	def add_face(self, face):
		self.faces.append(face)

	def remove_face(self, face):
		self.faces.remove(face)
	
	def add_tetrahedron(self, tetrahedron):
		self.tetrahedra.append(tetrahedron)

	def remove_tetrahedron(self, tetrahedron):
		self.tetrahedra.remove(tetrahedron)
