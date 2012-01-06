
import math as m
import numpy as np
import numpy.linalg as la

import transformations as tr

from OpenGL.GL import *

from drawable import Drawable
from mesh import Mesh
from sparks import Sparks

class Robot( Drawable ) :
	def __init__( self , files ) :
		Drawable.__init__( self )

		self.meshes = []
		for path in files :
			self.meshes.append( Mesh(path) )

		self.colors = [ (.68,.16,.19) , (.68,.16,.19) , (.74,.73,.21) , (.15,.55,.27) , (.15,.55,.27) , (.14,.15,.12) ]

		self.sparks = Sparks()

	def resolve( self , pos , frame ) :
		rots = None
		try :
			rots = self.inverse_kinematics( pos , frame ) 
		except ValueError , e :
			rots = [0]*9

#        print rots

		self.ms = [ 
			tr.rotation_matrix( rots[0] , (0,0,1) ) ,
			tr.translation_matrix( ( 0, 0, rots[1] ) ) ,
			tr.rotation_matrix( rots[2] , (0,1,0) ) ,
			tr.translation_matrix( ( rots[3], 0, 0 ) ) ,
			tr.rotation_matrix( rots[4] , (0,1,0) ) ,
			tr.translation_matrix( ( 0, 0, -rots[5] ) ) ,
			tr.rotation_matrix( rots[6] , (0,0,1)  ) ,
			tr.translation_matrix( ( rots[7], 0, 0 ) ) ,
			tr.rotation_matrix( rots[8] , (0,0,1) )
		]

		self.sparks.spawn( np.resize(pos,3) , frame[0] )

	def create_volumes( self , pos ) :
		p = np.resize( pos , 3 )

		for i in range(6) :
			self.meshes[i].create_volume(p)

	def gfx_init( self ) :
		for i in range(6) :
			self.meshes[i].gfx_init()

	def draw( self , sparks = True ) :
		glMatrixMode(GL_MODELVIEW)
		if sparks : self.sparks.draw()

		zr = np.array((0,0,0,1))
		pts = [ zr ] * 5
		for i in range(3,-1,-1) :
			for j in range(i+1,5) :
				pts[j] = np.dot( self.ms[2*i+1] , pts[j] )
				pts[j] = np.dot( self.ms[2*i  ] , pts[j] )

#        print np.array(pts)

		glBegin(GL_LINE_STRIP)
		for p in pts :
			glVertex3f( p[0] , p[1] , p[2] )
		glEnd()

	def draw_volumes( self , cull = GL_NONE , visible = False ) :
		ml = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPushMatrix()
		for i in range(3,4) :
#            glMultTransposeMatrixf( self.ms[i] )
			self.meshes[i].draw_volume(ml,cull,visible)
		glPopMatrix()

	def update( self , dt ) :
		self.sparks.update( dt )

	def inverse_kinematics( self , pos ,  frame ) :
		l1 , l3 , l4 = 1 , 1 , 1 

#        p5 = np.array((pos[0],pos[2],pos[1]))
		p5 = pos

		x =-frame[0]
		y =-frame[1]
		z =-frame[2]

		a1 = m.atan2( p5[1] - l4 * x[1] , p5[0] - l4* x[0] )
		c1 = m.cos(a1)
		s1 = m.sin(a1)

		a4 = m.asin( c1 * x[1] - s1 * x[0] ) # FIXME: przypadki
		c4 = m.cos(a4)
		s4 = m.sin(a4)

		c5 = ( c1*y[1] - s1*y[0] ) / c4 
		s5 = ( s1*z[0] - c1*z[1] ) / c4
		a5 = m.atan2( s5 , c5 )

		a2 = m.atan( -(c1*c4*(p5[2] - l4*x[2] - l1) + l3*(x[0] + s1*s4))/
							(c4*(p5[0]-l4*x[0]) - c1*l3*x[2]) ) #FIXME: przypadki
		c2 = m.cos(a2)
		s2 = m.sin(a2)

		q2 = (c4*(p5[0]-l4*x[0])-c1*l3*x[2])/(c1*c2*c4)

		c23 = (x[0] + s1*s4) / (c1*c4)
		s23 = -x[2]/c4
		a23 = m.atan2( s23 , c23 )

		a3 = a23 - a2

#        a1 , a2 , a3 , a4 , a5 , q2  = 0 , -m.pi / 4 , m.pi/4 , 0 , 0 , 1

		return a1 , l1 , a2 , q2 , a3 , l3 , a4 , l4 , a5

