from scene import Scene

import numpy as np

class AnimState( Scene ) :
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

		st = a * self.bst + (1-a) * self.est

		self.robot.set_state( st )

	def anim_toggle( self ) :
		Scene.anim_toggle( self )

		st = self.robot.get_state()

		self.robot.resolve( self.ctls[0].pos , self.ctls[0].frm )
		self.bst = np.array( self.robot.get_state() )

		self.robot.resolve( self.ctls[1].pos , self.ctls[1].frm )
		self.est = np.array( self.robot.get_state() )

		self.robot.set_state( st )

