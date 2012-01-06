
from scene import Scene

import numpy as np

class AnimPosition( Scene ) :
	def __init__( self , anim_time , *args ) :
		Scene.__init__( self , *args )
		self.anim_time = anim_time
	
	def _update_scene( self , dt ) :
		Scene._update_scene( self , dt )

		if not self.anim_state :
			self.robot.resolve( self.ctl.pos , self.ctl.frm )
			return

		if not self.ctls[0] or not self.ctls[1] : return

		a = (self.time - self.time_beg) / self.anim_time

		if a > 1.0 : a = 1.0

		pos = a * self.ctls[0].pos + (1-a) * self.ctls[1].pos
		x = a * self.ctls[0].frm[0] + (1-a) * self.ctls[1].frm[0]
		y = a * self.ctls[0].frm[1] + (1-a) * self.ctls[1].frm[1]
		z = a * self.ctls[0].frm[2] + (1-a) * self.ctls[1].frm[2]

		x = x / np.linalg.norm(x)
		y = y / np.linalg.norm(y)
		z = z / np.linalg.norm(z)

		self.robot.resolve( pos , (x,y,z) )

