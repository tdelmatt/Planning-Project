from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (
    Node, Problem,
)
from aimacode.utils import expr
from lp_utils import (
    FluentState, encode_state, decode_state,
)
from my_planning_graph import PlanningGraph

from functools import lru_cache


class AirCargoProblem(Problem):
    def __init__(self, cargos, planes, airports, initial: FluentState, goal: list):
        """
        :param cargos: list of str
            cargos in the problem
        :param planes: list of str
            planes in the problem
        :param airports: list of str
            airports in the problem
        :param initial: FluentState object
            positive and negative literal fluents (as expr) describing initial state
        :param goal: list of expr
            literal fluents required for goal test
        """
        self.state_map = initial.pos + initial.neg
        self.initial_state_TF = encode_state(initial, self.state_map)
        Problem.__init__(self, self.initial_state_TF, goal=goal)
        self.cargos = cargos
        self.planes = planes
        self.airports = airports
        self.actions_list = self.get_actions()

    def get_actions(self):
        """
        This method creates concrete actions (no variables) for all actions in the problem
        domain action schema and turns them into complete Action objects as defined in the
        aimacode.planning module. It is computationally expensive to call this method directly;
        however, it is called in the constructor and the results cached in the `actions_list` property.

        Returns:
        ----------
        list<Action>
            list of Action objects
        """

        # TODO create concrete Action objects based on the domain action schema for: Load, Unload, and Fly
        # concrete actions definition: specific literal action that does not include variables as with the schema
        # for example, the action schema 'Load(c, p, a)' can represent the concrete actions 'Load(C1, P1, SFO)'
        # or 'Load(C2, P2, JFK)'.  The actions for the planning problem must be concrete because the problems in
        # forward search and Planning Graphs must use Propositional Logic

        def load_actions():
            """Create all concrete Load actions and return a list

            :return: list of Action objects
            """
            loads = []
            # TODO create all load ground actions from the domain Load action
            
            #I am still missing what I actually return here.  
            #okay I return a list of load ground actions from domain load action
            #what format are those in and where do I get them from
            
            #what is an action object
            #fly actions returns an action object, we can take a look at it
            
            
            #what the fuck does this entire program return in the first place.  
            #what is the purpose of this program
                #this program through the format of PDDL
                #searches a state space created by using actions to branch from state to state
                #to find a goal state
                
                #later we will implement a planning graph which helps find heuristics to solve the search, and actually solve the search
            
            
            #for all in airports
            for ap in self.airports:
                #for all in planes
                for pl in self.planes:
                    #for all in cargo
                    for cg in self.cargos:
                        #pos_preconditions =       
                        pos_preconditions = [expr("At({}, {})".format(cg, ap)), 
                                            expr("At({}, {})".format(pl, ap))] 
                        #neg_preconditions =
                        neg_preconditions = []
                        #effects_add = 
                        effects_add = [expr("In({}, {})".format(cg, pl))]
                        #effects_neg = 
                        effects_neg = [expr("At({}, {})".format(cg, ap))]
                        load = Action(expr("Load({}, {}, {})".format(cg, pl, ap)), 
                        [pos_preconditions, neg_preconditions], 
                        [effects_add, effects_neg])
                        loads.append(load)
            #print(loads)
            return loads

        def unload_actions():
            """Create all concrete Unload actions and return a list

            :return: list of Action objects
            """
            unloads = []
            #for all in airports
            for ap in self.airports:
                #for all in planes
                for pl in self.planes:
                    #for all in cargo
                    for cg in self.cargos:
                        #pos_preconditions =       
                        pos_preconditions = [expr("In({}, {})".format(cg, pl)), 
                                            expr("At({}, {})".format(pl, ap))] 
                        #neg_preconditions =
                        neg_preconditions = []
                        #effects_add = 
                        effects_add = [expr("At({}, {})".format(cg, ap))]
                        #effects_neg = 
                        effects_neg = [expr("In({}, {})".format(cg, pl))]
                        unload = Action(expr("Unload({}, {}, {})".format(cg, pl, ap)), 
                            [pos_preconditions, neg_preconditions], 
                            [effects_add, effects_neg])
                        unloads.append(unload)
            
            # TODO create all Unload ground actions from the domain Unload action
            #print(unloads)
            return unloads

        def fly_actions():
            """Create all concrete Fly actions and return a list

            :return: list of Action objects
            """
            flys = []
            for fr in self.airports:
                for to in self.airports:
                    if fr != to:
                        for p in self.planes:
                        
                            precond_pos = [expr("At({}, {})".format(p, fr)),
                                           ]
                            precond_neg = []
                            effect_add = [expr("At({}, {})".format(p, to))]
                            effect_rem = [expr("At({}, {})".format(p, fr))]
                            fly = Action(expr("Fly({}, {}, {})".format(p, fr, to)),
                                         [precond_pos, precond_neg],
                                         [effect_add, effect_rem])
                            flys.append(fly)
            return flys

        return load_actions() + unload_actions() + fly_actions()

    def actions(self, state: str) -> list:
        """ Return the actions that can be executed in the given state.

        :param state: str
            state represented as T/F string of mapped fluents (state variables)
            e.g. 'FTTTFF'
        :return: list of Action objects
        
        
        
        """
        # TODO implement
        """possible_actions = []
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        #for all actions
        for action in self.actions_list:
            possible = True
            #for all preconditions 
                #if that precondition is not met, then the action is not possible
            for precond in action.precond_pos:
                if precond not in kb.clauses:
                    possible = False
            for precond in action.precond_neg:
                if precond in kb.clauses:
                    possible = False
            #if action is possible, append the action to possible actions list
            if possible is True:
                possible_actions.append(action)
        #print(possible_actions)
        return possible_actions"""
        possible_actions = []
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for action in self.actions_list:
            is_possible = True
            for clause in action.precond_pos:
                if clause not in kb.clauses:
                    is_possible = False
            for clause in action.precond_neg:
                if clause in kb.clauses:
                    is_possible = False
            if is_possible:
                possible_actions.append(action)
        return possible_actions

    def result(self, state: str, action: Action):
        """ Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        :param state: state entering node
        :param action: Action applied
        :return: resulting state after action
        """
        # TODO implement
        """
        new_state = FluentState([], [])
        old_state = decode_state(state, self.state_map)
        
        #you remove the positive fluent
        #and you add it to the negative fluents as not being positive
        #I just dont understand why you cant just know if there is no positive fluent,
        #then that is the same as there being a negative fluent.  
        #it seems like the lists are redundant
        
        #assert action in self.actions(state)
        
        #add all old positive fluents by checking they are not in remove
        for fluent in old_state.pos:
            if fluent not in action.effect_rem:
                new_state.pos.append(fluent)
                
        #add all action effect fluents if they are not already in the state fluents 
        for fluent in action.effect_add:
            if fluent not in new_state.pos:
                new_state.pos.append(fluent)
                
        #add all old negative fluents by checking they are not in add
        for fluent in old_state.neg:
            if fluent not in action.effect_add:
                new_state.neg.append(fluent)
        
        #add any new negative fluents in action.remove by checking they are not already in old state fluents
        for fluent in action.effect_rem:
            if fluent not in new_state.neg:
                new_state.neg.append(fluent)
        
        
        return encode_state(new_state, self.state_map)
        """
        new_state = FluentState([], [])
        old_state = decode_state(state, self.state_map)
        #you remove the positive fluent
        #and you add it to the negative fluents as not being positive
        #I just dont understand why you cant just know if there is no positive fluent,
        #then that is the same as there being a negative fluent.  
        #it seems like the lists are redundant
        
        #add all old positive fluents by checking they are not in remove
        for fluent in old_state.pos:
            if fluent not in action.effect_rem:
                new_state.pos.append(fluent)
        
        #add all action effect fluents if they are not already in the state fluents 
        for fluent in action.effect_add:
            if fluent not in new_state.pos:
                new_state.pos.append(fluent)
        
        #add all old negative fluents by checking they are not in add
        
        #add any new negative fluents in action.remove by checking they are not already in old state fluents
        
        for fluent in old_state.neg:
            if fluent not in action.effect_add:
                new_state.neg.append(fluent)
                
        for fluent in action.effect_rem:
            if fluent not in new_state.neg:
                new_state.neg.append(fluent)
                
        return encode_state(new_state, self.state_map)
        
    def goal_test(self, state: str) -> bool:
        """ Test the state to see if goal is reached

        :param state: str representing state
        :return: bool
        """
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        # note that this is not a true heuristic
        h_const = 1
        return h_const

    @lru_cache(maxsize=8192)
    def h_pg_levelsum(self, node: Node):
        """This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of all actions that must be carried
        out from the current state in order to satisfy each individual goal
        condition.
        """
        # requires implemented PlanningGraph class
        pg = PlanningGraph(self, node.state)
        pg_levelsum = pg.h_levelsum()
        return pg_levelsum

    @lru_cache(maxsize=8192)
    def h_ignore_preconditions(self, node: Node):
        """This heuristic estimates the minimum number of actions that must be
        carried out from the current state in order to satisfy all of the goal
        conditions by ignoring the preconditions required for an action to be
        executed.
        """
        #question: isnt this still a search?  how do we know some minimum number of actions that achieves the goal, and where do we start here???
        #I would do something like 
        #bestaction = actions[1]
        #for  act in actions
            #if that act effects improve goal more than best action
                #bestaction = act
            #OR YOU COULD JUST DIRECTLY APPLY IT IF IT IMPROVES THE GOAL STATE    
            #if effects = needed parts of goal, then apply action
        
        
        #so it turns out that the minimum number of actions you could take is the number
        #of unsatisfied fluents in the goal in this problem domain.  Since we dont
        #have actions that can satisfy multiple fluents
        
        #for fluent in self.goal:
        #print(len(self.goal))
        a_state = decode_state(node.state, self.state_map)
        
        #    print(fluent)
        min = len(self.goal)
        for fluent in self.goal:
            for fluent1 in a_state.pos:
                #print("******")
                #print(fluent)
                #print(fluent1)
                #print("******")
                if fluent == fluent1:
                    #print("this happened")
                    min -=1
        return min
            
        
        
        
        
        
        
        
        # TODO implement (see Russell-Norvig Ed-3 10.2.3  or Russell-Norvig Ed-2 11.2)



