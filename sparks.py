import numpy as np
import numpy.linalg as la

import random as rnd

import math as m

import transformations as tr

from drawable import Drawable

from OpenGL.GL import *

from copy import copy

class Spark( Drawable ) :
	G = np.array( (0,-.9,0) )

	def __init__( self , pos , vel , lifeleft ) :
		Drawable.__init__( self )

		self.pvel = np.resize( vel , 3 ) * .05
		self. vel = copy(self.pvel)
		self.ppos = np.resize( pos , 3 )
		self. pos = copy(self.ppos)

		for i in range(10) :
			self. vel += .01 * self.G
			self. pos += .01 * self.vel

		self.life = lifeleft

	def draw( self ) :
		glColor4f( .99 , .98 , .28 , m.log( self.life + 1 , 2 ) )

		glBegin(GL_LINES)
		glVertex3f(*self.ppos)
		glVertex3f(*self. pos)
		glEnd()

	def update( self , dt ) : 
		self.pvel += dt * self.G
		self.ppos += dt * self.pvel

		self. vel += dt * self.G
		self. pos += dt * self.vel

		self.life-= dt

		return not self.died()

	def died( self ) :
		return self.life < 0 

class Sparks( Drawable ) :
	def __init__( self ) :
		Drawable.__init__( self )

		self.sparks = []

	def draw( self ) :
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)

		for s in self.sparks :
			s.draw()

		glDisable(GL_BLEND)

	def update( self , dt ) :
		for i in reversed(xrange(len(self.sparks))) :
			if not self.sparks[i].update( dt ) : del self.sparks[i]

	def spawn( self , pos , norm ) :
		for i in range(30) :
			life = rnd.gauss(.2,.4)
			vel = np.array([ rnd.gauss(norm[0],3) , rnd.gauss(norm[1],3) , rnd.gauss(norm[3],3) ])
			if life < 0 : continue
			self.sparks.append( Spark( pos , vel , life ) )

