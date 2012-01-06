
import sys
import time

import numpy as np
import numpy.linalg as la
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
from controler import Controler

class Scene :
	def __init__( self , fovy , ratio , near , far , robot_files ) :
		self.fovy = fovy
		self.near = near 
		self.far = far
		self.ratio = ratio

		self.camera = None
		self.plane  = Plane( (2,2) )

		self.wall = Plane( (20,10) )
		self.mw = tr.rotation_matrix( -m.pi / 2.0 , (1,0,0) )
		self.mw = np.dot( self.mw , tr.translation_matrix( (0,3,0) ) )

		self.robot = Robot( robot_files )
		self.ctl   = Controler()

		self.x = 0.0

		self.last_time = timer()

		self.plane_alpha = 65.0 / 180.0 * m.pi

		self.lpos = [ 1 ,-1 , 0 ]

		self._make_plane_matrix()

		self.draw_robot = True
		self.draw_sparks = True 
		self.draw_front = False
		self.draw_back = False

	def _make_plane_matrix( self ) :
		r = tr.rotation_matrix( self.plane_alpha , (0,0,1) )
		s = tr.scale_matrix( 1 )
		t = tr.translation_matrix( (-1.25,.7,.05) )

		self.m = np.dot( np.dot( t , s ) , r )
		self.im = la.inv( self.m )
		self.im[3] = [ 0 , 0 , 0 , 1 ]

	def gfx_init( self ) :
		self.camera = Camera( ( 0 , -3 , 0 ) , ( 0 , 0 , 0 ) , ( 0 , 0 , 1 ) )

		self._update_proj()

		glEnable( GL_DEPTH_TEST )
		glEnable( GL_NORMALIZE )
		glEnable( GL_CULL_FACE )
		glEnable( GL_COLOR_MATERIAL )
		glColorMaterial( GL_FRONT , GL_AMBIENT_AND_DIFFUSE )

		self.robot.gfx_init()

	def draw( self ) :
		self.time = timer()

		dt = self.time - self.last_time

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.camera.look()

		self.lpos = [ m.sin(1/10.0)*.5 , m.cos(1/10.0)*.5 , 2 ]

		self._update_scene( dt )
		self._draw_scene()

		self.x+=dt*.3

		self.last_time = self.time

	def _update_scene( self , dt ) :
		self.robot.update( dt )

		self.robot.resolve( self.ctl.pos , self.ctl.frm )


	def _draw_scene( self ) :
		glClearStencil(0);
		glClear(GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT);

		self.ctl.draw()

		self._set_ambient()
		self._set_diffuse()

		if self.draw_robot : self.robot.draw( self.draw_sparks )


	def _update_proj( self ) :
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective( self.fovy , self.ratio , self.near , self.far )
		glMatrixMode(GL_MODELVIEW)

	def _set_lights( self ) :
		glEnable(GL_LIGHTING);
		glLightfv(GL_LIGHT0, GL_AMBIENT, [ 0.2 , 0.2 , 0.2 ] );
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [ 0.9 , 0.9 , 0.9 ] );
		glLightfv(GL_LIGHT0, GL_SPECULAR,[ 0.3 , 0.3 , 0.3 ] );
		glLightfv(GL_LIGHT0, GL_POSITION, self.lpos );
		glEnable(GL_LIGHT0); 

	def _set_ambient( self ) :
		glEnable(GL_LIGHTING);
		glLightfv(GL_LIGHT0, GL_AMBIENT, [ 0.1 , 0.1 , 0.1 ] );
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [ 0.0 , 0.0 , 0.0 ] );
		glLightfv(GL_LIGHT0, GL_SPECULAR,[ 0.0 , 0.0 , 0.0 ] );
		glLightfv(GL_LIGHT0, GL_POSITION, self.lpos );
		glEnable(GL_LIGHT0); 

	def _set_diffuse( self ) :
		glEnable(GL_LIGHTING);
		glLightfv(GL_LIGHT0, GL_AMBIENT , [ 0.0 , 0.0 , 0.0 ] );
		glLightfv(GL_LIGHT0, GL_DIFFUSE , [ 0.9 , 0.9 , 0.9 ] );
		glLightfv(GL_LIGHT0, GL_SPECULAR, [ 0.3 , 0.3 , 0.3 ] );
#        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
#        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)
#        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.08)
		glLightfv(GL_LIGHT0, GL_POSITION, self.lpos );
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

	def mouse_move( self , df , buts ) :
		if 1 in buts and buts[1] :
			mv = np.array( (-df[0],df[1],0,0) , np.float )
			mv *= .01
			self.ctl.move( np.dot( mv , np.linalg.inv(self.camera.m) ) )
		if 2 in buts and buts[2] :
			self.ctl.rotate( -df[0]*0.01 , np.dot( np.array((0,0,1,0)) , np.linalg.inv(self.camera.m) ) )
		elif 3 in buts and buts[3] :
			self.camera.rot( *map( lambda x : -x*.2 , df ) )

	def key_pressed( self , mv ) :
		self.camera.move( *map( lambda x : x*.25 , mv ) )

