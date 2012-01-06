import sys , traceback

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

	def add( self , painter , viewport = (0,0,1,1) ):
		self.todraw.append( (painter,viewport) )

	def remove( self , painter ):
		self.todraw = [ p for p in self.todraw if p[0] != painter ]

	def _on_realize(self, *args):
		# Obtain a reference to the OpenGL drawable
		# and rendering context.
		gldrawable = self.get_gl_drawable()
		glcontext = self.get_gl_context()

		print 'Realize!'

		# OpenGL begin.
		if not gldrawable.gl_begin(glcontext):
			return

		for p in self.todraw :
			p[0].gfx_init()

		# OpenGL end
		gldrawable.gl_end()

	def _on_configure_event(self, *args):
		# Obtain a reference to the OpenGL drawable
		# and rendering context.
		gldrawable = self.get_gl_drawable()
		glcontext = self.get_gl_context()

		self.width = self.allocation.width
		self.height = self.allocation.height

		print 'Configure!'

		# OpenGL begin
		if not gldrawable.gl_begin(glcontext):
			return False

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

		try :
			for p in self.todraw :
				self.__set_viewport( p[1] )
				p[0].draw()
		except Exception as e :
			t , v , tb = sys.exc_info()
			print
			print 'Traceback:'
			traceback.print_tb( tb )
			print
			print '%s: %s' % (type(e).__name__ , str(e))
			sys.exit(0)

		if gldrawable.is_double_buffered():
			gldrawable.swap_buffers()
		else:
			glFlush()

		# OpenGL end
		gldrawable.gl_end()

		return False

	def __set_viewport( self , v ) :
		glViewport( *map( int , (self.allocation.width * v[0] , self.allocation.height * v[1] , self.allocation.width * v[2] , self.allocation.height * v[3]) ) )


