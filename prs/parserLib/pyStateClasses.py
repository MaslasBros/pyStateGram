class DiagramPackage:
    """
    A class holding the created state and transitions dictionaries
    """
    def __init__(self, states:dict, transitions:dict):
        self.states = states
        self.transitions = transitions
        pass

class Transition:
    """
    A compact class representing a state transition.
    """
    def __init__(self, source:str, target:str, onTransition):
        """
        Creates a Transition instance which caches the 
        source and target of the transition.\n
        Accepts a method that can be executed when the transition happens.
        """
        self.source = source
        self.target = target
        self.onTransition = onTransition
        pass