import datetime


# State or node
class State:
    # Heuristic function (Manhattan Distance)
    def h(self):
        total = 0
        for x in self.board:
            if x != 0:
                ydist = abs(GOAL_STATE.index(x) % 3 - self.board.index(x) % 3)
                xdist = abs(GOAL_STATE.index(x) // 3 - self.board.index(x) // 3)
                total += (xdist + ydist)
        return total

    # Constructor for the state, g holds the value of steps, and f is g + the heuristic
    def __init__(self, board, parent=None, transition=None):
        self.parent = parent
        self.transition = transition
        self.board = list(board)
        self.g = 0
        if self.parent is not None:
            self.g = self.parent.g + 1
        self.f = self.h() + self.g


# prints the path from the initial state to the given state using the parent field
def print_path(current_node):
    path = list()
    while current_node is not None:
        if current_node.transition is not None:
            path.append(current_node.transition)
        current_node = current_node.parent
    path = path[::-1]
    for x in path:
        print("Move blank", x, end=", ")
    print()


# prints out a 3x3 visual of a state
def print_state(s):
    count = 0
    for x in s.board:
        if x != 0:
            print("|", x, end="")
        else:
            print("| ", end=" ")
        count += 1
        if count % 3 == 0:
            print("|")
    print()


# Creates a new node with the blank space moved one
def move(s, step, amount):
    new_state = State(s.board, s, step)
    temp_index = new_state.board.index(0)
    temp = new_state.board[temp_index + amount]
    new_state.board[temp_index + amount] = 0
    new_state.board[temp_index] = temp
    return new_state


# main method for the A* search
def search(s):
    explored = list()
    frontier = list()
    expl_board = list()
    current = s
    explored.append(current)
    expl_board.append(current.board)

    while current.h() != 0:
        if current.board.index(0) > 2:
            new = move(current, "up", -3)
            if current.parent is None or current.parent.board != new.board and new.board not in expl_board:
                frontier.append(new)

        if current.board.index(0) < 6:
            new = move(current, "down", 3)
            if current.parent is None or current.parent.board != new.board and new.board not in expl_board:
                frontier.append(new)

        if current.board.index(0) not in (2, 5, 8):
            new = move(current, "right", 1)
            if current.parent is None or current.parent.board != new.board and new.board not in expl_board:
                frontier.append(new)

        if current.board.index(0) not in (0, 3, 6):
            new = move(current, "left", -1)
            if current.parent is None or current.parent.board != new.board and new.board not in expl_board:
                frontier.append(new)

        choice = min(x.f for x in frontier)
        for i in frontier:
            if i.f == choice:
                current = i
                explored.append(current)
                expl_board.append(current.board)
                frontier.remove(current)
                break

    print_path(explored[-1])


# the goal result of the slide puzzle
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
s1 = list(map(int, input("Enter an initial configuration for the slide puzzle (left to right top to bottom separated "
                         "by spaces) with a 0 for the blank square: ").split()))
start = datetime.datetime.now()
search(State(s1))
print("Time: ", datetime.datetime.now()-start)
