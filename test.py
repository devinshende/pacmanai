import random
from copy import copy

from pacai.agents.capture.capture import CaptureAgent

class testAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at `pacai.core.baselineTeam` for more details about how to create an agent.
    """

    def __init__(self, index, isRed, **kwargs):
        super().__init__(index, **kwargs)
        self.isRed = isRed

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)
        if self.index % 2 == 1:
            self.enemyIndex = self.index - 1
        else:
            self.enemyIndex = self.index + 1
        self.gameWidth = gameState.getInitialLayout().width
        self.gameHeight = gameState.getInitialLayout().height
        self.middle = self.gameWidth / 2
        self.border = []
        for y in range(self.gameHeight):
            if not gameState.hasWall(int(self.middle - 1), y) and not gameState.hasWall(int(self.middle), y):
                if self.isRed:
                    self.border.append( ( (self.middle - 1, y), (self.middle, y) ) )
                else:
                    self.border.append( ( (self.middle, y), (self.middle - 1, y) ) )

        # Your initialization code goes here, if you need any.
    def chooseAction(self, gameState):
        # print("INDEX: ",self.index)
        # print("Grabbed indices: ",self.index, self.enemyIndex)
        returnMe = "Stop"
        selfPos = gameState.getAgentPosition(self.index)
        enemyPos = gameState.getAgentPosition(self.enemyIndex)
        ghostManhattans = {}
        for i in self.getOpponents(gameState):
            e = gameState.getAgentPosition(i)
            ghostManhattans[i] = abs(selfPos[0] - e[0]) + abs(selfPos[1] - e[1])

        bestDist = 9999999
        bestFood = None
        for i in self.getFood(gameState).asList():
            cur = abs(i[0] - selfPos[0]) + abs(i[1] - selfPos[1])
            if cur < bestDist:
                bestDist = cur
                bestFood = i

        enemyDistances = {}
        for i in self.border:
            enemyDistances[i[0]] = abs(enemyPos[0] - i[1][0]) + abs(enemyPos[1] - i[1][1])
            # if (self.isRed and enemyPos[0] < self.middle * 1.5 ) or (not self.isRed and enemyPos > self.middle/2):
            #     enemyDistances[i[0]] = self.breadthFirstSearch(gameState, self.enemyIndex, i[1], self.manhattanHeuristic)[1]
            # else:
            #     enemyDistances[i[0]] = abs(enemyPos[0] - i[1][0]) + abs(enemyPos[1] - i[1][1])
        guardSpot = min(enemyDistances, key=enemyDistances.get)

        #get the closest food to the enemy
        enFoodDistances = {}
        for food in self.getFoodYouAreDefending(gameState).asList() + self.getCapsulesYouAreDefending(gameState):
            enFoodDistances[food] = abs(enemyPos[0] - food[0]) + abs(enemyPos[1] - food[1])
        predictedSpot = min(enFoodDistances, key=enFoodDistances.get)

        if self.isRed and enemyPos[0] < self.middle:
            xDiff = enemyPos[0] - selfPos[0]
            yDiff = enemyPos[1] - selfPos[1]
            if xDiff == 1 and yDiff == 0:
                return 'East'
            if xDiff == -1 and yDiff == 0:
                return 'West'
            if yDiff == 1 and xDiff == 0;
                return 'North'
            if yDiff == -1 and xDiff == 0:
                return 'South'
            return self.defensiveBreadthFirstSearch(gameState, self.index, enemyPos, self.noHeuristic)[0]
        elif not self.isRed and enemyPos[0] >= self.middle:
            xDiff = enemyPos[0] - selfPos[0]
            yDiff = enemyPos[1] - selfPos[1]
            if xDiff == 1:
                return 'East'
            if xDiff == -1:
                return 'West'
            if yDiff == 1:
                return 'North'
            if yDiff == -1:
                return 'South'

            return self.defensiveBreadthFirstSearch(gameState, self.index, enemyPos, self.noHeuristic)[0]

        if self.index > 1 and gameState.getScore() < 1 and ghostManhattans[self.enemyIndex] > 2:
            if self.isRed and selfPos[0] > self.middle/2:
                return self.foodBreadthFirstSearch(gameState, self.index, bestFood, self.noHeuristic)[0]
            elif not self.isRed and selfPos[0] < self.middle + (self.middle / 2):
                return self.foodBreadthFirstSearch(gameState, self.index, bestFood, self.noHeuristic)[0]





        newEnemyPos = guardSpot
        newState = copy(gameState)

        for i in range(10):
            adjacent = newState.getLegalActions(self.enemyIndex)
            adjacent.remove('Stop')
            if len(adjacent) == 0:
                newEnemyPos = newState.getAgentPosition(self.enemyIndex)
                break
            chosenAction = None
            if self.isRed:
                if 'West' in adjacent:
                    chosenAction = 'West'
                elif 'East' in adjacent:
                    if len(adjacent) == 1:
                        chosenAction = 'East'
                    else:
                        adjacent.remove('East')
                        chosenAction = random.choice(adjacent)
                else:
                    chosenAction = random.choice(adjacent)
            if not self.isRed:
                if 'East' in adjacent:
                    chosenAction = 'East'
                elif 'West' in adjacent:
                    if len(adjacent) == 1:
                        chosenAction = 'West'
                    else:
                        adjacent.remove('West')
                        chosenAction = random.choice(adjacent)
                else:
                    chosenAction = random.choice(adjacent)
            newState = newState.generateSuccessor(self.enemyIndex, chosenAction)

        newEnemyPos = newState.getAgentPosition(self.enemyIndex)
        if self.isRed and selfPos[0] >= self.middle:
            return self.breadthFirstSearch(gameState, self.index, guardSpot, self.noHeuristic)[0]
        elif not self.isRed and selfPos[0] <= self.middle:
            return self.breadthFirstSearch(gameState, self.index, guardSpot, self.noHeuristic)[0]

        if ghostManhattans[self.enemyIndex] > 4:
            return self.breadthFirstSearch(gameState, self.index, guardSpot, self.noHeuristic)[0]
        else:
            return self.defensiveBreadthFirstSearch(gameState, self.index, guardSpot, self.noHeuristic)[0]
        #print("Done! Guarding: ",guardSpot)

    def breadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        counter = 0
        while True:
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) == target:
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop",0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)

            tempActions = currentState.getLegalActions(index)
            for action in tempActions:
                succ = currentState.generateSuccessor(index, action)
                if succ in exploredPaths or succ.getAgentPosition(index) in exploredNodes or succ in frontier:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                frontier = self.priorityPush(frontier, succ, currentCost + heuristic(succ, index, target) )
            if not frontier:
                #print("empty frontier")
                return ("Stop",0)
            # counter += 1
            # if counter >= 90000:
            #     print("uh oh, exeeded limit!")
            #     return False


    def defensiveBreadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        counter = 0
        while True:
            #     print("Frontier: ")
            #     for i in frontier:
            #         print(i.getAgentPosition(index),end=", ")
            #     print("\n")
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) == target:
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop",0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)
            for action in currentState.getLegalActions(index):
                succ = currentState.generateSuccessor(index, action)
                xVal = succ.getAgentPosition(index)[0]
                if xVal < self.middle and not self.isRed:
                    continue
                if xVal > self.middle - 1 and self.isRed:
                    continue
                if succ in exploredPaths or succ.getAgentPosition(index) in exploredNodes or succ in frontier:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                frontier = self.priorityPush(frontier, succ, currentCost + heuristic(succ, index, target) )
            if not frontier:
                # print("empty frontier")
                return ("Stop",0)
            # counter += 1
            # if counter >= 90000:
            #     print("uh oh, exeeded limit!")
            #     return False

    def foodBreadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        counter = 0
        while True:
            #     print("Frontier: ")
            #     for i in frontier:
            #         print(i.getAgentPosition(index),end=", ")
            #     print("\n")
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) in self.getFood(gameState).asList():
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop",0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)
            for action in currentState.getLegalActions(index):
                succ = currentState.generateSuccessor(index, action)
                if succ in exploredPaths or succ.getAgentPosition(index) in exploredNodes or succ in frontier:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                frontier = self.priorityPush(frontier, succ, currentCost + heuristic(succ, index, target) )
            if not frontier:
                #print("empty frontier")
                return ("Stop",0)
            counter += 1
            if counter >= 90000:
                print("uh oh, exeeded limit!")
                return False


    def middleHeuristic(self, gameState, index, target = None):
        return abs(gameState.getAgentPosition(index)[0] - self.middle)

    def noHeuristic(self, gameState, index, target = None):
        return 1

    def enemyHeuristic(self, gameState, index, target = None):
        xDiff = abs(gameState.getAgentPosition(index)[0] - gameState.getAgentPosition(self.enemyIndex)[0])
        yDiff = abs(gameState.getAgentPosition(index)[1] - gameState.getAgentPosition(self.enemyIndex)[1])
        return (xDiff + yDiff)

    def manhattanHeuristic(self, gameState, index, target):
        selfPos = gameState.getAgentPosition(index)
        return abs(selfPos[0] - target[0]) + abs(selfPos[1] - target[1])

    def euclidianHeuristic(self, gameState, index, target):
        selfPos = gameState.getAgentPosition(index)
        return pow( pow(selfPos[0] - target[0], 2) + pow(selfPos[1] - target[1], 2), 0.5)

    def inGhostMode(self, gameState, agentIndex):
        agentPos = gameState.getAgentPosition(agentIndex)
        gameWidth = gameState.getInitialLayout().width
        if agentIndex % 2 == 0 and agentPos[0] < gameWidth / 2:  #blue team case
            return True
        if agentIndex % 2 == 1 and agentPos[0] > gameWidth / 2:
            return True
        return False

    def priorityPush(self, queue, input, priority):
        for i in range(len(queue)):
            if queue[i][1] > priority:
                queue.insert(i, (input, priority))
                return queue
        queue.append((input, priority))
        return queue
