
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

	def resolve( self , pos , norm ) :
		rots = None
		try :
			rots = self.inverse_kinematics( pos , norm ) 
		except ValueError , e :
			rots = [0]*5

		self.ms = [ 
			tr.identity_matrix() ,
			tr.rotation_matrix( rots[0] , (0,1,0) , (0,0,0) ) ,
			tr.rotation_matrix( rots[1] , (0,0,1) , (0,.27,0) ) ,
			tr.rotation_matrix( rots[2] , (0,0,1) , (-.91,.27,0) ) ,
			tr.rotation_matrix( rots[3] , (1,0,0) , (0,.27,-.26) ) ,
			tr.rotation_matrix( rots[4] , (0,0,1) , (-1.72,.27,0) )
		]

		self.sparks.spawn( np.resize(pos,3) , norm )

	def create_volumes( self , pos ) :
		p = np.resize( pos , 3 )

		for i in range(6) :
			self.meshes[i].create_volume(p)

	def gfx_init( self ) :
		for i in range(6) :
			self.meshes[i].gfx_init()

	def draw( self ) :
		self.sparks.draw()
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		for i in range(6) :
			glColor3f(*self.colors[i])
			glMultTransposeMatrixf( self.ms[i] )
			self.meshes[i].draw()
		glPopMatrix()

	def draw_volumes( self , cull = GL_NONE , visible = False ) :
		ml = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPushMatrix()
		for i in range(6) :
			glMultTransposeMatrixf( self.ms[i] )
			self.meshes[i].draw_volume(ml,cull,visible)
		glPopMatrix()

	def update( self , dt ) :
		self.sparks.update( dt )

	def inverse_kinematics( self , pos ,  normal ) :
		l1 , l2 , l3 = .91 , .81 , .33
		dy , dz  = .27 , .26 

		normal = normal / la.norm( normal )

		pos1 = pos + normal * l3

		e = m.sqrt(pos1[2]*pos1[2]+pos1[0]*pos1[0]-dz*dz)

		a1 = m.atan2(pos1[2], -pos1[0]) + m.atan2(dz, e)

		pos2 = np.array( [ e , pos1[1]-dy , .0 ] );
		a3 = -m.acos(min(1.0,(pos2[0]*pos2[0]+pos2[1]*pos2[1]-l1*l1-l2*l2)/(2.0*l1*l2)))
		k = l1 + l2 * m.cos(a3)
		l = l2 * m.sin(a3)
		a2 = -m.atan2(pos2[1],m.sqrt(pos2[0]*pos2[0]+pos2[2]*pos2[2])) - m.atan2(l,k);

		rotmat = tr.rotation_matrix( -a1 , (0,1,0) ) 
		normal1 = np.resize( np.dot( rotmat , np.resize( normal , 4 ) ) , 3 )

		rotmat = tr.rotation_matrix( -a2-a3 , (0,0,1) ) 
		normal1 = np.resize( np.dot( rotmat , np.resize( normal1, 4 ) ) , 3 )

		a5 = m.acos( normal1[0] )
		a4 = m.atan2(normal1[2], normal1[1])

		return a1 , a2 , a3 , a4 , a5

