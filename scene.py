
import operator as op

from OpenGL.GL import *

class Scene :
	def __init__( self , fov , ratio , near ) :
		self.fov = fov
		self.near = near 
		self.ratio = ratio

	def gfx_init( self ) :
		pass

	def draw( self ) :
		pass

	def _update_proj( self ) :
		pass

	def set_fov( self , fov ) :
		self.fov = fov
		self._update_proj()

	def set_near( self , near ) :
		self.near = near
		self._update_proj()

	def set_ratio( self , ratio ) :
		self.ratio = ratio
		self._update_proj()

	def set_screen_size( self , w , h ) :
		self.width  = w 
		self.height = h
		self.set_ratio( float(w)/float(h) )

	def mouse_move( self , df , a1 , a2 ) :
		pass

