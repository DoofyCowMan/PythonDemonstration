import random

def main():
    difficulty = input("Select a Difficulty\neasy, medium, or hard: ").lower()
    while difficulty not in ["easy", "medium", "hard"]:
        print("Invalid Input")
        difficulty = input("Select a Difficulty\neasy, medium, or hard: ").lower()

    state = [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"]
    ]

    PrintBoard(state)
    gameOver = 2

    while gameOver == 2:
        inputs = GetInputs(state)
        state[inputs[0] - 1][inputs[1] - 1] = "X"
        PrintBoard(state)

        gameOver = CheckForGameOver(state)
        if gameOver != 2:
            break

        opponentInput = []

        if difficulty == "easy":
            opponentInput = GetRandomMove(state)
        elif difficulty == "medium":
            opponentInput = GetMediumMove(state)
        else:
            opponentInput = GetBestMove(state)

        state[opponentInput[0]][opponentInput[1]] = "O"
        PrintBoard(state)

        gameOver = CheckForGameOver(state)

    PrintBoard(state)

    if gameOver == -1:
        print("You Lose")
    elif gameOver == 1:
        print("You Win")
    else:
        print("It's a draw")

def GetInputs(state):
    valid = False
    while not valid:
        try:
            rowPosition = int(input("Enter the row number for where you would like to put an X: "))
            columnPosition = int(input("Enter the column number for where you would like to put an X: "))
            if state[rowPosition - 1][columnPosition - 1] == "-":
                valid = True
            else:
                print("Invalid Input")
        except (ValueError, IndexError):
            print("Invalid Input")
    return rowPosition, columnPosition

def GetRandomMove(state):
    valid = False
    while not valid:
        rowPosition = random.randint(0, 2)
        columnPosition = random.randint(0, 2)
        if state[rowPosition][columnPosition] == "-":
            valid = True
    return rowPosition, columnPosition

#Probably a better way to do this
def GetMediumMove(state):
    moves = evaluateState(state, 0)
    values = moves[0]
    move = moves[1]

    print(moves)

    bestMove = GetBestMove(state)

    weights=[]
    for i in range(len(values)):
        if values[i] != -1:
            weights.append(1/((values[i]+1)/10))
        else:
            weights.append(1/((values[i]+1.001)/10))
        if move[i] == bestMove:
            weights[i] *= len(values)/2.5


    chosenMove = random.choices(move, weights=weights)
    return chosenMove[0]



def GetBestMove(state):
    moves = evaluateState(state, 0)
    values = moves[0]
    move = moves[1]

    lowest = float('inf')
    lowestIndex = -1
    for s in range(len(values)):
        if values[s] < lowest:
            lowest = values[s]
            lowestIndex = s

    return move[lowestIndex]

#MinMax algorithm
def evaluateState(state, turn):
    values = []
    associatedMove = []
    for i in range(len(state)):
        for k in range(len(state[i])):
            if state[i][k] == "-":
                newState = [row[:] for row in state]
                if turn == 0:
                    newState[i][k] = "O"
                else:
                    newState[i][k] = "X"

                gameOver = CheckForGameOver(newState)

                if gameOver != 2:
                    values.append(float(gameOver))
                    associatedMove.append((i, k))
                else:
                    nestedValues, _ = evaluateState(newState, 1 - turn)
                    avg = sum(nestedValues) / len(nestedValues)
                    values.append(avg)
                    associatedMove.append((i, k))

    return values, associatedMove

def CheckForGameOver(state):
    for i in range(len(state)):
        if state[i][0] != "-" and state[i][0] == state[i][1] == state[i][2]:
            return 1 if state[i][0] == "X" else -1

        if state[0][i] != "-" and state[0][i] == state[1][i] == state[2][i]:
            return 1 if state[0][i] == "X" else -1

    if state[0][0] != "-" and state[0][0] == state[1][1] == state[2][2]:
        return 1 if state[0][0] == "X" else -1

    if state[2][0] != "-" and state[2][0] == state[1][1] == state[0][2]:
        return 1 if state[2][0] == "X" else -1

    for r in state:
        if "-" in r:
            return 2


    return 0

def PrintBoard(state):
    print("\t1\t2\t3")
    for i in range(len(state)):
        print(f"{i + 1}\t{state[i][0]}\t{state[i][1]}\t{state[i][2]}")
    print("")
    print("")


main()
