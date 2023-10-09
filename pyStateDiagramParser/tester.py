import merparser as parser

class Tester:
    if __name__ == "__main__":
        #Test
        '''stateDiagram = """
            stateDiagram-v2
                [*] --> startState
                startState --> state1: Start to state 1
                state1 --> state2: "State 1 to state 2"
                state2 --> state3: State 2 to state 3
                state3 --> state4: "State 3 to state 4"
                state4 --> endState: "State 4 to end state"
                endState --> [*]
            """'''

        #Test   
        '''stateDiagram = """
            stateDiagram-v2
                [*] --> ss_start
                ss_start --> ss_state0: Start to state 0
                ss_state0 --> ss_state1: State 0 to state 1
                ss_state1 --> ss_state2: State 1 to state 2
                ss_state2 --> ss_state3: State 2 to state 3
                ss_state3 --> ss_end: State 3 to end state
                ss_end --> [*]
            """'''
        
        #Test
        '''stateDiagram = """
            stateDiagram-v2
                [*] --> startFunc
                myStateId0
                state "This is a description" as myStateId1
                myStateId2 : "State 2 description"

                myStateId0 --> myStateId1_concated
                myStateId1 --> myStateId2: "Transit to myState2 from myState1"
                endFunc --> [*]
            """'''
        
        #Testing on unsupported states
        stateDiagram = """
            stateDiagram-v2
                state fork_state <<fork>>
                    [*] --> fork_state
                    fork_state --> State2
                    fork_state --> State3
                pass
    
                state join_state <<join>>
                    State2 --> join_state
                    State3 --> join_state
                    join_state --> State4
                    State4 --> [*]
                pass

                [*] --> startState
                startState --> state1: Start to state 1
                state1 --> state2: "State 1 to state 2"
                state2 --> state3: State 2 to state 3
                state3 --> state4: "State 3 to state 4"
                state4 --> endState: "State 4 to end state"
                endState --> [*]

                state First {
                    [*] --> second
                    second --> [*]
}

                state if_state <<choice>>:
                [*] --> IsPositive
                IsPositive --> if_state
                if_state --> False: if n < 0
                if_state --> True : if n >= 0
                pass
                """

        parsedDiagram = parser.parseStateDiagram(stateDiagram)

        #Tests - Debugs
        keys = list(parsedDiagram.keys())

        for i in keys:
            print(i)

        #parsedDiagram['--> [*]'](print)("Hi")