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
class QLearnAgent(Agent):

    # Constructor, called when we start running the
    def __init__(self, alpha=0.001, epsilon=0.35, gamma=0.8, numTraining = 10):
        # alpha       - learning rate
        # epsilon     - exploration rate
        # gamma       - discount factor
        # numTraining - number of training episodes
        #
        # These values are either passed from the command line or are
        # set to the default values above. We need to create and set
        # variables for them
        self.r = -0.04
        self.food = []
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.gamma = float(gamma)
        self.numTraining = int(numTraining)
        self.s = ()
        self.a = ''        
        # Count the number of games we have played
        self.episodesSoFar = 0
        self.qvalues = []
        self.moves_num ={'North':0,'East':1,'South':2,'West':3}
    
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
    
    def setQvalues(self, qvalues):
        self.qvalues = qvalues
    
    def getQvalues(self):
        return self.qvalues
    
    def getEpsilon(self):
        return self.epsilon

    #Intialises the Q-values array
    #@params: state: The state of the agent
    def createNewQvalues(self,state):
        self.setQvalues(np.zeros((len(list(state.getFood())),
                                  len(list(state.getFood())[:][0]),4)))
        self.current_q = (np.zeros((len(list(state.getFood())),
                                  len(list(state.getFood())[:][0]),4)))        
        
    #Updates the Q-values of the state s based on the current state and the 
    #current action that the agent chose
    #@params: state: the current state of the agent
    #@params: pick: the action that the agent chooses in the current state
    def updateQvalues(self,state,pick):
        if(state.getPacmanPosition() in self.food):
            self.current_q[self.s[1]][self.s[0]][self.moves_num[self.a]]+= self.getAlpha()*(self.r + self.getGamma()*(5)-self.getQvalues()[self.s[1]][self.s[0]][self.moves_num[self.a]])
        elif(state.getPacmanPosition() in state.getGhostPositions()):
            self.current_q[self.s[1]][self.s[0]][self.moves_num[self.a]]+= self.getAlpha()*(self.r + self.getGamma()*(-5)-self.getQvalues()[self.s[1]][self.s[0]][self.moves_num[self.a]])
        else:
            self.current_q[self.s[1]][self.s[0]][self.moves_num[self.a]]+= (self.getAlpha()*(self.r + self.getGamma()*self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][self.moves_num[pick]]-
                     self.current_q[self.s[1]][self.s[0]][self.moves_num[self.a]]))
            
    #gets the next state of the agent.(Taken from game.Actions)
    #@params: position: the current position of the agent
    #@params: action: the direction in which the successor is to be found
    def getSuccessor(self, position, action):
        dx, dy = game.Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)

    def rounder(self,a):
        return round(a,2)
    # getAction
    #
    # The main method required by the game. Called every time that
    # Pacman is expected to move    
    def getAction(self, state):
        f = ()
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        
         #converting legal moves into numbers
        legal_move_num = [self.moves_num[mov] for mov in legal]        
        
        
        self.c = 100
        if(len(np.where(np.array(list(state.getFood())) == True))>1):
            food = np.where(np.array(list(state.getFood())) == True)
            if(len(food[:][0])>1):
                for i in range(len(np.where(np.array(list(state.getFood())) == True))):                    
                        f = [x[i] for x in food]                        
                        self.food.append(f)                        
            else:
                f = [x[0] for x in food]   
                self.food.append(f)        
                        
        # The data we have about the state of the game
        if(len(self.getQvalues())==0):
            self.createNewQvalues(state)
        print "Legal moves: ", legal
        print "Pacman position: ", state.getPacmanPosition()
        print "Ghost positions:" , state.getGhostPositions()
        print "Food locations: "
        print state.getFood()
        print "Score: ", state.getScore()
 
            
        # Now pick what action to take. For now a random choice among
        # the legal moves
            
        #when learning
        if(self.getEpisodesSoFar() < self.getNumTraining()):
            prop = random.random()
            if(self.s == ()):
                pick = random.choice(legal)
            #E-greedy
            elif(prop > 1 - self.getEpsilon()):
                pick = random.choice(legal)  
                self.updateQvalues(state, pick)
            else:
                maxq = max(self.qvalues[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][legal_move_num])                        
                ind = np.where(self.qvalues[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][legal_move_num] == maxq)[0]        
                if(len(ind) >1 ):                                
                    pick = legal[random.choice(ind)]
                else:

                    pick = legal[ind]
                    pick = legal[np.argmax(self.qvalues[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][legal_move_num])]                                  
                    self.updateQvalues(state, pick)
       #When doing actual runs
        else:

            ghost = state.getGhostPositions()[0]
            #magnifying the ghost so that the agent avoids it
            mag_ghost = [[ghost[0]+1,ghost[1]],[ghost[0],ghost[1]+1],[ghost[0]-1,ghost[1]],[ghost[0],ghost[1]-1]]
            mag_ghost.append(ghost)
            self.current_q = np.copy(self.getQvalues())
            rounder = np.vectorize(self.rounder)
            self.current_q = rounder(self.current_q)
            states = [self.getSuccessor(state.getPacmanPosition(),direc) for
                                         direc in legal]    
            state_restore_values = {}                   
            for st in states:
                if(st in mag_ghost):
                    state_restore_values[st]=self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][self.moves_num[game.Actions.vectorToDirection((st[0]-state.getPacmanPosition()[0],st[1]-state.getPacmanPosition()[1]))]]
                    self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][self.moves_num[game.Actions.vectorToDirection((st[0]-state.getPacmanPosition()[0],st[1]-state.getPacmanPosition()[1]))]] = -5                
            maxq = max(self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][legal_move_num])                        
            ind = np.where(self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][legal_move_num] == maxq)[0]        
            if(len(ind) > 1 ):                
                print 'ind1',ind
                pick = legal[random.choice(ind)]
            else:                
                pick = legal[ind]
            for st in state_restore_values.keys():
                self.current_q[state.getPacmanPosition()[1]][state.getPacmanPosition()[0]][self.moves_num[game.Actions.vectorToDirection((st[0]-state.getPacmanPosition()[0],st[1]-state.getPacmanPosition()[1]))]] = state_restore_values[st]
            print legal_move_num, legal
            print states,  mag_ghost
            
        # We have to return an action
        self.s = state.getPacmanPosition()
        self.a =  pick
        print state.getPacmanPosition()
        
        return pick    

    # Handle the end of episodes
    #
    # This is called by the game after a win or a loss.
    def final(self, state):
        #clearing the previous state and action variables
        self.s = ()
        self.a = ''
        print "A game just ended!"
        #setting the updated Q-values
        self.qvalues = np.copy(self.current_q)
        # Keep track of the number of games played, and set learning
        # parameters to zero when we are done with the pre-set number
        # of training episodes
        self.incrementEpisodesSoFar()
        if self.getEpisodesSoFar() == self.getNumTraining():
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
            self.setAlpha(0)
            self.setEpsilon(0)

