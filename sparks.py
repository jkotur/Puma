
import cython

import random as rnd
import math as m

import numpy as np

import csparks 

from OpenGL.GL import *

from copy import copy

class Sparks :
	def __init__( self ) :
		self.size = 1024
		self.real_size = 0

		self.poss = np.zeros(self.size*3*2 , np.double )
		self.vels = np.zeros(self.size*3*2 , np.double )
		self.cols = np.zeros(self.size*4*2 , np.double )
		self.lifes= np.zeros(self.size , np.double )

	def draw( self ) :
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)

		glEnableClientState(GL_VERTEX_ARRAY);
		glEnableClientState(GL_COLOR_ARRAY);

		glVertexPointer( 3 , GL_FLOAT , 0 , self.poss )
		glColorPointer ( 4 , GL_FLOAT , 0 , self.cols )

		glDrawArrays( GL_LINES , 0 , self.real_size*2 )

		glDisableClientState(GL_VERTEX_ARRAY);
		glDisableClientState(GL_COLOR_ARRAY);

		glDisable(GL_BLEND)

	def update( self , dt ) :
		self.real_size = csparks.update( self.poss , self.vels , self.cols , self.lifes , dt , self.real_size )

	def spawn( self , pos , norm ) :
		for i in range(100) :
			life = rnd.gauss(.1,.2)

			if life < 0 : continue

			if self.real_size >= self.size :
				print 'Resizing: ' , self.size , self.real_size
				self.size *= 2
				self.poss.resize( self.size*3*2 )
				self.vels.resize( self.size*3*2 )
				self.cols.resize( self.size*4*2 )
				self.lifes.resize( self.size )

			var = .5
			vel = [ rnd.gauss(norm[0],var) , rnd.gauss(norm[1],var) , rnd.gauss(norm[3],var) ]

			ppos = copy(pos)
			pvel = np.array(vel)

			csparks.iterate( ppos , pvel , .002 )

			self.poss[self.real_size*3*2  :self.real_size*3*2+3] = pos 
			self.poss[self.real_size*3*2+3:self.real_size*3*2+6] =ppos

			self.vels[self.real_size*3*2  :self.real_size*3*2+3] = vel
			self.vels[self.real_size*3*2+3:self.real_size*3*2+6] =pvel
                                                             
			self.cols[self.real_size*4*2  :self.real_size*4*2+4] = [ .99 , .98 , .28 , 1 ]
			self.cols[self.real_size*4*2+4:self.real_size*4*2+8] = [ .99 , .98 , .28 , 1 ]

			self.lifes[self.real_size] = life

			self.real_size += 1

