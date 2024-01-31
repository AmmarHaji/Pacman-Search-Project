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
    s = problem.getStartState()
    #frontier for the list of possible actions
    frontier = util.Stack()
    #keeping track of action list
    listaction=[]
    #keeping track of explored list
    explored=[]
    frontier.push((s,listaction))
    while frontier:
        currstate,action=frontier.pop()
        if not currstate in explored:
            explored.append(currstate)
            if problem.isGoalState(currstate):
                return action
            for successor in problem.getSuccessors(currstate):
                coord,location,cost=successor
                nextstate= action+[location]
                frontier.push((coord,nextstate))
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    s=problem.getStartState()
    #frontier for the list of possible actions
    frontier=util.Queue()
    #keeping track of action list
    listaction=[]
    #keeping track of explored list
    explored=[]
    frontier.push((s,listaction))
    while frontier:
        currstate,action=frontier.pop()
        if not currstate in explored:
            explored.append(currstate)
            if problem.isGoalState(currstate):
                return action
            for successor in problem.getSuccessors(currstate):
                coord,location,cost=successor
                nextstate=action+[location]
                frontier.push((coord,nextstate))
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    s=problem.getStartState()
    frontier = util.PriorityQueue()
    listaction = []
    exploredList = []
    frontier.push((s, listaction), problem)
    while frontier:
        currstate, action = frontier.pop()
        if not currstate in exploredList:
            exploredList.append(currstate)
            if problem.isGoalState(currstate):
                return action
            for successor in problem.getSuccessors(currstate):
                coord, location, cost = successor
                nextstate = action + [location]
                nextcost = problem.getCostOfActions(nextstate)
                frontier.push((coord, nextstate), nextcost)
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    s = problem.getStartState()
    #frontier for the list of possible actions
    frontier = util.PriorityQueue()
    #set up this way to keep consistent with the structure of successors
    frontier.push((s,[],0), heuristic(s,problem))
    #keeping track of explored list
    explored = []
    while(not frontier.isEmpty()):
        #same structure as successors
        currstate, actions, cost = frontier.pop()
        #checking if goal state
        if problem.isGoalState(currstate):
            return actions
        #a* search begins here
        if currstate not in explored:
            explored.append(currstate)
            #traversing through all successors
            for nextstate, action, stepcost in problem.getSuccessors(currstate):
                if nextstate not in explored:
                    path = list(actions) +[action]
                    #heuristic for a*
                    nextcost = problem.getCostOfActions( path) + heuristic(nextstate, problem)
                    #cost doesnt matter in frontier since we are using getCostofActions instead and it acts as value in priorityqueue
                    frontier.push((nextstate,path,0),nextcost)
            
    
    return []
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
