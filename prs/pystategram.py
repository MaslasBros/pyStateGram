import re
from .parserLib import pyStateClasses as pClass
from .parserLib import pyStatePatterns as pPattern

def detectUnsupportedFeatures(diagramStr: str):
    """
    Detects the unusupported features in the passed state diagram.\n
    If any is found, its appropriate error is immediately thrown in the console.
    """

    for ftr, msg in pPattern.unsupportedPatterns:
        if ftr in diagramStr:
            raise SyntaxError('Symbol: \'' + ftr + '\'. ' + msg)

    pass

def createTransition(source: str, target:str, description:str) -> (str, pClass.Transition):
    """
    Creates a Transition instance and the correcty formatted description of it.\n
    Returns a Tuple containing the created Transition instance and the formatted description.\n
    Item1: Description
    Item2: Transition\n
    """
    tempTransition = pClass.Transition(source, target, lambda x:x)
    description = re.sub(r'[^a-zA-Z0-9_]+',  '_', description).replace(' ','').lower() if len(description) > 0 else str.lower(source + '_' + target) 

    return (description, tempTransition)

def addToStates(statesDict: dict, stateKey:str, item) -> dict:

    if stateKey == pPattern.startSymbol or stateKey == pPattern.endSymbol:
        raise KeyError('Key: \'' + stateKey + '\'.You can\'t use ' + pPattern.startSymbol + ' and ' + pPattern.endSymbol + ' as state IDs.')

    statesDict[stateKey] = item

    return statesDict

def parseStateDiagram(diagramStr: str) -> pClass.DiagramPackage:
    """
    Parses the passed mermaid.js and returns a n object containing the two dictionaries of States and Transitions.\n
    Checks for unsupported features are also done through this method.\n
    The mermaid transitions are stored as a combination of the two state ID names as a key if there is not transition description
    else the key is the transition description.\n
    """

    #Remove the stateDiagram-(v2) from the start of the state graph
    stateDiagramLines = diagramStr.strip().split('\n')[1:]
    cleanedStateDiagram = '\n'.join(stateDiagramLines)

    #Raise appropriate events if ANY unsupported feature gets detected in the diagram.
    detectUnsupportedFeatures(diagramStr)

    states = {}
    transitions = {}

    for pattern in pPattern.patterns:
        matches = re.findall(pattern, cleanedStateDiagram)
        for match in matches:
            if pattern == pPattern.patterns[3]: # Pattern for the Transition
                source, target, description = match[0:3]
                tempTrans = createTransition(source, target, description)
                transitions[tempTrans[0]] = tempTrans[1]
                # The two lines below here create two separate entries for each transition method in case they are not parsed elsewere.
                states = addToStates(states, source, lambda x: x)
                states = addToStates(states, target, lambda x: x)
            elif pattern == pPattern.patterns[2]: # Pattern for state with description after :
                source = match[0]
                states = addToStates(states, source, lambda x: x)

            elif pattern == pPattern.patterns[4]: # Pattern for start func
                source = pPattern.startSymbol
                target = match[1]
                tempTrans = createTransition(source, target, '')
                transitions[tempTrans[0]] = tempTrans[1]
                states[pPattern.startSymbol] = lambda x: x
                states[target] = lambda x: x
            elif pattern == pPattern.patterns[5]: # Pattern for end func
                source = pPattern.endSymbol
                target = match[0]
                tempTrans = createTransition(target, source, '')
                transitions[tempTrans[0]] = tempTrans[1]
                states[pPattern.endSymbol] = lambda x: x
                states[target] = lambda x: x
            else: # Every other pattern can get directly created
                states = addToStates(states, match, lambda x: x)

    return pClass.DiagramPackage(states, transitions)