def air_cargo_p1() -> AirCargoProblem:
    cargos = ['C1', 'C2']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO']
    pos = [expr('At(C1, SFO)'),
           expr('At(C2, JFK)'),
           expr('At(P1, SFO)'),
           expr('At(P2, JFK)'),
           ]
    neg = [expr('At(C2, SFO)'),
           expr('In(C2, P1)'),
           expr('In(C2, P2)'),
           expr('At(C1, JFK)'),
           expr('In(C1, P1)'),
           expr('In(C1, P2)'),
           expr('At(P1, JFK)'),
           expr('At(P2, SFO)'),
           ]
    init = FluentState(pos, neg)
    goal = [expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)


def air_cargo_p2() -> AirCargoProblem:
    # TODO implement Problem 2 definition
    cargos = ['C1', 'C2', 'C3']
    planes = ['P1', 'P2', 'P3']
    airports = ['JFK', 'SFO', 'ATL']
    pos = [expr('At(C1, SFO)'), expr('At(C2, JFK)'), expr('At(C3, ATL)'), 
    expr('At(P1, SFO)'), expr('At(P2, JFK)'), expr('At(P3, ATL)')]
    neg = [
           #airports cargo is not at
           expr('At(C1, JFK)'),
           expr('At(C1, ATL)'),
           expr('At(C2, SFO)'),
           expr('At(C2, ATL)'),
           expr('At(C3, SFO)'),
           expr('At(C3, JFK)'),
           
           #planes cargo is not in (all planes at beginning)
           expr('In(C1, P1)'),
           expr('In(C1, P2)'),
           expr('In(C1, P3)'),
           expr('In(C2, P1)'),
           expr('In(C2, P2)'),
           expr('In(C2, P3)'),
           expr('In(C3, P1)'),
           expr('In(C3, P2)'),
           expr('In(C3, P3)'),

           #airports planes are not at
           expr('At(P1, JFK)'),
           expr('At(P1, ATL)'),
           expr('At(P2, SFO)'),
           expr('At(P2, ATL)'),
           expr('At(P3, SFO)'),
           expr('At(P3, JFK)')
           ]
    init = FluentState(pos,neg)
    goal = [expr('At(C1, JFK)'), expr('At(C2, SFO)'), expr('At(C3, SFO)')]
    return AirCargoProblem(cargos, planes, airports, init, goal)

