import sys

import pygtk
pygtk.require('2.0')
import gtk

import operator as op

from OpenGL.GL import *

from glwidget import GLDrawingArea

from scene import Scene

ui_file = "puma.ui"

meshes = [ 'data/mesh{0}.mesh'.format(i) for i in range(1,7) ]

class App(object):
	"""Application main class"""

	def __init__(self):

		self.move = [0,0,0]

		self.dirskeys = ( ( ['w'] , ['s'] ) , ( ['a'] , ['d'] ) , ( ['e'] , ['q'] ) )

		for d in self.dirskeys :
			for e in d :
				for i in range(len(e)) : e[i] = ( gtk.gdk.unicode_to_keyval(ord(e[i])) , False )

		self.near = 1
		self.far = 1000
		self.fov  = 60

		builder = gtk.Builder()
		builder.add_from_file(ui_file)

		glconfig = self.init_glext()

		self.drawing_area = GLDrawingArea(glconfig)
		self.drawing_area.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON3_MOTION_MASK )
		self.drawing_area.set_size_request(320,240)

		builder.get_object("vbox1").pack_start(self.drawing_area)

		win_main = builder.get_object("win_main")

		win_main.set_events( gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK )

		win_main.connect('key-press-event'  , self._on_key_pressed  )
		win_main.connect('key-release-event', self._on_key_released )

		win_main.show_all()

		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height
		ratio = float(width)/float(height)

		self.scene = Scene( self.fov , ratio , self.near , self.far , meshes )
		self.drawing_area.add( self.scene )

		builder.connect_signals(self)

#        self.statbar = builder.get_object('statbar')

		self.drawing_area.connect('motion_notify_event',self._on_mouse_motion)
		self.drawing_area.connect('button_press_event',self._on_button_pressed)
		self.drawing_area.connect('configure_event',self._on_reshape)
		self.drawing_area.connect_after('expose_event',self._after_draw)

		gtk.timeout_add( 1 , self._refresh )

	def _refresh( self ) :
		self.drawing_area.queue_draw()
		return True

	def _after_draw( self , widget , data=None ) :
		self.update_statusbar()

	def update_statusbar( self ) :
		pass

	def _on_reshape( self , widget , data=None ) :
		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height

		ratio = float(width)/float(height)

		self.scene.set_screen_size( width , height )

	def _on_button_pressed( self , widget , data=None ) :
		if data.button == 3 :
			self.mouse_pos = data.x , data.y
		self.drawing_area.queue_draw()

	def _on_mouse_motion( self , widget , data=None ) :
		diff = map( op.sub , self.mouse_pos , (data.x , data.y) )

		self.scene.mouse_move( diff )

		self.mouse_pos = data.x , data.y
		self.drawing_area.queue_draw()

#        gtk.gdk.Keymap

	def _on_key_pressed( self , widget , data=None ) :
		print gtk.gdkgl.query_gl_extension('GL_EXT_stencil_wrap')
		print gtk.gdkgl.query_gl_extension('GL_EXT_stencil_two_side')
		if not any(self.move) :
			gtk.timeout_add( 20 , self._move_callback )

		for i in range(len(self.dirskeys)) :
			if (data.keyval,False) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]+= 1
			elif (data.keyval,False) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]-= 1

	
	def _on_key_released( self , widget , data=None ) :
		for i in range(len(self.dirskeys)) :
			if (data.keyval,True) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]-= 1
			elif (data.keyval,True) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]+= 1

	def _move_callback( self ) :
		self.scene.key_pressed( self.move )
		self.drawing_area.queue_draw()
		return any(self.move)

	def init_glext(self):
		# Query the OpenGL extension version.
#        print "OpenGL extension version - %d.%d\n" % gtk.gdkgl.query_version()

		# Configure OpenGL framebuffer.
		# Try to get a double-buffered framebuffer configuration,
		# if not successful then try to get a single-buffered one.
		display_mode = (
				gtk.gdkgl.MODE_RGB    |
				gtk.gdkgl.MODE_DEPTH  |
				gtk.gdkgl.MODE_STENCIL|
				gtk.gdkgl.MODE_DOUBLE )
		try:
			glconfig = gtk.gdkgl.Config(mode=display_mode)
		except gtk.gdkgl.NoMatches:
			display_mode &= ~gtk.gdkgl.MODE_DOUBLE
			glconfig = gtk.gdkgl.Config(mode=display_mode)

#        print "is RGBA:",                 glconfig.is_rgba()
#        print "is double-buffered:",      glconfig.is_double_buffered()
#        print "is stereo:",               glconfig.is_stereo()
#        print "has alpha:",               glconfig.has_alpha()
#        print "has depth buffer:",        glconfig.has_depth_buffer()
#        print "has stencil buffer:",      glconfig.has_stencil_buffer()
#        print "has accumulation buffer:", glconfig.has_accum_buffer()
#        print

		return glconfig

	def on_win_main_destroy(self,widget,data=None):
		gtk.main_quit()
		 
	def on_but_quit_clicked(self,widget,data=None):
		gtk.main_quit()

if __name__ == '__main__':
	app = App()
	gtk.main()

