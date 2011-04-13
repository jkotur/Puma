import sys

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

class Mesh( Drawable ) :
	def __init__( self , f = None ) :
		Drawable.__init__( self )

		self.verts , self.v , self.n , self.t , self.ev , self.et = [[]] * 6

		if file : self.fromFile( f )

	def draw( self ) :
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_NORMAL_ARRAY)

		glVertexPointer( 3 , GL_FLOAT , 0 , self.v )
		glNormalPointer(     GL_FLOAT , 0 , self.n )

		glDrawElements( GL_TRIANGLES , len(self.t) , GL_UNSIGNED_INT , self.t )

		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_NORMAL_ARRAY)


	def fromFile( self , path ) :
		f = open(path,'r')

		try :
			self.verts      = self._readVertices ( f )
			self.v , self.n = self._readPoints   ( f , self.verts )
			self.t          = self._readTriangels( f )
			self.ev,self.et = self._readEdges    ( f )
		except IOError as (errno, strerror):
			print path , " I/O error({0}): {1}".format(errno, strerror)
		except ValueError as e :
			print "Could not convert data: " , e

		self.verts = np.array( self.verts , np.float32 )
		self.v     = np.array( self.v     , np.float32 )
		self.n     = np.array( self.n     , np.float32 )
		self.t     = np.array( self.t     , np.uint32  )
		self.ev    = np.array( self.ev    , np.uint32  )
		self.et    = np.array( self.et    , np.uint32  )

	def _readVertices( self , f ) :
		v = []
		for i in xrange(int(f.readline())) :
			v += map( float , f.readline().split(' ') )
		return v

	def _readPoints( self , f , verts ) :
		v , n = [] , []
		for i in xrange(int(f.readline())) :
			l = f.readline().split(' ')
			ind = int(l[0])*3
			v += verts[ind:ind+3]
			n += l[1:]
		return v , n

	def _readTriangels( self , f ) :
		t = []
		for i in xrange(int(f.readline())) :
			t += map( int , f.readline().split(' ') )
		return t

	def _readEdges( self , f ) :
		ev , et = [] , []
		for i in xrange(int(f.readline())) :
			l = map( int , f.readline().split(' ') )
			ev += l[:2]
			et += l[2:]
		return ev , et

