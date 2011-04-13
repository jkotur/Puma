
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera :
	def __init__( self , eye , center , up ) :
		glMatrixMode( GL_PROJECTION )
		glPushMatrix()
		glLoadIdentity()
		gluLookAt( *( eye + center + up ) )
		self.m = glGetFloatv( GL_PROJECTION_MATRIX )
		glPopMatrix()

	def look( self ) :
		glMultMatrixf( self.m )

	def rot( self , ax , ay ) :
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		glRotatef( ax , 0, 1, 0 )
		glRotatef( ay , 1, 0, 0 )
		glMultMatrixf( self.m )
		self.m = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPopMatrix()

	def move( self , fwd , right , up ) :
		self.m[3][2] += fwd
		self.m[3][1] += up
		self.m[3][0] += right

