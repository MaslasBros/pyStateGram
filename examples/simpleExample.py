from pyStateGram.pystategram import * 

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
'''stateDiagram = """
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
        
        _start_
            MyState1
            MyState2

            [*] --> Still
            Still --> [*]
            Still --> Moving: "Hiya There"
            Moving --> Still
            Moving --> Crash
            Crash --> [*]
        """'''

#Test
'''stateDiagram = """
        ---
        title: Simple sample
        ---
        stateDiagram-v2
            2_start_
            MyState1
            MyState2

            [*] --> Still
            Still --> [*]
            Still --> Moving: "Hiya There"
            Moving --> Still
            Moving --> Crash
            Crash --> [*]
        """'''

stateDiagram = """
        ---
        title: Simple sample
        dasasd
        adas
        da
    
        ---
        stateDiagram-v2
            Idle
            Load
            Release
            Aim
            Fire
            
            Idle --> Hello_1: "transitHello"
            Idle --> Release
            Load --> Aim
            Aim --> Fire
            Fire --> Hello_2
        """

#Parsing
diagramPackage = parseStateDiagram(stateDiagram)

#Tests - Debugs
for i in diagramPackage.states:
    print('State: '+ i)

for i in diagramPackage.transitions.items():
    print('Transition: '+ str(i))

""" print(diagramPackage.transitions['hiya_there'].source)
print(diagramPackage.transitions['hiya_there'].target)
diagramPackage.transitions['hiya_there'].onTransition(print)("Hello from transition") """