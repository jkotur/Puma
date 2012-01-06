import math as m
import numpy as np
import numpy.linalg as la

import transformations as tr

from OpenGL.GL import *

from drawable import Drawable

class Controler( Drawable ) :
	def __init__( self , pos = np.zeros(3) , dir = np.array((1,0,0)) ) :
		self.pos = np.array(pos)
		self.dir = dir / np.linalg.norm(dir)

		self.pos.resize(4)
		self.dir.resize(4)

	def gfx_init( self ) :
		pass

	def move( self , dp ) :
		self.pos += dp

	def rotate( self , an , ax ) :
		self.dir = np.dot( tr.rotation_matrix(an,ax) , self.dir )

	def draw( self ) :
		glPushAttrib(GL_ALL_ATTRIB_BITS)
		glPushMatrix()

		glPointSize(5)
		glDisable(GL_LIGHTING)
		glDisable(GL_CULL_FACE)

		glTranslatef( self.pos[0] ,self.pos[1] ,self.pos[2] )

		glColor3f( 1 , .5 , 0 )

		glBegin(GL_POINTS)
		glVertex3f( 0 , 0 , 0 )
		glEnd()

		glScalef(.2,.2,.2)

		glBegin(GL_LINES)
		glVertex3f( 0 , 0 , 0 )
		glVertex3f( self.dir[0] , self.dir[1] , self.dir[2] )
		glEnd()

		glPopMatrix()
		glPopAttrib(GL_ALL_ATTRIB_BITS)

