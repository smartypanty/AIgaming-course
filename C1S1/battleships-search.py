#   ____        _   _   _           _     _
#  | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  ___
#  |  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \/ __|
#  | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) \__ \
#  |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/|___/
#                                          |_|
botName='smarty-battleship'

import random
import json
from random import randint, choice


# These are the only additional libraries available to you. Uncomment them
# to use them in your solution.
#
#import numpy    # Base N-dimensional array package
#import pandas   # Data structures & analysis


# =============================================================================
# This calculateMove() function is where you need to write your code. When it
# is first loaded, it will play a complete game for you using the Helper
# functions that are defined below. The Helper functions give great example
# code that shows you how to manipulate the data you receive and the move
# that you have to return.
#

def calculateMove(gameState):
    if "previousMove" not in persistentData:
        persistentData["previousMove"] = {}
    if "targetMode" not in persistentData:
        persistentData["targetMode"] = False
        
    if gameState["Round"] == 0:
        #move = exampleShipPlacement()  # Does not take land into account
        move = deployRandomly(gameState)
    else:
        previousMove = persistentData["previousMove"]
        if len(previousMove) > 0:
            isHit = checkHitOrMiss(previousMove, gameState)
            if (isHit and not persistentData["targetMode"]):
                persistentData["targetMode"] = True
            if persistentData["targetMode"]:
                # perform search
                move = searchNeighbours(previousMove, isHit, persistentData, gameState)
            else:
                move = chooseRandomValidTarget(gameState)
        else:
            move = chooseRandomValidTarget(gameState)
        persistentData["previousMove"] = move
    print('MOVE: ' + str(move))
    return move



def searchNeighbours(previousMove, isHit, persistentData, gameState):
    if "visited" not in persistentData:
        persistentData["visited"] = set()
    visited = persistentData["visited"]
    
    if "stack" not in persistentData:
        persistentData["stack"] = [str(previousMove)]
    stack = persistentData["stack"] 

    visited.add(str(previousMove))
    
    if isHit:
        row = ord(previousMove['Row']) - 65
        column = previousMove['Column'] - 1
        neighbours = selectUntargetedAdjacentCell(row, column, gameState["OppBoard"])
        neighbour_moves = set()
        for n in neighbours:
            m = translateMove(n[0], n[1])
            neighbour_moves.add(str(m))
        stack.extend(neighbour_moves - visited)
    
    if stack:
        move = eval(stack.pop())
        return move
    else: # the stack is empty; reboot stack and visited for the future searches; move randomly
        persistentData["visited"] = set()
        persistentData["stack"] = []
        persistentData["targetMode"] = False
        move = chooseRandomValidTarget(gameState)
        return move


def checkHitOrMiss(move, gameState):
    board = gameState['OppBoard']
    row = ord(move['Row']) - 65
    column = move['Column'] - 1
    
    moveValue = board[row][column]
    if moveValue == 'H':
        return True
    else: # moveValue == 'M'
        return False

# =============================================================================
# The code below shows a selection of helper functions designed to make the
# time to understand the environment and to get a game running as short as
# possible. The code also serves as an example of how to manipulate the myBoard
# and oppBoard dictionaries that are in gameState.


def exampleShipPlacement():
    # The Placement list adds ships in the order that the ships are
    # listed in the game style e.g. 5,4,3,3,2 places the ship of length
    # 5 first, the ship of length 4 second, the ship of length 3 third.
    #
    # This function does not check for any land and, so, should be used
    # with a gamestyle that does not include land.
    move = {"Placement": [
                  {
                    "Row": "A",
                    "Column": 1,
                    "Orientation": "H"
                  },
                  {
                    "Row": "B",
                    "Column": 6,
                    "Orientation": "V"
                  },
                  {
                    "Row": "C",
                    "Column": 1,
                    "Orientation": "H"
                  },
                  {
                    "Row": "D",
                    "Column": 1,
                    "Orientation": "H"
                  },
                  {
                    "Row": "E",
                    "Column": 1,
                    "Orientation": "V"
                  }
               ]
            }
    return move


