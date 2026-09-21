import time
class ODESolver:
    problem = None
    stepper = None
    conservedValueRelativeTreshold = None
    conservedValues = []
    outputList = []

    def __init__(self, stepper, problem):
        self.problem = problem
        self.stepper = stepper

    # Registers custom output function which is triggered every step of the simulation
    def registerOutput(self, output):
        self.outputList.append(output)

    # Runs the simulation from t_0 to t_max with step size t_step
    # state is starting state of the system
    #
    def integrate(self, t_0, t_max, t_step, conservedValueRelativeTreshold, state):
        t = t_0

        # Store initial conserved values
        self.conservedValueRelativeTreshold = conservedValueRelativeTreshold
        self.conservedValues = self.problem.getConservedValues(t_0, state)

        iteration = 0
        while (t < t_max):
            #time.sleep(0.5)
            iteration += 1
            state_new = self.stepper.nextStep(t_0, t_step, state, self.problem)
            halt = self.problem.shouldHalt(t, t + t_step, state, state_new)

            if not self.checkConservedValues(t + t_step, state_new):
                break

            for output in self.outputList:
                output(t + t_step, state, iteration)

            if (halt):
                return True

            t += t_step
            state = state_new

        return False

    def checkConservedValues(self, t_new, state_new):
        conservedValues = self.problem.getConservedValues(t_new, state_new)
        success = True

        for index in range(len(conservedValues)):
            value = conservedValues[index]
            ratio = value / self.conservedValues[index]
            if (ratio < 1):
                ratio = 1 / ratio
            if (ratio - 1 > self.conservedValueRelativeTreshold):
                success = False
                print("Conserved value {0} is too far from expected. current = {1}, expected = {2}".format(index, value, self.conservedValues[index]))

        return success
