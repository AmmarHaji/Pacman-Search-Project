# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def minimaxFunction(self, depth, agent, gameState):
        #print "recurse called for agent: ",agentIndex, " , depth: ",depth
        if (gameState.isWin() or gameState.isLose() or depth > self.depth):
            return self.evaluationFunction(gameState)

        nextAction = []  # RM: stores the return value for this node actions
        action = gameState.getLegalActions(agent)  # Store the actions
        if Directions.STOP in action:
            action.remove(Directions.STOP)

        for a in action:
            successorGameState = gameState.generateSuccessor(agent, a)
            if((agent+1) >= gameState.getNumAgents()):
                nextAction += [self.minimaxFunction(depth+1, 0, successorGameState)]
            else:
                nextAction += [self.minimaxFunction(depth, agent+1, successorGameState)]


        if agent == 0:
            if(depth == 1): # if back to root, return action, else ret value
                bestScore = max(nextAction)
                length = len(nextAction)
                for i in range(length):
                    if (nextAction[i] == bestScore):
                        return action[i]
            else:
                valueAction = max(nextAction)

        elif agent > 0: # ghosts
            valueAction = min(nextAction)
        return valueAction
    
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxFunction(1,0,gameState) 
        
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectiMax(self,gameState,agent,depth):
        result = []

        # Terminate states
        if (not gameState.getLegalActions(agent)) or depth == self.depth:
            return self.evaluationFunction(gameState),0
       
        # All ghosts have finised one round: increase depth(last ghost) #
        if agent == gameState.getNumAgents() - 1:
            depth += 1

        # recursion through state tree

        # Final agent is pacman, rest are ghosts
        if agent+1 == gameState.getNumAgents():
            nextAgent = self.index
        else:
            nextAgent = agent + 1

        # Minimax 
        for action in gameState.getLegalActions(agent):
            if not result: 
                nextValue = self.expectiMax(gameState.generateSuccessor(agent,action),nextAgent,depth)
                # Checking if not pacman
                # All actions have the same probability, therefore prob = 1/p
                if(agent != self.index):
                    result.append((1.0 / len(gameState.getLegalActions(agent))) * nextValue[0])
                    result.append(action)
                else:
                    # Fix result with minimax value and action #
                    result.append(nextValue[0])
                    result.append(action)
            else:

                # PacMan agent max section
                previousValue = result[0] 
                nextValue = self.expectiMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                if agent == self.index:
                    if nextValue[0] > previousValue:
                        result[0] = nextValue[0]
                        result[1] = action

                # Min agent for ghosts
                else:
                    result[0] = result[0] + (1.0 / len(gameState.getLegalActions(agent))) * nextValue[0]
                    result[1] = action
        return result

    
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        return self.expectiMax(gameState,self.index,0)[1]
        util.raiseNotDefined()

