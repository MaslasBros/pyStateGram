import re
from transition import Transition

def parse_state_diagram(diagram_str:str):
    # Regular expression pattern to match states, transitions and start/end symbols
    patterns = [r'(st_\w+)', #States
                #r'state (\w+|"\w+") as (\w+)', 
                r'(\w+) : (\w+|"\w+")']
                #r'(\w+) --> (\w+)', #Transitions
                #r'(\w+) --> (\w+): (\w+|"\w+")',
                #r'[\*] --> (\w+)', #Start, End funcs
                #r'(\w+) --> [\*]']
    
    parsed_diagram = {}
    for pattern in patterns:
        matches = re.findall(pattern, diagram_str)
        for match in matches:
            parsed_diagram[match] = lambda x: x

    #TODO: 

    return parsed_diagram