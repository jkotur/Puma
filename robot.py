
import math as m
import numpy as np
import numpy.linalg as la

import transformations as tr

from OpenGL.GL import *

from drawable import Drawable
from mesh import Mesh

class Robot( Drawable ) :
	def __init__( self , files ) :
		Drawable.__init__( self )

		self.meshes = []
		for path in files :
			self.meshes.append( Mesh(path) )

	def draw( self , pos , norm ) :
		try :
			rots = self.inverse_kinematics( pos , norm ) 
		except ValueError , e :
			rots = [0]*5

		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		self.meshes[0].draw()
		glMultTransposeMatrixf( tr.rotation_matrix( rots[0] , (0,1,0) , (0,0,0) ) )
		self.meshes[1].draw()
		glMultTransposeMatrixf( tr.rotation_matrix( rots[1] , (0,0,1) , (0,.27,0) ) )
		self.meshes[2].draw()
		glMultTransposeMatrixf( tr.rotation_matrix( rots[2] , (0,0,1) , (-.91,.27,0) ) )
		self.meshes[3].draw()
		glMultTransposeMatrixf( tr.rotation_matrix( rots[3] , (1,0,0) , (0,.27,-.26) ) )
		self.meshes[4].draw()
		glMultTransposeMatrixf( tr.rotation_matrix( rots[4] , (0,0,1) , (-1.72,.27,-.26) ) )
		self.meshes[5].draw()
		glPopMatrix()

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

