
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

		self.state = (0,1,0,1,0,1,0,1,0)

	def get_state( self ) :
		return self.state

	def set_state( self , state ) :
		self.state = state

		self.ms = [ 
			tr.rotation_matrix( self.state[0] , (0,0,1) ) ,
			tr.translation_matrix( ( 0, 0, self.state[1] ) ) ,
			tr.rotation_matrix( self.state[2] , (0,1,0) ) ,
			tr.translation_matrix( ( self.state[3], 0, 0 ) ) ,
			tr.rotation_matrix( self.state[4] , (0,1,0) ) ,
			tr.translation_matrix( ( 0, 0, -self.state[5] ) ) ,
			tr.rotation_matrix( self.state[6] , (0,0,1)  ) ,
			tr.translation_matrix( ( self.state[7], 0, 0 ) ) ,
			tr.rotation_matrix( self.state[8] , (0,0,1) )
		]


	def resolve( self , pos , frame ) :
		try :
			self.set_state( self.inverse_kinematics( pos , frame , self.state ) )
		except ValueError , e :
			self.set_state( (0,1,0,1,0,1,0,1,0) )

		def rtd( i ) :
			return self.state[i] * 180.0 / m.pi

		print rtd(0) , rtd(2) , rtd(4) , rtd(6) , rtd(8)


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
		for i in range(len(pts)) :
			glColor3f( *self.colors[i] )
			glVertex3f( pts[i][0] , pts[i][1] , pts[i][2] )
		glEnd()

		self.sparks.spawn( np.resize(pts[-1],3) , pts[-2] - pts[-1] )


	def draw_volumes( self , cull = GL_NONE , visible = False ) :
		ml = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPushMatrix()
		for i in range(3,4) :
#            glMultTransposeMatrixf( self.ms[i] )
			self.meshes[i].draw_volume(ml,cull,visible)
		glPopMatrix()

	def update( self , dt ) :
		self.sparks.update( dt )

	def inverse_kinematics( self , p5 ,  frame , os ) :
		l1 , l3 , l4 = 1 , 1 , 1 

		x =-frame[0]
		y =-frame[1]
		z =-frame[2]

		def rtd( a ) :
			return a * 180.0 / m.pi

		a1 = m.atan( (p5[1] - l4 * x[1])/(p5[0] - l4* x[0]) )
		print rtd(a1)
		if m.fabs( a1 - os[0] ) > m.fabs( a1 + m.pi - os[0] ) : 
			a1 += m.pi
		c1 = m.cos(a1)
		s1 = m.sin(a1)

		a4 = m.asin( c1 * x[1] - s1 * x[0] )
#        if m.fabs( a4 - os[6] ) > m.fabs( a4 + m.pi - os[6] ) : 
#            a4 += m.pi
		c4 = m.cos(a4)
		s4 = m.sin(a4)

		c5 = ( c1*y[1] - s1*y[0] ) / c4 
		s5 = ( s1*z[0] - c1*z[1] ) / c4
		a5 = m.atan( s5 / c5 )
		if m.fabs( a5 - os[0] ) > m.fabs( a5 + m.pi - os[0] ) : 
			a5 += m.pi

		a2 = m.atan( -(c1*c4*(p5[2] - l4*x[2] - l1) + l3*(x[0] + s1*s4))/
							(c4*(p5[0]-l4*x[0]) - c1*l3*x[2]) )
		if m.fabs( a2 + os[2] ) > m.fabs( a2 + m.pi - os[2] ) : 
			a1 += m.pi
		c2 = m.cos(a2)
		s2 = m.sin(a2)

		q2 = (c4*(p5[0]-l4*x[0])-c1*l3*x[2])/(c1*c2*c4)

		c23 = (x[0] + s1*s4) / (c1*c4)
		s23 = -x[2]/c4
		a23 = m.atan2( s23 , c23 )

		a3 = a23 - a2

		return a1 , l1 , a2 , q2 , a3 , l3 , a4 , l4 , a5

