class DiagramPackage:
    """
    A class holding the created state and transitions dictionaries
    """
    def __init__(self, states:dict, transitions:dict):
        """
        Creates a DiagramPackage instance.

        Attributes:
            ~ pyFsm.DiagramPackage.states (:class:`dict`): Populated from the constructor
            ~ pyFsm.DiagramPackage.transitions (:class:`dict`): Populated from the constructor

        Args:
            states (:class:`dict`): A dictionary containing the state names as keys
            transitions (:class:`dict`): A dicitonary containing the transition names as keys
        """

        self.states = states
        self.transitions = transitions
        pass

class Transition:
    """
    A compact class representing a state transition.
    """
    def __init__(self, source:str, target:str, onTransition):
        """
        Creates a Transition instance which caches the source and target of the transition.

        Attributes:
            ~ pyFsm.pyStateClasses.Transition.source (:class:`str`): Populated from the constructor
            ~ pyFsm.pyStateClasses.Transition.target (:class:`str`): Populated from the constructor
            ~ pyFsm.pyStateClasses.Transition.onTransition (:class:`func`): Populated from the constructor

        Args:
            source (:class:`str`): The source state.
            target (:class:`str`): The target state.
            onTransition (:class:`func`): The transition function to execute between the state transtitioning.
        """
        self.source = source
        self.target = target
        self.onTransition = onTransition
        pass