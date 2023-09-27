import merparser as parser

class Tester:
    if __name__ == "__main__":
        stateDiagram = """
            stateDiagram-v2
                [*] --> startFunc
                st_myStateId0
                state "This is a description" as myStateId1
                myStateId2 : "State 2 description"

                st_myStateId0 --> myStateId1
                myStateId1 --> myStateId2: "Transition Description"
                endFunc --> [*]

        """

        state_diagram_lines = stateDiagram.split('\n')[1:]
        cleaned_state_diagram = '\n'.join(state_diagram_lines)

        parsed_diagram = parser.parse_state_diagram(cleaned_state_diagram)

        for i in parsed_diagram:
            print(i)
