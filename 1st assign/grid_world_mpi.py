import numpy as np
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def gridWorld():
    shape = [4, 4]
    # define the boundary
    MAX_X = shape[0]
    MAX_Y = shape[1]

    # define the grid
    nActions = 4
    nStates = np.prod(shape)

    grid = np.arange(nStates).reshape([nActions, nActions])
    P = {}

    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.nditer.html
    it = np.nditer(grid, flags=['multi_index'])

    while not it.finished:
        s = it.iterindex
        y, x = it.multi_index  # y -> number of row, x -> number of column

        # initialize prob distribution
        P[s] = {a: [] for a in range(nActions)}

        # check if arrive at terminal states (position 0 and 15)
        check_terminal = lambda s: s == 0 or s == (nStates - 1)
        reward = 0.0 if check_terminal(s) else -1.0

        if check_terminal(s):
            # got terminal, next state should be itself
            P[s][UP] = [(1.0, s, reward)]
            P[s][DOWN] = [(1.0, s, reward)]
            P[s][LEFT] = [(1.0, s, reward)]
            P[s][RIGHT] = [(1.0, s, reward)]

        else:

            ns_up = s if y == 0 else s - MAX_X
            ns_right = s if x == (MAX_X - 1) else s + 1
            ns_down = s if y == (MAX_Y - 1) else s + MAX_X
            ns_left = s if x == 0 else s - 1

            P[s][UP] = [(1.0, ns_up, reward)]
            P[s][RIGHT] = [(1.0, ns_right, reward)]
            P[s][DOWN] = [(1.0, ns_down, reward)]
            P[s][LEFT] = [(1.0, ns_left, reward)]

        it.iternext()

    # Initial state distribution is uniform
    # isd = np.ones(nStates) / nStates

    return nStates, nActions, P


# def policy_improvement(P, modified_evaluation, discount_factor = 0.95):
#     # U = dict([(s, 0) for s in grid])
#     # V = np.zeros(nStates)
#     # pi = dict([(s, random.choice(nActions)) for s in range(nStates)])
#     policy = np.zeros([nStates, nActions]) / nActions
#     counter = 0
#     while True:
#         counter += 1
#         V = modified_evaluation(policy, P)
#         policy_stable = True
#         for s in range(nStates):
#             old_a = np.argmax(policy[s])
#
#             action_array = np.zeros(nActions)
#             for a in range(nActions):
#
#                 for prob, next_s, reward in P[s][a]:
#                     action_array[a] += prob * (reward + discount_factor * V[next_s])
#
#             new_a = np.argmax(action_array)
#
#             if new_a != old_a:
#                 policy_stable = False
#             policy[s] = np.eye(nActions)[new_a]
#
#         if policy_stable:
#             return policy


def modified_evaluation(policy, P, k=20, discount_factor = 0.95):
    V = np.zeros(nStates)

    for i in range(k):

        for s in range(nStates):
            v = 0

            for a, a_prob in enumerate(policy[s]):

                for prob, next_s, reward in P[s][a]:

                    v += a_prob * prob * (reward + discount_factor * V[next_s])

            V[s] = v

    return np.array(V)

# def modified_evaluation(policy, P, discount_factor=0.95):
#     V = np.zeros(nStates)
#
#     for i in range(20):
#
#         for s in range(nStates):
#             v = 0
#
#             for a, a_prob in enumerate(policy[s]):
#
#                 for prob, next_s, reward in P[s][a]:
#                     v += a_prob * prob * (reward + discount_factor * V[next_s])
#
#             V[s] = v
#
#
#     return np.array(V)


def policy_improvement(P, policy_eval_fn=modified_evaluation, discount_factor=0.95):
    policy = np.ones([nStates, nActions]) / nActions

    while True:

        V = policy_eval_fn(policy, P)

        policy_stable = True

        for s in range(nStates):

            old_a = np.argmax(policy[s])

            action_array = np.zeros(nActions)

            for a in range(nActions):
                for prob, next_s, reward in P[s][a]:
                    action_array[a] += prob * (reward + discount_factor * V[next_s])

            new_a = np.argmax(action_array)

            if old_a != new_a:
                policy_stable = False
            policy[s] = np.eye(nActions)[new_a]

        if policy_stable:
            return policy, V




if __name__ == '__main__':
    discount_factor = 0.95
    nStates, nActions, P = gridWorld()

    policy = policy_improvement(P)

    print("policy")
    print(policy)
    print("")

    # print("value")
    # print(V)
    # print("")

    # print(V.reshape([4, 4]))
