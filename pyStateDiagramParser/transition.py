class Transition:
    def __init__(self, source:function, target:function, onTransition:function):
        self.source = source
        self.target = target
        self.onTransition = onTransition
        pass