
from drawable import Drawable
from mesh import Mesh

class Robot( Drawable ) :
	def __init__( self , files ) :
		Drawable.__init__( self )

		self.meshes = []
		for path in files :
			self.meshes.append( Mesh(path) )

	def draw( self ) :
		for m in self.meshes :
			m.draw()

