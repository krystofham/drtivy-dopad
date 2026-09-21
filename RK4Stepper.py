import numpy as np
from SystemState import SystemState

class RK4Stepper:

	def __init__(self):
		self.k1 = SystemState()
		self.k2 = SystemState()
		self.k3 = SystemState()
		self.k4 = SystemState()

	# Do single RK4 step.
	def nextStep(self, t_0, t_step, state, problem):
		t_0 += t_step 
		problem.getDerivatives(t_0, state, self.k1)
		problem.getDerivatives(t_0 + t_step/2, state + t_step * self.k1/2,  self.k2)
		problem.getDerivatives(t_0 + t_step/2, state + t_step * self.k2/2,  self.k3)
		problem.getDerivatives(t_0 + t_step, state + t_step * self.k3,  self.k4)

		state_new = state + 1/6*t_step*(self.k1 + 2* self.k2 + 2*self.k3 + self.k4)
		# earthPosNew = earthPos + 1/6*(t_step)*(self.k1+2*self.k2+2*self.k3+self.k4)


		# Fill in this method. It should return new system state after one state.
		# Use RK4

		return SystemState(state_new.EarthPosition, state_new.EarthPosition, state_new.AsteroidPosition, state_new.AsteroidVelocity)