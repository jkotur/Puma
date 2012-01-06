import math as m
import numpy as np
import numpy.linalg as la

import transformations as tr

from OpenGL.GL import *

from drawable import Drawable

class Controler( Drawable ) :
	def __init__( self , pos = np.zeros(3) ) :
		self.pos = np.array(pos)
		self.pos.resize(4)

		self.frm = np.array(((1,0,0,0),(0,1,0,0),(0,0,1,0)))

	def gfx_init( self ) :
		pass

	def move( self , dp ) :
		self.pos += dp

	def rotate( self , an , ax ) :
		mat = tr.rotation_matrix(an,ax)
		self.frm = np.array(
				( np.dot( mat , self.frm[0] ) , 
				  np.dot( mat , self.frm[1] ) ,
				  np.dot( mat , self.frm[2] ) )
				)

	def draw( self ) :
		glPushAttrib(GL_ALL_ATTRIB_BITS)
		glPushMatrix()

		glPointSize(5)
		glDisable(GL_LIGHTING)
		glDisable(GL_CULL_FACE)

		glTranslatef( self.pos[0] ,self.pos[1] ,self.pos[2] )

		glScalef(.2,.2,.2)

		glBegin(GL_LINES)
		glColor3f( 1 , 0 , 0 )
		glVertex3f( 0 , 0 , 0 )
		glVertex3f( self.frm[0][0] , self.frm[0][1] , self.frm[0][2] )
		glColor3f( 0 , 1 , 0 )
		glVertex3f( 0 , 0 , 0 )
		glVertex3f( self.frm[1][0] , self.frm[1][1] , self.frm[1][2] )
		glColor3f( 0 , 0 , 1 )
		glVertex3f( 0 , 0 , 0 )
		glVertex3f( self.frm[2][0] , self.frm[2][1] , self.frm[2][2] )
		glEnd()

		glBegin(GL_POINTS)
		glColor3f( 1 , .5 , 0 )
		glVertex3f( 0 , 0 , 0 )
		glEnd()

		glPopMatrix()
		glPopAttrib(GL_ALL_ATTRIB_BITS)

