#!/usr/bin/env python3.6

from fauxmo.plugins import FauxmoPlugin
import RPi.GPIO as GPIO
import time
from threading import Thread
import numpy as np

from Functions import *
from PWM import *

# Our class is a Fauxmo plugin, instances will be created when 
# launched with 'fauxmo -c irongauntlet.json'
class InfinityStone(FauxmoPlugin):
    name = None
    
    # Names of our Infinity stones to indices
    stoneIndices = {
        "Time stone": 0,
        "Power stone": 1,
        "Space stone": 2,
        "Mind stone": 3,
        "Reality stone": 4,
        "Soul stone" : 5
    }

    # Contains the current states of our Infinity stones
    # Off by default so we can have the pleasure of activating them :)
    states =  [ 0.0, 0.0,  0.0,  0.0,  0.0,  0.0 ]

    # GPIO pins associated with our Infinity stones
    ledPins = [11, 12, 13, 15, 16, 18]

    # Random phases for our Noise function
    phases = np.random.random(6) * 10
    # Frequency of our noise function for all stones (Hz)
    noiseFrequency = 0.05
    
    # PWM sampling frequency (Hz)
    frequency = 60

    # Minimum brightness
    baselines = [ 0.1, 0.1, 0.1, 0.1, 0.1, 0.1 ]

    # Did we initialize GPIO?
    initialized = False

    # Is our rendering thread running?
    running = False

    # Rendering thread
    thread = None

    # Utility method to check if all our Infinity stones are off
    @staticmethod
    def areAllOff():
        for i in range(len(InfinityStone.states)):
            if InfinityStone.states[i] == 1.0:
                return False
        return True

    # Initialize GPIO
    @staticmethod
    def initialize():	
        print("Acquiring infinity stones...")
        GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
        GPIO.setup(InfinityStone.ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
        GPIO.output(InfinityStone.ledPins, GPIO.HIGH) # make all ledPins output HIGH level, turn off all leds
        InfinityStone.initialized = True

    @staticmethod
    def teardown():
        # Turn off all stones
        InfinityStone.states = np.zeros(6)
        
        # Update rendering state
        InfinityStone.updateRenderingState()

        # GPIO cleanup
        GPIO.cleanup()

        InfinityStone.initialized = False

    # Rendering thread function
    @staticmethod
    def run():
        # We're running now
        InfinityStone.running = True
        sampler = PWM()
        pwm = np.zeros(6)
        # TODO: Make this an FPS based loop, not a tight loop
        while InfinityStone.running:
            # Get current time
            t = time.time()
            
            # For all Infinity stones
            for i in range(len(InfinityStone.ledPins)):
                # Find out current noise value (amplitude)
                noise = Functions.Noise(t, InfinityStone.noiseFrequency,
                    baseline = InfinityStone.baselines[i] * InfinityStone.states[i], # RESPECT the state!
                    amplitude = InfinityStone.states[i], # RESPECT the state!
                    phase = InfinityStone.phases[i])
                
                # Convert into a PWM value representing brightness
                # For example: if the noise function asked us to set half-brightness (amplitude = 0.5),
                # our PWM generator would output a 50% duty cycle wave, with frequency of InfinityStone.frequency

                # Note: It's important that for smooth rendering, the loop run faster than 1 / (2 * InfinityStone.frequency) Hz, 
                # in accordance with the Nyquist-Shannon sampling theorem (https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)
                pwmVal = sampler.sample(t, InfinityStone.frequency, noise, GPIO.HIGH, GPIO.LOW)

                # We have an instantanous value for this pin, output it!
                GPIO.output(InfinityStone.ledPins[i], pwmVal)
    
    @staticmethod
    def updateRenderingState():
        if InfinityStone.running:
            # See if we can stop/pause rendering
            if InfinityStone.areAllOff():
                print("Stop/Pause rendering")
                InfinityStone.running = False
                if InfinityStone.thread != None: 
                    InfinityStone.thread.join()
                    InfinityStone.thread = None
        else:
            # See if we need to start/resume rendering
            if InfinityStone.thread == None:
                print("Start/Resume rendering")
                InfinityStone.thread = Thread(target = InfinityStone.run)
                InfinityStone.thread.start()

    # Constructor, called by Fauxmo - one instance per device
    def __init__(
        self,
        name: str,
        port: int,
        on_cmd: str,
        off_cmd: str,
        state_cmd: str = None,
        use_fake_state: bool = True
    ) -> None:
        self.name = name

        # Do this once for all instances
        if not InfinityStone.initialized:
            InfinityStone.initialize()

        super().__init__(name=name, port=port)
        print(f"{self.name} acquired!")
        InfinityStone.updateRenderingState()

    def __del__(self):
        
        # Do this once for all instances
        if InfinityStone.initialized:
            InfinityStone.teardown()
        
        print(f"{self.name} destroyed!")

    def on(self) -> bool:
        # Set state to 1.0 and update rendering state
        print(f"Activating {self.name}!")
        InfinityStone.states[InfinityStone.stoneIndices[self.name]] = 1.0
        InfinityStone.updateRenderingState()
        return True

    def off(self) -> bool:
        # Set state to 0.0 and update rendering state
        print(f"Deactivating {self.name}!")
        InfinityStone.states[InfinityStone.stoneIndices[self.name]] = 0.0
        InfinityStone.updateRenderingState()
        return True

    def get_state(self) -> str:
        # Return status as "on/off"
        state = "on" if InfinityStone.states[InfinityStone.stoneIndices[self.name]] == 1 else "off"
        return state