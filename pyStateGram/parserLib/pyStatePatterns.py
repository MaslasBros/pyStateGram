class Patterns:
    #Start and End function symbols
    startSymbol = '_start_'
    endSymbol = '_end_'

    # Regular expression pattern to match states, transitions and start/end symbols
    patterns = [r'\s+(\w+)\n', r'state\s+"[^"]+"\s+as\s+(\w+)', r'(\w+)\s+:\s+"([^"]+)"', #States
                r'(\w+)\s-->\s(\w+)(?::\s*"([^"]+)"?)?', #Transitions
                r'(\[\*\]\s-->)\s(\w+)', r'(\w+)\s(-->\s\[\*\])'] #Start, End funcs

    # Tuple list of the unsupported features of the parser along with their error messages. 
    unsupportedPatterns = [(r'<<choice>>', 'Choise states are not yet supported from the parser.'), #Choise state
                        (r'<<fork>>', 'Fork states are not yet supported from the parser.'), (r'<<join>>', 'Fork states are not yet supported from the parser.'), #Fork state
                        (r'{', 'Composite states are not yet supported from the parser.'), #Composite states
                        (r'}', 'Composite states are not yet supported from the parser.')] #Composite states
