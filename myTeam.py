from pacai.agents.capture.capture import CaptureAgent

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.student.test.testAgent',
        second = 'pacai.student.test.testAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    # firstAgent = reflection.qualifiedImport(first)
    # secondAgent = reflection.qualifiedImport(second)
    return [
        testAgent(firstIndex, isRed),
        testAgent(secondIndex, isRed),
    ]

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
            tempL = int(self.middle - 1)
            tempR = int(self.middle)
            if not gameState.hasWall(tempL, y) and not gameState.hasWall(tempR, y):
                bLeft = self.middle - 1
                bRight = self.middle
                if self.isRed:
                    self.border.append(((bLeft, y), (bRight, y)))
                else:
                    self.border.append(((bRight, y), (bLeft, y)))

        # Your initialization code goes here, if you need any.
    def chooseAction(self, gameState):
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

        defenseTies = []
        for i in enemyDistances:
            if enemyDistances[i] == min(enemyDistances.values()):
                defenseTies.append(i)
        if len(defenseTies) == 1:
            guardSpot = defenseTies[0]
        else:
            closest = None
            middleDist = 99999
            for i in defenseTies:
                tempMidDist = abs(i[1] - self.gameWidth / 2)
                if tempMidDist < middleDist:
                    closest = i
                    middleDist = tempMidDist

            guardSpot = closest

        if self.isRed and enemyPos[0] < self.middle:
            xDiff = enemyPos[0] - selfPos[0]
            yDiff = enemyPos[1] - selfPos[1]
            if xDiff == 1 and yDiff == 0:
                return 'East'
            if xDiff == -1 and yDiff == 0:
                return 'West'
            if yDiff == 1 and xDiff == 0:
                return 'North'
            if yDiff == -1 and xDiff == 0:
                return 'South'
            ind = self.index
            return self.defensiveBreadthFirstSearch(gameState, ind, enemyPos, self.noHeuristic)[0]

        elif not self.isRed and enemyPos[0] >= self.middle:
            xDiff = enemyPos[0] - selfPos[0]
            yDiff = enemyPos[1] - selfPos[1]
            if xDiff == 1 and yDiff == 0:
                return 'East'
            if xDiff == -1 and yDiff == 0:
                return 'West'
            if yDiff == 1 and xDiff == 0:
                return 'North'
            if yDiff == -1 and xDiff == 0:
                return 'South'
            ind = self.index
            return self.defensiveBreadthFirstSearch(gameState, ind, enemyPos, self.noHeuristic)[0]

        if self.index > 1 and gameState.getScore() < 1 and ghostManhattans[self.enemyIndex] > 4:
            if self.isRed and selfPos[0] > self.middle / 2:
                h = self.noHeuristic
                return self.foodBreadthFirstSearch(gameState, self.index, bestFood, h)[0]
            elif not self.isRed and selfPos[0] < self.middle + (self.middle / 2):
                h = self.noHeuristic
                return self.foodBreadthFirstSearch(gameState, self.index, bestFood, h)[0]

        if self.isRed and selfPos[0] >= self.middle:
            h = self.noHeuristic
            return self.breadthFirstSearch(gameState, self.index, guardSpot, h)[0]
        elif not self.isRed and selfPos[0] <= self.middle:
            h = self.noHeuristic
            return self.breadthFirstSearch(gameState, self.index, guardSpot, h)[0]

        if ghostManhattans[self.enemyIndex] > 4:
            h = self.noHeuristic
            return self.defensiveBreadthFirstSearch(gameState, self.index, guardSpot, h)[0]
        else:
            h = self.noHeuristic
            return self.defensiveBreadthFirstSearch(gameState, self.index, guardSpot, h)[0]

    def breadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        while True:
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) == target:
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop", 0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)

            tempActions = currentState.getLegalActions(index)
            for action in tempActions:
                succ = currentState.generateSuccessor(index, action)
                val1 = succ in exploredPaths
                val2 = succ.getAgentPosition(index) in exploredNodes
                val3 = succ in frontier
                if val1 or val2 or val3:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                h = heuristic(succ, index, target)
                frontier = self.priorityPush(frontier, succ, currentCost + h)
            if not frontier:
                return ("Stop", 0)

    def defensiveBreadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        while True:
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) == target:
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop", 0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)
            for action in currentState.getLegalActions(index):
                succ = currentState.generateSuccessor(index, action)
                xVal = succ.getAgentPosition(index)[0]
                if xVal < self.middle and not self.isRed:
                    continue
                if xVal > self.middle - 1 and self.isRed:
                    continue
                succ = currentState.generateSuccessor(index, action)
                val1 = succ in exploredPaths
                val2 = succ.getAgentPosition(index) in exploredNodes
                val3 = succ in frontier
                if val1 or val2 or val3:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                h = heuristic(succ, index, target)
                frontier = self.priorityPush(frontier, succ, currentCost + h)
            if not frontier:
                return ("Stop", 0)

    def foodBreadthFirstSearch(self, gameState, index, target, heuristic):
        """
        Search the shallowest nodes in the search tree first. [p 81]
        """
        frontier = [(gameState, 0)]
        exploredPaths = {}
        exploredPaths[gameState] = ["Stop"]
        exploredNodes = [gameState.getAgentPosition(index)]
        while True:
            newFrontierPull = frontier.pop(0)
            currentState = newFrontierPull[0]
            currentCost = newFrontierPull[1]
            if currentState.getAgentPosition(index) in self.getFood(gameState).asList():
                if len(exploredPaths[currentState]) == 1:
                    return ("Stop", 0)
                return (exploredPaths[currentState][1], len(exploredPaths[currentState]) - 1)
            for action in currentState.getLegalActions(index):
                succ = currentState.generateSuccessor(index, action)
                val1 = succ in exploredPaths
                val2 = succ.getAgentPosition(index) in exploredNodes
                val3 = succ in frontier
                if val1 or val2 or val3:
                    continue
                exploredNodes.append(succ.getAgentPosition(index))
                exploredPaths[succ] = exploredPaths[currentState] + [action]
                h = heuristic(succ, index, target)
                frontier = self.priorityPush(frontier, succ, currentCost + h)
            if not frontier:
                return ("Stop", 0)

    def middleHeuristic(self, gameState, index, target = None):
        return abs(gameState.getAgentPosition(index)[0] - self.middle)

    def noHeuristic(self, gameState, index, target = None):
        return 1

    def enemyHeuristic(self, gameState, index, target = None):
        selfPos = gameState.getAgentPosition(index)
        enemyPos = gameState.getAgentPosition(self.enemyIndex)
        xDiff = abs(selfPos[0] - enemyPos[0])
        yDiff = abs(selfPos[1] - enemyPos[1])
        return (xDiff + yDiff)

    def manhattanHeuristic(self, gameState, index, target):
        selfPos = gameState.getAgentPosition(index)
        return abs(selfPos[0] - target[0]) + abs(selfPos[1] - target[1])

    def euclidianHeuristic(self, gameState, index, target):
        selfPos = gameState.getAgentPosition(index)
        return pow(pow(selfPos[0] - target[0], 2) + pow(selfPos[1] - target[1], 2), 0.5)

    def inGhostMode(self, gameState, agentIndex):
        agentPos = gameState.getAgentPosition(agentIndex)
        gameWidth = gameState.getInitialLayout().width
        if agentIndex % 2 == 0 and agentPos[0] < gameWidth / 2:
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
