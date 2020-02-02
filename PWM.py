import math

class PWM:

    # Generate a PWM sample for a given dutyCycle at time t
    @staticmethod
    def sample(t, frequency, dutyCycle, lowVal = 0, highVal = 1):
        pt = t * frequency # "period" time, where 1 unit is 1 period on the "real" time stamp
        tc = pt - math.trunc(pt) # cycle time within 1 period. 0..1.
        return highVal if tc < dutyCycle else lowVal