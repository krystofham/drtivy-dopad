import numpy as np
from SystemState import SystemState
class Space:
    SunMass = 1.99E30
    EarthMass = 5.94E24
    GConst = 6.67E-11
    EarthRadius = 6378000

    # There are 4 variables, each of three coordinates. This function computes
    # d/dt for each variable
    def getDerivatives(self, time, state, dState):
        # Fill in this method.
        # Set dState with time derivatives of state .

        dState.EarthPosition = state.EarthVelocity
        dState.EarthVelocity = -self.GConst * self.SunMass*state.EarthPosition / (np.linalg.norm(state.EarthPosition)**3)
        #print(self.GConst * self.SunMass / (state.EarthPosition**2))
        dState.AsteroidPosition = state.AsteroidVelocity
        dState.AsteroidVelocity = -(self.GConst * self.SunMass* state.AsteroidPosition / np.linalg.norm(state.AsteroidPosition)**3) 
        - (self.GConst * self.EarthMass * (state.AsteroidPosition - state.EarthPosition)/ np.linalg.norm(state.AsteroidPosition - state.EarthPosition)**3)
        
    # Decides whether the simulation should terminate
    def shouldHalt(self, t_old, t_new, state_old, state_new):

        # Fill in this method.
        e_old = state_old.EarthPosition
        e_new = state_new.EarthPosition
        a_new = state_new.AsteroidPosition
        if np.linalg.norm((a_new - e_new) - np.dot((a_new - e_new), ((e_new - e_old))/ np.linalg.norm(e_new - e_old))) < self.EarthRadius:
            return True
        # Decide whether the collision of the asteroid with Earth occured.
        if (np.linalg.norm(state_old.AsteroidPosition - state_old.EarthPosition)) < self.EarthRadius:
            return True
        return False

    # This function returns a list of values which sould be constant during the simulation.
    # It is used to check the correctness of the algorithm and if the step size is not too big
    def getConservedValues(self, t, state):

        # Fill in this method.
        # Returs as much values as possible which are constant during the simulation and may help
        # us to decide if the algorithm is correct
        SunMass = 1.99E30
        EarthMass = 5.94E24
        GConst = 6.67E-11
        EarthRadius = 6378000
        return [SunMass, EarthMass, GConst, EarthRadius]