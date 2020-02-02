import math
import numpy as np

# Simple noise function, ported from
# https://github.com/aniongithub/graffiti/blob/master/Graffiti.Core/Math/Functions.cs

class Functions:
    # Only powers of two!
    NoiseTableSize = 1024
    NoiseProfile = np.random.random(NoiseTableSize)
    for i in range(NoiseTableSize):
        if i % 32 == 0:
            continue
        prev = (i // 32) * 32
        next = prev + 32
        if next >= NoiseTableSize:
            next = 0
        mu = (i % 32) / 32.0
        
        # CosineInterpolate
        mu2 = (1.0 - math.cos(mu * math.pi)) / 2.0
        NoiseProfile[i] = (NoiseProfile[prev] * (1 - mu2) + NoiseProfile[next] * mu2)

    @staticmethod
    def CosineInterpolate(y1, y2, mu):
        mu2 = (1.0 - math.cos(mu * math.pi)) / 2.0
        return (y1 * (1 - mu2) + y2 * mu2)

    @staticmethod
    def Value(t, frequency, phase = 0):
        pt = (t + phase) * frequency # "period" time, where 1 unit is 1 period on the "real" time stamp.
        tc = pt - math.trunc(pt) # cycle time within 1 period. 0..1.
        return tc
    
    @staticmethod
    def Noise(t, frequency, baseline = 0.0, amplitude = 1.0, phase = 0.0):
        value = Functions.Value(t, frequency, phase) * Functions.NoiseTableSize
        a = math.floor(value)
        b = math.ceil(value)
        mu = value - a
        if (b > Functions.NoiseTableSize - 1):
            b = 0
        return amplitude * Functions.CosineInterpolate(Functions.NoiseProfile[a], Functions.NoiseProfile[b], mu) + baseline

    @staticmethod
    def Sine(t, frequency, period = math.pi, baseline = 0.0, amplitude = 1.0, phase = 0.0):
        v = Functions.Value(t, frequency)
        return amplitude * math.sin(v * period) + baseline
