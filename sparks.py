import numpy as np
import numpy.linalg as la

import random as rnd

import transformations as tr

from drawable import Drawable

from OpenGL.GL import *

class Spark( Drawable ) :
	G = np.array( (0,-.9,0) )

	def __init__( self , pos , vel , lifeleft ) :
		Drawable.__init__( self )

		self.pos = np.resize( pos , 3 )
		self.vel = np.resize( vel , 3 ) * .05
		self.life = lifeleft

	def draw( self ) :
		glPushMatrix()
		glTranslatef( *self.pos )
		glScalef( .01 , .01 , .01 )

		glBegin(GL_LINE_LOOP)
		glVertex3f(0,1,0)
		glVertex3f(1,0,0)
		glVertex3f(0,0,1)
		glVertex3f(0,-1,0)
		glVertex3f(-1,0,0)
		glVertex3f(0,0,-1)
		glEnd()
		glPopMatrix()

	def update( self , dt ) : 
		self.vel += dt * self.G
		self.pos += dt * self.vel
		self.life-= dt

	def died( self ) :
		return self.life < 0 

class Sparks( Drawable ) :
	def __init__( self ) :
		Drawable.__init__( self )

		self.sparks = []

	def draw( self ) :
		for s in self.sparks :
			s.draw()

	def update( self , dt ) :
		for s in self.sparks :
			s.update( dt )

		self.sparks = [ s for s in self.sparks if not s.died() ]

	def spawn( self , pos , norm ) :
		for i in range(20) :
			life = rnd.gauss(.2,.4)
			vel = np.array( [ rnd.gauss(norm[0],2) , rnd.gauss(norm[1],2) , rnd.gauss(norm[3],2) ] )
#            vel = vel / la.norm(vel)
			if life < 0 : continue
			self.sparks.append( Spark( pos , vel , life ) )