# Deploys all the ships randomly on a blank board
def deployRandomly(gamestate):
    move = []  # Initialise move as an emtpy list
    orientation = None
    row = None
    column = None
    for i in range(len(gamestate["Ships"])):  # For every ship that needs to be deployed
        deployed = False
        while not deployed:  # Keep randomly choosing locations until a valid one is chosen
            row = randint(0, len(gamestate["MyBoard"]) - 1)  # Randomly pick a row
            column = randint(0, len(gamestate["MyBoard"][0]) - 1)  # Randomly pick a column
            orientation = choice(["H", "V"])  # Randomly pick an orientation
            if deployShip(row, column, gamestate["MyBoard"], gamestate["Ships"][i], orientation, i):  # If ship can be successfully deployed to that location...
                deployed = True  # ...then the ship has been deployed
        move.append({"Row": chr(row + 65), "Column": (column + 1),
                     "Orientation": orientation})  # Add the valid deployment location to the list of deployment locations in move
    return {"Placement": move}  # Return the move


# Returns whether given location can fit given ship onto given board and, if it can, updates the given board with that ships position
def deployShip(i, j, board, length, orientation, ship_num):
    if orientation == "V":  # If we are trying to place ship vertically
        if i + length - 1 >= len(board):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i + l][j] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            board[i + l][j] = str(ship_num)  # Place the ship on the board
    else:  # If we are trying to place ship horizontally
        if j + length - 1 >= len(board[0]):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i][j + l] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            board[i][j + l] = str(ship_num)  # Place the ship on the board
    return True  # Ship deployed


# Randomly guesses a location on the board that hasn't already been hit
def chooseRandomValidTarget(gamestate):
    valid = False
    row = None
    column = None
    while not valid:  # Keep randomly choosing targets until a valid one is chosen
        row = randint(0, len(gamestate["MyBoard"]) - 1)  # Randomly pick a row
        column = randint(0, len(gamestate["MyBoard"][0]) - 1)  # Randomly pick a column
        if gamestate["OppBoard"][row][column] == "":  # If the target is sea that hasn't already been guessed...
            valid = True  # ...then the target is valid
    move = {"Row": chr(row + 65),
            "Column": (column + 1)}  # Set move equal to the valid target (convert the row to a letter 0->A, 1->B etc.)
    return move  # Return the move


# Returns a list of the lengths of your opponent's ships that haven't been sunk
def shipsStillAfloat(gamestate):
    afloat = []
    ships_removed = []
    for k in range(len(gamestate["Ships"])):  # For every ship
        afloat.append(gamestate["Ships"][k])  # Add it to the list of afloat ships
        ships_removed.append(False)  # Set its removed from afloat list to false
    for i in range(len(gamestate["OppBoard"])):
        for j in range(len(gamestate["OppBoard"][0])):  # For every grid on the board
            for k in range(len(gamestate["Ships"])):  # For every ship
                if str(k) in gamestate["OppBoard"][i][j] and not ships_removed[k]:  # If we can see the ship number on our opponent's board and we haven't already removed it from the afloat list
                    afloat.remove(gamestate["Ships"][k])  # Remove that ship from the afloat list (we can only see an opponent's ship number when the ship has been sunk)
                    ships_removed[k] = True  # Record that we have now removed this ship so we know not to try and remove it again
    return afloat  # Return the list of ships still afloat


# Returns a list of cells adjacent to the input cell that are free to be targeted (not including land)
def selectUntargetedAdjacentCell(row, column, oppBoard):
    adjacent = []  # List of adjacent cells
    if row > 0 and oppBoard[row - 1][column] == "":  # If there is a cell above
        adjacent.append((row - 1, column))  # Add to list of adjacent cells
    if row < len(oppBoard) - 1 and oppBoard[row + 1][column] == "":  # If there is a cell below
        adjacent.append((row + 1, column))  # Add to list of adjacent cells
    if column > 0 and oppBoard[row][column - 1] == "":  # If there is a cell left
        adjacent.append((row, column - 1))  # Add to list of adjacent cells
    if column < len(oppBoard[0]) - 1 and oppBoard[row][column + 1] == "":  # If there is a cell right
        adjacent.append((row, column + 1))  # Add to list of adjacent cells
    return adjacent


# Given a valid coordinate on the board returns it as a correctly formatted move
def translateMove(row, column):
    return {"Row": chr(row + 65), "Column": (column + 1)}