def air_cargo_p3() -> AirCargoProblem:
    # TODO implement Problem 3 definition
    cargos = ['C1', 'C2', 'C3', 'C4']
    planes = ['P1', 'P2']
    airports = ['JFK', 'SFO', 'ATL', 'ORD']
    pos = [expr('At(C1, SFO)'), expr('At(C2, JFK)'), expr('At(C3, ATL)'),
    expr('At(C4, ORD)'), expr('At(P1, SFO)'), expr('At(P2, JFK)')]
    
    neg = [
       #airports cargo is not at
       expr('At(C1, JFK)'),
       expr('At(C1, ATL)'),
       expr('At(C1, ORD)'),
       expr('At(C2, SFO)'),
       expr('At(C2, ATL)'),
       expr('At(C2, ORD)'),
       expr('At(C3, SFO)'),
       expr('At(C3, JFK)'),
       expr('At(C3, ORD)'),
       expr('At(C4, SFO)'),
       expr('At(C4, JFK)'),
       expr('At(C4, ATL)'),

       
       #planes cargo is not in (all planes at beginning)
       expr('In(C1, P1)'),
       expr('In(C1, P2)'),
       expr('In(C2, P1)'),
       expr('In(C2, P2)'),
       expr('In(C3, P1)'),
       expr('In(C3, P2)'),
       expr('In(C4, P1)'),
       expr('In(C4, P2)'),
    
       #airports planes are not at
       expr('At(P1, JFK)'),
       expr('At(P1, ATL)'),
       expr('At(P1, ORD)'),
       expr('At(P2, SFO)'),
       expr('At(P2, ATL)'),
       expr('At(P2, ORD)')
       ]
    
    init = FluentState(pos,neg)
    goal = [expr('At(C1, JFK)'), expr('At(C3, JFK)'), expr('At(C2, SFO)'), expr('At(C4, SFO)')]
    return AirCargoProblem(cargos, planes, airports, init, goal)
