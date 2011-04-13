
import operator as op

from robot import Robot

from OpenGL.GL import *
from OpenGL.GLU import *


class Scene :
	def __init__( self , fov , ratio , near , robot_files ) :
		self.fov = fov
		self.near = near 
		self.ratio = ratio

		self.eye = ( 0 , 1 , -5 )
		self.center = ( 0 , 0 , 0 )
		self.up = ( 0 , 1 , 0 )

		self.robot = Robot( robot_files )

	def gfx_init( self ) :
		self._update_proj()

	def draw( self ) :
		gluLookAt( *( self.eye + self.center + self.up ) )
		self.robot.draw()

	def _update_proj( self ) :
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective( 75 , self.ratio , 1 , 1000 )
		glMatrixMode(GL_MODELVIEW)

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

	def mouse_move( self , df ) :
		pass

