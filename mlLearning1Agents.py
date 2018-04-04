# mlLearningAgents.py
# parsons/27-mar-2017
#
# A stub for a reinforcement learning agent to work with the Pacman
# piece of the Berkeley AI project:
#
# http://ai.berkeley.edu/reinforcement.html
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agent here was written by Simon Parsons, based on the code in
# pacmanAgents.py
# learningAgents.py

from pacman import Directions
from game import Agent
import random
import game
import util
import numpy as np

# QLearnAgent
#
class Q1LearnAgent(Agent):

    # Constructor, called when we start running the
    def __init__(self, alpha=0.25, epsilon=0.05, gamma=0.8, numTraining = 10):
        # alpha       - learning rate
        # epsilon     - exploration rate
        # gamma       - discount factor
        # numTraining - number of training episodes
        #
        # These values are either passed from the command line or are
        # set to the default values above. We need to create and set
        # variables for them
        self.food = []
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.gamma = float(gamma)
        self.numTraining = int(numTraining)
        # Count the number of games we have played
        self.episodesSoFar = 0
        self.policy = [[ch for ch in 'EEESSWWEESSWWWW']]
        self.policy.append([ch for ch in 'WSSSSEEEENNWW'])
        self.policy.append([ch for ch in 'EEESSWWEENNWWWWSSSS'])
        self.policy.append([ch for ch in 'WSSSSNNNNEEEESSWW'])
        self.utility=[]
        self.reward = 0.5
        self.index = 0
        self.directions = {'N':'North','E':'East','S':'South','W':'West'}
        self.policy_index = 0
        self.current_utility = []


    
    # Accessor functions for the variable episodesSoFars controlling learning
    def incrementEpisodesSoFar(self):
        self.episodesSoFar +=1

    def getEpisodesSoFar(self):
        return self.episodesSoFar

    def getNumTraining(self):
            return self.numTraining

    # Accessor functions for parameters
    def setEpsilon(self, value):
        self.epsilon = value

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, value):
        self.alpha = value
        
    def getGamma(self):
        return self.gamma

    def getMaxAttempts(self):
        return self.maxAttempts
    
    def createUtilities(self,state):
        self.utility = (np.zeros((len(list(state.getFood())),
                                  len(list(state.getFood())[:][0]))))
        self.current_utility = (np.zeros((len(list(state.getFood())),
                                  len(list(state.getFood())[:][0]))))
    
    def updateUtility(self,state):
        self.reward = 0.05
        self.getFood(state)            
        if(state.getPacmanPosition() in state.getGhostPositions()):
            self.current_utility[self.previous_state[1]][self.previous_state[0]]+=self.alpha*(
                    self.reward+(self.getGamma()*(-5))
                    -self.current_utility[self.previous_state[1]][self.previous_state[0]])
        elif(state.getPacmanPosition() in self.food):
            self.current_utility[self.previous_state[1]][self.previous_state[0]]+=self.alpha*(
                    self.reward+(self.getGamma()*5)-
                    self.current_utility[self.previous_state[1]][self.previous_state[0]])
        else:
            if(self.current_utility[self.previous_state[1]][self.previous_state[0]]==0.0):
                self.current_utility[self.previous_state[1]][self.previous_state[0]]=self.reward
            else:
                self.current_utility[self.previous_state[1]][self.previous_state[0]]+=self.alpha*(
                        self.reward+(self.getGamma()*self.current_utility[state.getPacmanPosition()[1]]
                        [state.getPacmanPosition()[0]])-
                        self.current_utility[self.previous_state[1]][self.previous_state[0]])
        
    def getFood(self,state):
        food = np.where(np.array(list(state.getFood())) == True)
        if(len(food[:][0])>1):
            for i in range(len(np.where(np.array(list(state.getFood())) == True))):                    
                    f = [x[i] for x in food]                        
                    self.food.append(f)                        
        else:
            f = [x[0] for x in food]   
            self.food.append(f)
    
    def getSuccessor(self, position, action):
        dx, dy = game.Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)

    # getAction
    #
    # The main method required by the game. Called every time that
    # Pacman is expected to move
    def getAction(self, state):

        # The data we have about the state of the game
        if(self.utility == []):
            self.createUtilities(state)
        legal = state.getLegalPacmanActions()        
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
        print "Legal moves: ", legal
        print "Pacman position: ", state.getPacmanPosition()
        print "Ghost positions:" , state.getGhostPositions()
        print "Food locations: "
        print state.getFood()
        print "Score: ", state.getScore()
 
            
        # Now pick what action to take. For now a random choice among
        # the legal moves
        if(self.episodesSoFar <self.getNumTraining()):
            pick = self.directions[self.policy[self.policy_index][self.index]]        
            if(self.index > 0):
                self.updateUtility(state)                
                
            self.previous_state = state.getPacmanPosition()    
            
            # We have to return an action
            self.index+=1
        elif(state.getPacmanPosition() not in state.getGhostPositions()): 
            self.current_utility = np.copy(self.utility)
            self.current_utility[state.getGhostPositions()[0][1]][state.getGhostPositions()[0][0]] = -5
            self.current_utility[state.getGhostPositions()[0][1]+1][state.getGhostPositions()[0][0]] = -5            
            self.current_utility[state.getGhostPositions()[0][1]][state.getGhostPositions()[0][0]+1] = -5            
            self.current_utility[state.getGhostPositions()[0][1]-1][state.getGhostPositions()[0][0]] = -5
            self.current_utility[state.getGhostPositions()[0][1]][state.getGhostPositions()[0][0]-1] = -5
            states = [self.getSuccessor(state.getPacmanPosition(),direc) for
                                         direc in legal]
            print states
            pick = legal[np.argmax([self.current_utility[st[1]][st[0]]for st in states])]
        return pick
            

    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):

        print "A game just ended!"
        self.index = 0
        self.policy_index = random.choice([0,1,2,3])
        if(state.data.score > 0):
            self.utility = np.copy(self.current_utility)
        else:            
            self.current_utility = np.copy(self.utility)
        print self.utility
        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)


