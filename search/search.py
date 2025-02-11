# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #DFS
    # initialize stack and visited set
    fringe = util.Stack()
    closed = set()

    # set the initial state and add to fringe
    initial_state = problem.getStartState()
    initial_actions = [] # an empty array, initially no actions have been performed
    fringe.push((initial_state, initial_actions)) # ((x,y), [array of actions]) 

    # loop 
    while True:
        # check if all explored
        if fringe.isEmpty():
            return []
        
        # get current state and path
        current_state, path = fringe.pop()

        # check if our current state is the goal
        if (problem.isGoalState(current_state)):
            return path

        # add this state to the closed note
        if current_state not in closed:
            closed.add(current_state)

        # push all successors of this state to the fringe
        for successor, new_path, cost in problem.getSuccessors(current_state):
            if successor not in closed:
                fringe.push((successor, (path + [new_path])))
                # closed.add(successor) # works without this?
 
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #BFS
    # initialize queue and visited set
    fringe = util.Queue()
    closed = set()

    # set the initial state and add to fringe
    initial_state = problem.getStartState()
    initial_actions = [] # an empty array, initially no actions have been performed
    fringe.push((initial_state, initial_actions)) # ((x,y), [array of actions]) 

    # loop 
    while True:
        # check if all explored
        if fringe.isEmpty():
            return []
        
        # get current state and path
        current_state, path = fringe.pop()

        # check if our current state is the goal
        if (problem.isGoalState(current_state)):
            return path

        # add this state to the closed note
        if current_state not in closed:
            closed.add(current_state)

        # push all successors of this state to the fringe
        for successor, new_path, cost in problem.getSuccessors(current_state):
            if successor not in closed:
                fringe.push((successor, (path + [new_path])))
                closed.add(successor)
    
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # initialize queue and visited set
    fringe = util.PriorityQueue()
    closed = set()

    # set the initial state and add to fringe
    initial_state = problem.getStartState()
    initial_actions = []
    initial_priority = 0
    fringe.update((initial_state, initial_actions), initial_priority)

    # loop 
    while True:
        # check if all explored
        if fringe.isEmpty():
            return []
        
        # get current state, path, and cost
        (current_state, path) = fringe.pop()

        # check if our current state is the goal
        if problem.isGoalState(current_state):
            return path

        # add this state to the closed note if not already explored
        if current_state not in closed:
            closed.add(current_state)

            # push all successors of this state to the fringe
            for successor, new_path, new_cost in problem.getSuccessors(current_state):
                if successor not in closed:
                    successor_path = path + [new_path]
                    successor_cost = problem.getCostOfActions(successor_path)
                    # fringe update automatically accounts for cost.
                    fringe.update((successor, successor_path), successor_cost)
    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # initialize queue and visited set
    fringe = util.PriorityQueue()
    closed = set()

    # set the initial state and add to fringe
    initial_state = problem.getStartState()
    initial_actions = []
    g_cost = 0  # Initial path cost
    h_cost = heuristic(initial_state, problem)  # Initial heuristic estimate
    f_cost = g_cost + h_cost  # f(n) = g(n) + h(n)
    
    fringe.update((initial_state, initial_actions), f_cost)

    while True:
        # check if all explored
        if fringe.isEmpty():
            return []
        
        # get current state, path, and cost
        (current_state, path) = fringe.pop()

        # check if our current state is the goal
        if problem.isGoalState(current_state):
            return path
        
        # add this state to the closed note if not already explored
        if current_state not in closed:
            closed.add(current_state)

            # push all successors of this state to the fringe
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in closed:
                    successor_path = path + [action]
                    g_cost = problem.getCostOfActions(successor_path)  # True cost to reach successor
                    h_cost = heuristic(successor, problem)  # Heuristic estimate to goal
                    f_cost = g_cost + h_cost  # Total cost f(n) = g(n) + h(n)
                    
                    fringe.update((successor, successor_path), f_cost)
    
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
