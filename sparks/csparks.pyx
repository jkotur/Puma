
cimport numpy as np

import cython

import random as rnd
import math as m

import numpy as np

cdef float Gx = 0
cdef float Gy =-9
cdef float Gz = 0

@cython.boundscheck(False)
cpdef int update( np.ndarray[ double ] pos , np.ndarray[ double ] vel , np.ndarray[ double ] col , np.ndarray[ double ] life , double dt , int l ) :
	cdef int id
	cdef int cid
	cdef int end = l-1
	cdef int eid
	cdef int i = 0

	while i < l :
		id = i*2*3
		cid = i*2*4

		life[i] -= dt

		if life[i] < 0 :
			l -= 1
			if i >= l : return l
			eid = l*3*2

			vel[id  ] = vel[eid  ]
			vel[id+1] = vel[eid+1]
			vel[id+2] = vel[eid+2]
			vel[id+3] = vel[eid+3]
			vel[id+4] = vel[eid+4]
			vel[id+5] = vel[eid+5]
			pos[id  ] = pos[eid  ]
			pos[id+1] = pos[eid+1]
			pos[id+2] = pos[eid+2]
			pos[id+3] = pos[eid+3]
			pos[id+4] = pos[eid+4]
			pos[id+5] = pos[eid+5]
			col[cid+3] = col[l*4*2+3]
			col[cid+7] = col[l*4*2+7]
			life  [i] = life [l]

			life[i] -= dt

		vel[id  ] += dt * Gx
		vel[id+1] += dt * Gy
		vel[id+2] += dt * Gz

		pos[id  ] += dt * vel[id  ]
		pos[id+1] += dt * vel[id+1]
		pos[id+2] += dt * vel[id+2]

		vel[id+3] += dt * Gx
		vel[id+4] += dt * Gy
		vel[id+5] += dt * Gz

		pos[id+3] += dt * vel[id+3]
		pos[id+4] += dt * vel[id+4]
		pos[id+5] += dt * vel[id+5]

		col[cid+3] = col[cid+7] = m.log( life[i] + 1 , 2 )

		i += 1

	return l

@cython.boundscheck(False)
cpdef iterate( np.ndarray[ double ] pos , np.ndarray[ double ] vel , double dt ) :
	for i in range(10) :
		vel[0] += dt * Gx
		vel[1] += dt * Gy
		vel[2] += dt * Gz
		pos[0] += dt * vel[0]
		pos[1] += dt * vel[1]
		pos[2] += dt * vel[2]
	return 0

