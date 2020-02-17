'''
Title:           Torus 8-Puzzle A* Search
Files:           torus_puzzle.py
Course:          CS540, Spring 2020

Author:          Yeochan Youn
Email:           yyoun5@wisc.edu
'''

'''
prints successor states of current state
input: 
    - state: current state
'''
def print_succ(state):
    ls = generate_succ(state)
    for i in range(4):
        print('{} h={}'.format(ls[i], heuristic(ls[i]))) # print all the successors

'''
generating successor of current state
input: 
    - state: current state
return: list of successors
'''
def generate_succ(state):
    pos0 = state.index(0)
    ls = []
    ls.append(move_up(state, pos0))
    ls.append(move_down(state, pos0))
    ls.append(move_left(state, pos0))
    ls.append(move_right(state, pos0))
    ls = sorted(ls) # sort the succ list
    return ls

'''
calculate heuristic of current state
input:
    - state: current state
return: heuristic of the state
'''
def heuristic(state):
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    h = 0
    for i in range(len(goal)):
        if state[i] != goal[i] and state[i] != 0:
            h += 1  # if position of element does not match with goal position, increase h by 1
    return h

'''
move up the 0 tile
input:
    - state: current state
    - pos0: current position of 0
return: state after 0 move up
'''
def move_up(state, pos0):
    ls = state.copy()
    new = -1
    if pos0 in [0, 1, 2]:
        new = pos0 + 6
    else:
        new = pos0 - 3
    ls[pos0], ls[new] = ls[new], ls[pos0]
    return ls

'''
move down the 0 tile
input:
    - state: current state
    - pos0: current position of 0
return: state after 0 move down
'''
def move_down(state, pos0):
    ls = state.copy()
    if pos0 in [6, 7, 8]:
        new = pos0 - 6
    else:
        new = pos0 + 3
    ls[pos0], ls[new] = ls[new], ls[pos0]
    return ls

'''
move left the 0 tile
input:
    - state: current state
    - pos0: current position of 0
return: state after 0 move left
'''
def move_left(state, pos0):
    ls = state.copy()
    if pos0 in [0, 3, 6]:
        new = pos0 + 2
    else:
        new = pos0 - 1
    ls[pos0], ls[new] = ls[new], ls[pos0]
    return ls

'''
move right the 0 tile
input:
    - state: current state
    - pos0: current position of 0
return: state after 0 move right
'''
def move_right(state, pos0):
    ls = state.copy()
    if pos0 in [2, 5, 8]:
        new = pos0 - 2
    else:
        new = pos0 + 1
    ls[pos0], ls[new] = ls[new], ls[pos0]
    return ls

'''
generate dictionary form of the state
input:
    - state: current state
    - move: count of move to get this 
    - parent: parent state of current state
return: dictionary form of the state
'''
def dic_gen(state, move, parent):
    return {'state': state, 'h': heuristic(state), 'g': move, 'parent': parent, 'f': heuristic(state) + move}

'''
solve the puzzle
input:
    - state: start state
'''
def solve(state):
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # goal state
    complete = False
    self = PriorityQueue()
    move = 0
    parent = None
    closed = []

    start = dic_gen(state, move, parent)  # create dictionary form from start state
    self.enqueue(start)

    while not complete:  # run until complete
        if self.is_empty():  # if queue is empty before complete, fail
            print('fail')
            break
        n = self.pop()
        closed.append(n)

        if n['state'] == goal:  # if goal is found, break the loop
            complete = True
            break
        else:  # else keep run the loop with successor states
            succ = generate_succ(n['state'])
            for i in succ:
                ex = False
                for j in closed:  # check succ states are existing on closed list
                    if i == j['state']:
                        ex = True
                        if n['g'] + 1 < j['g']:
                            j['g'] = n['g'] + 1
                            j['parent'] = n['state']
                            self.requeue(j)
                if not ex:  # if not existing, enqueue the succ
                    self.enqueue(dic_gen(i, n['g'] + 1, n['state']))

    pls = []  # list to print the goal path
    while True:
        pls.append(n)

        if n['state'] == start['state']:
            break
        for i in closed:
            if i['state'] == n['parent']:
                n = i
    pls.reverse()  # reverse the list to print from the start state
    for n in pls:
        print('{} h={} moves: {}'.format(n['state'], heuristic(n['state']), n['g']))
    print('Max queue length: {}'.format(self.max_len))


''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        in_open = False
        # TODO: set in_open to True if the state is in the queue already
        # TODO: handle that case correctly
        for i in self.queue:
            if state_dict['state'] == i['state']:
                in_open = True
                new = state_dict['g']
                orig = i['g']

                if new < orig:
                    i['g'] = state_dict['g']
                    i['f'] = state_dict['f']
                    i['parent'] = state_dict['parent']

        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state
