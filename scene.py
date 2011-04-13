
import operator as op

from camera import Camera
from robot import Robot

from OpenGL.GL import *
from OpenGL.GLU import *


class Scene :
	def __init__( self , fovy , ratio , near , far , robot_files ) :
		self.fovy = fovy
		self.near = near 
		self.far = far
		self.ratio = ratio

		self.camera = Camera( ( 0 , 1 , -5 ) , ( 0 , 0 , 0 ) , ( 0 , 1 , 0 ) )

		self.robot = Robot( robot_files )

	def gfx_init( self ) :
		self._update_proj()
		self._set_lights()

	def draw( self ) :
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.camera.look()
		self.robot.draw()

	def _update_proj( self ) :
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective( self.fovy , self.ratio , self.near , self.far )
		glMatrixMode(GL_MODELVIEW)

	def _set_lights( self ) :
		glEnable(GL_LIGHTING);
		glLightfv(GL_LIGHT0, GL_AMBIENT, [ 0.2 , 0.2 , 0.2 ] );
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [ 0.9 , 0.9 , 0.9 ] );
		glLightfv(GL_LIGHT0, GL_SPECULAR,[ 0.9 , 0.9 , 0.9 ] );
		glLightfv(GL_LIGHT0, GL_POSITION, [ 0 , 5 , -2 ] );
		glEnable(GL_LIGHT0); 
						 
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
		self.camera.rot( *map( lambda x : -x*.1 , df ) )

	def key_pressed( self , mv ) :
		self.camera.move( *map( lambda x : x*.25 , mv ) )

