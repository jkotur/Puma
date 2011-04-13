
import sys
import time

import numpy as np
import transformations as tr

from OpenGL.GL import *
from OpenGL.GLU import *

import math as m

if sys.platform.startswith('win'):
    timer = time.clock
else:
    timer = time.time

from camera import Camera
from robot import Robot
from plane import Plane

class Scene :
	def __init__( self , fovy , ratio , near , far , robot_files ) :
		self.fovy = fovy
		self.near = near 
		self.far = far
		self.ratio = ratio

		self.camera = Camera( ( 0 , 1 , -5 ) , ( 0 , 0 , 0 ) , ( 0 , 1 , 0 ) )
		self.plane  = Plane( (2,2) )

		self.robot = Robot( robot_files )

		self.x = 0.0

		self.last_time = timer()

		self.plane_alpha = 30.0 / 180.0 * m.pi

		self._make_plane_matrix()

	def _make_plane_matrix( self ) :
		r = tr.rotation_matrix( -self.plane_alpha , (0,0,1) )
		s = tr.scale_matrix( .25 )
		t = tr.translation_matrix( (-1.5,.25,.0) )

		self.m = np.dot( np.dot( t , s ) , r )

	def gfx_init( self ) :
		self._update_proj()
		self._set_lights()

		glEnable( GL_DEPTH_TEST )
		glEnable( GL_NORMALIZE )

	def draw( self ) :
		self.time = timer()

		dt = self.time - self.last_time

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.camera.look()

		pos = np.dot( self.m , np.array( [ m.sin(self.x) , 0 , m.cos(self.x) , 1 ] ) )
		nrm = np.dot( self.m , np.array( [      0        , 1 ,      0        , 0 ] ) )

		self.robot.draw( pos , nrm )
		self.plane.draw( self.m )

		self.x+=dt*.3

		self.last_time = self.time

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
		self.camera.rot( *map( lambda x : -x*.2 , df ) )

	def key_pressed( self , mv ) :
		self.camera.move( *map( lambda x : x*.25 , mv ) )

