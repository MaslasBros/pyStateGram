import re

from . import pyStatePatterns as Patterns
from .pyStateClasses import *

_excludedVersions = ['stateDiagram-v2', 'stateDiagram']
"""The versions of state diagrams to exclude from the state graph"""

def _detectUnsupportedFeatures(diagramStr: str):
    """
    Detects the unusupported features in the passed state diagram.

    Args:
        diagramStr (:class:`str`): The Mermaid JS diagram to parse

    Raises:
        (:class:`SyntaxError`): If any unsupported pattern is detected.
    """

    for ftr, msg in Patterns.unsupportedPatterns:
        if ftr in diagramStr:
            raise SyntaxError('Symbol: \'' + ftr + '\'. ' + msg)

    pass

def _createTransition(source: str, target:str, description:str) -> (str, Transition): 
    """
    Creates a Transition instance and the correcty formatted description of it.
    
    Args:
        source (:class:`str`): The source state name.
        target (:class:`str`): The target state name.
        description (:class:`str`): The description of the transition.

    Returns:
        Tuple containing the created Transition instance and the formatted description.
        Item1: Description
        Item2: Transition
    """
    tempTransition = Transition(source, target, lambda x:x)
    description = re.sub(r'[^a-zA-Z0-9_]+',  '_', description).replace(' ','').lower() if len(description) > 0 else str.lower(source + '_' + target) 

    return (description, tempTransition)

def _addToStates(statesDict: dict, stateKey:str, item) -> dict:
    """
    Adds the passed state name and item as a key-value pair in the passed dictionary.

    Args:
        statesDict (:class:`dict`): The dictionary to populate.
        stateKey (:class:`str`): The key string.
        item (:class:`func`): The value to associate with the key.

    Returns:
        The updated dictionary.

    Raises:
        (:class:`KeyError`): If any unsupported symbol is detected as a state ID
    """
    
    if stateKey == Patterns.startSymbol or stateKey == Patterns.endSymbol:
        raise KeyError('Key: \'' + stateKey + '\'.You can\'t use ' + Patterns.startSymbol + ' and ' + Patterns.endSymbol + ' as state IDs.')

    statesDict[stateKey] = item

    return statesDict

def parseStateDiagram(diagramStr: str) -> DiagramPackage:
    """
    Parses the passed mermaid.js and returns an object containing the two dictionaries of States and Transitions.

    Checks for unsupported features are also done through this method.

    The mermaid transitions are stored as a combination of the two state ID names as a key if there is not transition description
    else the key is the transition description.

    Args:
        diagramStr (:class:`str`): The diagram to parse

    Returns:
        The pyFsm.pyStateClasses.DiagramPackage containing the parsed states and transitions.
    
    Raises:
        (:class:`SyntaxError`): If any unsupported pattern is detected.
        (:class:`KeyError`): If any unsupported symbol is detected as a state ID
    """

    #Find the line index of stateDiagram-v2 or stateDiagram
    stateDiagramLines = diagramStr.split('\n')
    stateDiagramLines = [line.strip() for line in stateDiagramLines]

    lnIdx = -1
    for idx, line in enumerate(stateDiagramLines):
        if line in _excludedVersions:
            lnIdx = idx + 1
            break
    
    #Keep every line after the found line index of stateDiagram-v2 or stateDiagram
    cleanedStateDiagram = '\n'.join(stateDiagramLines[lnIdx:])

    #Raise appropriate errors if ANY unsupported feature gets detected in the diagram.
    _detectUnsupportedFeatures(diagramStr)

    states = {}
    transitions = {}

    for pattern in Patterns.patterns:
        matches = re.findall(pattern, cleanedStateDiagram)
        for match in matches:
            if pattern == Patterns.patterns[3]: # Pattern for the Transition
                source, target, description = match[0:3]
                tempTrans = _createTransition(source, target, description)
                transitions[tempTrans[0]] = tempTrans[1]
                # The two lines below here create two separate entries for each transition method in case they are not parsed elsewere.
                states = _addToStates(states, source, lambda x: x)
                states = _addToStates(states, target, lambda x: x)
            elif pattern == Patterns.patterns[2]: # Pattern for state with description after :
                source = match[0]
                states = _addToStates(states, source, lambda x: x)

            elif pattern == Patterns.patterns[4]: # Pattern for start func
                source = Patterns.startSymbol
                target = match[1]
                tempTrans = _createTransition(source, target, '')
                transitions[tempTrans[0]] = tempTrans[1]
                states[Patterns.startSymbol] = lambda x: x
                states[target] = lambda x: x
            elif pattern == Patterns.patterns[5]: # Pattern for end func
                source = Patterns.endSymbol
                target = match[0]
                tempTrans = _createTransition(target, source, '')
                transitions[tempTrans[0]] = tempTrans[1]
                states[Patterns.endSymbol] = lambda x: x
                states[target] = lambda x: x
            else: # Every other pattern can get directly created
                states = _addToStates(states, match, lambda x: x)

    return DiagramPackage(states, transitions)