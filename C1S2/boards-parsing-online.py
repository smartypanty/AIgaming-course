import urllib.request
import operator

def translateMove(row, column):
    return {"Row": chr(row + 65), "Column": (column + 1)}


# step 1 - loading the data
url = urllib.request.urlopen("https://raw.githubusercontent.com/smartypanty/AIgaming-course/master/C1S2/boards.txt") # creates a url object
s = url.read().decode() # extracts a byte string with the url content, and converts it into a string

boardStrings = s.strip().splitlines() # creates a list of boards
boards = []
for b in boardStrings:
    board = eval(b)
    boards.append(board)

print(len(boards))



# step 2 - finding similar boards
oppBoard = [['', '', 'H', 'H', '', '', '', ''], ['', '', '', '', '', '', 'M', ''], ['M', '', 'M', '', 'M', '', '', ''], ['', '', '', '', 'M', '', '', ''], ['', '', '', '', 'M', 'M', '', ''], ['', 'M', '', '', '', 'M', '', 'M'], ['', '', '', '', 'M', '', 'H', ''], ['M', '', 'H', 'M', '', '', '', '']]
#oppBoard = gameState['OppBoard']

# get indices of all opponent cells that are open
openedCells = []
for i in range(8): # for every row
    for j in range(8): # for every column
        if oppBoard[i][j] != '':
            openedCells.append([i, j])


similarBoards = []
for board in boards:
    for cell in openedCells:
        row = cell[0]
        column = cell[1]
        if oppBoard[row][column] == 'M' and board[row][column] != '':
            break
        if oppBoard[row][column] == 'H' and board[row][column] == '':
            break
    else:
        similarBoards.append(board)

print(len(similarBoards))
#print(similarBoards)



# step 3 - finding most promising cells
targetCells = {}
for board in similarBoards:
    for i in range(8):  # for every row
        for j in range(8):  # for every column
            if [i,j] not in openedCells:
                if board[i][j] != '':
                    cell = str(translateMove(i,j))
                    targetCells[cell] = targetCells.get(cell, 0) + 1

print(str(targetCells))

sortedTargetCells = sorted(targetCells.items(), key=operator.itemgetter(1), reverse=True)
print(sortedTargetCells)

move = eval(sortedTargetCells[0][0])
print(move)