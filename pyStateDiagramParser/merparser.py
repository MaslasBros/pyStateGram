import re

# Regular expression pattern to match states, transitions and start/end symbols
patterns = [r'\t\w+\n', r'state\s+"[^"]+"\s+as\s+(\w+)', r'(\w+)\s+:\s+"([^"]+)"', #States
            r'(\w+)\s-->\s(\w+)(?::\s*"([^"]+)"?)?', #Transitions
            r'(\[\*\]\s-->)\s(\w+)', r'(\w+)\s(-->\s\[\*\])'] #Start, End funcs


unsupportedPatterns = [r'state\s+(\w+)\s+\{(?:.*\n)*?\s*\}', # Composite states
            r'state\s(\w+)\s<<choice>>:([\s\S\d\w]*)pass', #Choices
            r'state\s(\w+)\s<<fork>>:\s+([\s\S\d\w]*)pass\n+\s*state\s(\w+)\s<<join>>:\s+([\s\S\d\w]*)pass'] #Fork states

startSymbol = '[*]->'
endSymbol = '->[*]'

class Transition:
    def __init__(self, source, target, onTransition):
        self.source = source
        self.target = target
        self.onTransition = onTransition
        pass

def parseStateDiagram(diagramStr: str) -> dict:
    """
    Parses the passed mermaid.js and returns a dictionary with the state IDs as keys 
    and empty lambda methods as values.\n
    The mermaid transitions are stored as a combination of the two state ID names as a key if there is not transition description
    else the key is the transition description.\n
    The value is a Transition object.
    """

    #Remove the stateDiagram-(v2) from the start of the state graph
    stateDiagramLines = diagramStr.strip().split('\n')[1:]
    cleanedStateDiagram = '\n'.join(stateDiagramLines)

    #Remove the unsupported detected features
    combinedUnsupported = '|'.join(unsupportedPatterns)
    cleanedStateDiagram = re.sub(combinedUnsupported, '', diagramStr)

    parsedPairs = {}

    for pattern in patterns:
        matches = re.findall(pattern, cleanedStateDiagram)
        for match in matches:
            if pattern == patterns[3]: # Pattern for the Transition
                source, target, description = match[0:3]
                transition = Transition(source, target, lambda x:x)
                parsedPairs[description if len(description) > 0 else str.lower(source + '_' + target)] = transition
        # The two lines below here create two separate entries for each transition method in case they are not parsed elsewere.
                parsedPairs[source] = lambda x: x
                parsedPairs[target] = lambda x: x
            elif pattern == patterns[2]: # Pattern for state with description after :
                source = match[0]
                parsedPairs[source] = lambda x: x
            elif pattern == patterns[4]: # Pattern for start func
                func = match[1]
                parsedPairs[startSymbol] = lambda x: x
                parsedPairs[func] = lambda x: x
            elif pattern == patterns[5]: # Pattern for end func
                func = match[0]
                parsedPairs[endSymbol] = lambda x: x
                parsedPairs[func] = lambda x: x
            else: # Every other pattern can get directly created
                parsedPairs[match] = lambda x: x

    return parsedPairs