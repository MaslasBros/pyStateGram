import re

# Regular expression pattern to match states, transitions and start/end symbols
patterns = [r'ss_\w+', r'state\s+"[^"]+"\s+as\s+(\w+)', r'(\w+)\s+:\s+"([^"]+)"', #States
            r'(\w+)\s-->\s(\w+)(?::\s*"([^"]+)"?)?', #Transitions
            r'\[\*\]\s-->\s(\w+)', r'(\w+)\s-->\s\[\*\]'] #Start, End funcs

class Transition:
    def __init__(self, source, target, onTransition = None):
        self.source = source
        self.target = target
        self.onTransition = onTransition if onTransition is not None else onTransition
        pass

def parseStateDiagram(diagram_str: str) -> dict:
    """
    Parses the passed mermaid.js and returns a dictionary with the state IDs as keys 
    and empty lambda methods as values.\n
    The mermaid transitions are stored as a combination of the two state ID names as a key if there is not transition description
    else the key is the transition description.\n
    The value is a Transition object.
    """

    parsedPairs = {}

    for pattern in patterns:
        matches = re.findall(pattern, diagram_str)
        for match in matches:
            if pattern == patterns[3]: # Pattern for the Transition
                source, target, description = match
                transition = Transition(source, target)
                parsedPairs[description if len(description) > 0 else str.lower(source + '_' + target)] = transition
                parsedPairs[source] = lambda x: x
                parsedPairs[target] = lambda x: x
            elif pattern == patterns[2]: # Pattern for state with description after :
                source, desc = match
                parsedPairs[source] = lambda x: x
            elif pattern == patterns[len(patterns) - 2]:
                parsedPairs["[*]-"] = lambda x: x
            elif pattern == patterns[len(patterns) - 1]:
                parsedPairs["-[*]"] = lambda x: x
            else: # Every other pattern can get directly created
                parsedPairs[match] = lambda x: x

    return parsedPairs