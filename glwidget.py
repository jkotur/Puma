import pygtk
pygtk.require('2.0')
import gtk

import gtk.gtkgl

from OpenGL.GL import *
from OpenGL.GLU import *

class GLDrawingArea(gtk.DrawingArea, gtk.gtkgl.Widget):
	"""OpenGL drawing area for simple demo."""
	def __init__(self, glconfig):
		gtk.DrawingArea.__init__(self)

		# Set OpenGL-capability to the drawing area
		self.set_gl_capability(glconfig)

		# Connect the relevant signals.
		self.connect_after('realize',   self._on_realize)
		self.connect('configure_event', self._on_configure_event)
		self.connect('expose_event',    self._on_expose_event)

		self.todraw = []

	def add( self , painter ):
		self.todraw.append(painter)

	def remove( self , painter ):
		self.todraw = [ p for p in self.todraw if p != painter ]

	def _on_realize(self, *args):
		# Obtain a reference to the OpenGL drawable
		# and rendering context.
		gldrawable = self.get_gl_drawable()
		glcontext = self.get_gl_context()

		# OpenGL begin.
		if not gldrawable.gl_begin(glcontext):
			return

		# OpenGL end
		gldrawable.gl_end()

	def _on_configure_event(self, *args):
		# Obtain a reference to the OpenGL drawable
		# and rendering context.
		gldrawable = self.get_gl_drawable()
		glcontext = self.get_gl_context()

		self.width = self.allocation.width
		self.height = self.allocation.height

		# OpenGL begin
		if not gldrawable.gl_begin(glcontext):
			return False

		glViewport(0, 0, self.allocation.width, self.allocation.height)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho( -5 , 5 , -5 , 5 , -1 , 100 )
		glMatrixMode(GL_MODELVIEW)

		for p in self.todraw :
			p.gfx_init()

		# OpenGL end
		gldrawable.gl_end()

		return False

	def _on_expose_event(self, *args):
		# Obtain a reference to the OpenGL drawable
		# and rendering context.
		gldrawable = self.get_gl_drawable()
		glcontext = self.get_gl_context()

		# OpenGL begin
		if not gldrawable.gl_begin(glcontext):
			return False

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		for p in self.todraw :
			p.draw()

		if gldrawable.is_double_buffered():
			gldrawable.swap_buffers()
		else:
			glFlush()

		# OpenGL end
		gldrawable.gl_end()

		return False

