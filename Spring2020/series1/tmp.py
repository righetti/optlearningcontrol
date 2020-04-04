

Python 3

    File
    Edit
    View
    Insert
    Cell
    Kernel
    Help

1

%matplotlib notebook

2

​

3

import numpy as np

4

import matplotlib.pyplot as plt

5

import matplotlib as mp

6

import heapq as hq

7

​

8

np.set_printoptions(precision=5,linewidth=120,suppress=True)

9

​

10

# the bisect module enables to easily keep an ordered list

11

# cf. https://docs.python.org/3.7/library/bisect.html

12

# useful for maintaining the OPEN list

13

import bisect

1

​

1

def breadthFirstSearch(graph, start_node, end_node, cost):

2

    """

3

    TO BE COMPLETED

4

    this function gets a graph, a start_node, end_node and cost list as entry

5

    and returns a path (list of nodes) as output

6

    it return an empty list in case of failure

7

    """

8

    # ref = 

9

    # https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/

10

    # graph is a adjacency list

11

    

12

    def minDistance(dist,queue): 

13

        # Initialize min value and min_index as -1 

14

        minimum = float("Inf") 

15

        min_index = -1

16

          

17

        # from the dist array,pick one which 

18

        # has min value and is till in queue 

19

        for i in range(len(dist)): 

20

            if (dist[i] < minimum or dist[i] == float('inf')) and i in queue: 

21

                minimum = dist[i] 

22

                min_index = i 

23

        return min_index 

24

    

25

    row = len(cost) 

26

    col = len(cost[0]) 

27

​

28

    # The output array. dist[i] will hold 

29

    # the shortest distance from src to i 

30

    # Initialize all distances as INFINITE  

31

    dist = [float("Inf")] * row 

32

​

33

    #Parent array to store  

34

    # shortest path tree 

35

    parent = [-1] * row 

36

​

37

    # Distance of source vertex  

38

    # from itself is always 0 

39

    dist[start_node] = 0

40

​

41

    # Add all vertices in queue 

42

    queue = [] 

43

    for i in range(row): 

44

        queue.append(i) 

45

​

46

    #Find shortest path for all vertices 

47

    while queue: 

48

​

49

        # Pick the minimum dist vertex  

50

        # from the set of vertices 

51

        # still in queue 

52

        u = minDistance(dist,queue)  

53

                

54

        # remove min element      

55

        queue.remove(u) 

56

​

57

        # Update dist value and parent  

58

        # index of the adjacent vertices of 

59

        # the picked vertex. Consider only  

60

        # those vertices which are still in 

61

        # queue 

62

        for i in range(col): 

63

            '''Update dist[i] only if it is in queue, there is 

64

            an edge from u to i, and total weight of path from 

65

            src to i through u is smaller than current value of 

66

            dist[i]'''

67

            if cost[u][i] and i in queue: 

68

                if dist[u] + cost[u][i] < dist[i]: 

69

                    dist[i] = dist[u] + cost[u][i] 

70

                    parent[i] = u 

71

                    

72

    def printPath(parent, j): 

73

        #Base Case : If j is source 

74

        if parent[j] == -1 :  

75

            print(j) 

76

            return

77

        printPath(parent , parent[j]) 

78

        print(j) 

79

        

80

    print("shortset dist is:", dist[end_node])

81

    print("the path is:")

82

    printPath(parent, end_node)

83

        

84

​

85

def depthFirstSearch(graph, start_node, end_node, cost):

86

    """

87

    TO BE COMPLETED

88

    this function gets a graph, a start_node, end_node and cost list as entry

89

    and returns a path (list of nodes) as output

90

    it return an empty list in case of failure

91

    """

92

    

93

​

94

​

95

    

96

​

97

def AStar(graph, start_node, end_node, cost, heuristic):

98

    """

99

    TO BE COMPLETED

100

    this function gets a graph, a start_node, end_node and cost list as entry

101

    and returns a path (list of nodes) as output

102

    it return an empty list in case of failure

103

    """

1

def display_result(world_mat, path):

2

    """

3

    This function displays a maze described in world_mat and a path inside the maze

4

    world_mat: a NxN matrix that contains the maze (0 for free path, -10 for obstacle)

5

    path: a list of elements numbered as the graph (i.e. from 0 to N**2-1)

6

    """

7

    N = world_mat.shape[0]

8

    display_mat = world_mat.copy()

9

    for el in path:

10

        display_mat[convert_to_matrixindex(el,N)] = 5

11

    plt.matshow(display_mat, cmap='Greys')

12

    

13

def convert_to_listindex(i,j,N):

14

    """

15

    This function converts a (i,j) matrix entry index to a list index for matrix of size N

16

    """

17

    return N*i+j

18

​

19

def convert_to_matrixindex(a,N):

20

    """

21

    This function converts a list entry a into a (i,j) matrix entry for matrix of size N

22

    """

23

    i = int(a/N) # the result of integer division

24

    j = int(a%N) # the  remainder of the division

25

    return i,j

26

​

27

def create_graph(world_mat):

28

    """

29

    This functions takes a NxN matrix in entry and creates a graph and a map of costs

30

    Since we use lists, for a world_mat of size NxN, we associate to the entry [i,j] of world_map

31

    the index a=N*i + j of the list

32

    output:

33

        graph: a list of neighbors  (indexed as explained above)

34

        cost: a N**2 x  N**2 array. Each entry cost[i,j] contains the cost of transitioning from node i to node j

35

            it is infinite if there is no edge from i to j

36

    """

37

    N = world_mat.shape[0]

38

    graph = []

39

    for i in range(N):

40

        for j in range(N):

41

            neigh = []

42

            if(i!=N-1):

43

                if(world_mat[i+1,j]==0):

44

                    neigh.append(N*(i+1)+j)

45

            if(i!=0):

46

                if(world_mat[i-1,j]==0):

47

                    neigh.append(N*(i-1)+j)

48

            if(j!=N-1):

49

                if(world_mat[i,j+1]==0):

50

                    neigh.append(N*i+j+1)

51

            if(j!=0):

52

                if(world_mat[i,j-1]==0):

53

                    neigh.append(N*i+j-1)

54

            graph.append(neigh)

55

    

56

    cost = np.ones([N*N,N*N]) * np.inf

57

    

58

    for i in range(N*N):

59

        for j in graph[i]:

60

            cost[i,j] = 1

61

    

62

    return graph, cost

1

# let's create a map corresponding to the robot path planning example of lecture 3

2

# it is a 5x5 grid

3

world_map = np.zeros([5,5])

4

# and it contains obstacles which we mark as non 0

5

world_map[0,4] = 10

6

world_map[1,1:3] = 10

7

world_map[2,1] = 10

8

world_map[3,3] = 10

9

world_map[4,1:3] = 10

10

​

11

# we can print the matrix

12

print(world_map)

13

​

14

# we can now display the result

15

display_result(world_map, [])

[[ 0.  0.  0.  0. 10.]
 [ 0. 10. 10.  0.  0.]
 [ 0. 10.  0.  0.  0.]
 [ 0.  0.  0. 10.  0.]
 [ 0. 10. 10.  0.  0.]]

Figure 1
1

# let's assume we have a path from (0,0) to (4,4) that does (in linear index)

2

path = [0,1,2,3,8,9,14,19,24]

3

​

4

# we print the equivalent in matrix entries

5

for a in path:

6

    print(convert_to_matrixindex(a, 5))

7

​

8

# and we display it on the world grid (shown in grey)

9

display_result(world_map, path)

10

​

11

​

12

adj_list, cost_mat =  create_graph(world_map)

13

breadthFirstSearch(adj_list, 0, 24, cost_mat)

(0, 0)
(0, 1)
(0, 2)
(0, 3)
(1, 3)
(1, 4)
(2, 4)
(3, 4)
(4, 4)

Figure 2

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
24 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
23 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
22 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
21 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
20 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
19 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
18 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
17 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
16 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
15 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
14 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
13 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
12 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
11 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
10 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
9 *******************
[0, 1, 2, 3, 4, 5, 6, 7, 8]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
8 *******************
[0, 1, 2, 3, 4, 5, 6, 7]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
7 *******************
[0, 1, 2, 3, 4, 5, 6]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
6 *******************
[0, 1, 2, 3, 4, 5]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
5 *******************
[0, 1, 2, 3, 4]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
4 *******************
[0, 1, 2, 3]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
3 *******************
[0, 1, 2]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
2 *******************
[0, 1]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
1 *******************
[0]
[0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
0 *******************
shortset dist is: inf
the path is:
24

1

# we can also create the associated graph and costs

2

graph, cost = create_graph(world_map)

3

​

4

# the neighbors of entry the cell [0,0] are

5

print('Neighbors of entry [0,0]')

6

a = convert_to_listindex(0,0,5)

7

neighborhs = graph[a]

8

for n in neighborhs:

9

    print('in linear indexes: ' + str(n) + ' which corresponds to the matrix entry: ' + str(convert_to_matrixindex(n,5)))

10

    

11

print('\n\nNeighbors of entry [2,3]')

12

a = convert_to_listindex(2,3,5)

13

neighborhs = graph[a]

14

for n in neighborhs:

15

    print('in linear indexes: ' + str(n) + ' which corresponds to the matrix entry: ' + str(convert_to_matrixindex(n,5)))

Neighbors of entry [0,0]
in linear indexes: 5 which corresponds to the matrix entry: (1, 0)
in linear indexes: 1 which corresponds to the matrix entry: (0, 1)


Neighbors of entry [2,3]
in linear indexes: 8 which corresponds to the matrix entry: (1, 3)
in linear indexes: 14 which corresponds to the matrix entry: (2, 4)
in linear indexes: 12 which corresponds to the matrix entry: (2, 2)

1

# here we load the 3 mazes and display them

2

maze1 = np.load('maze1.npy')

3

display_result(maze1, [])

4

​

5

maze2 = np.load('maze2.npy')

6

display_result(maze2, [])

7

​

8

maze3 = np.load('maze3.npy')

9

display_result(maze3, [])

10

​

Figure 3
Figure 4
Figure 5
x=49.0094 y=7.70564 [0]
1

print(graph)

2

print(cost)

3

​

4

print(type(cost[0][0]))

[[5, 1], [2, 0], [3, 1], [8, 2], [9, 3], [10, 0], [1, 5], [12, 2, 8], [13, 3, 9], [14, 8], [15, 5], [16, 12, 10], [17, 13], [8, 14, 12], [19, 9, 13], [20, 10, 16], [17, 15], [12, 16], [23, 13, 19, 17], [24, 14], [15], [16, 20], [17, 23], [24], [19, 23]]
[[inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [ 1. inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf  1. inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf inf  1. inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf inf inf  1. inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [ 1. inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf inf  1. inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf inf]
 [inf inf inf  1. inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf  1. inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf  1. inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf  1. inf inf inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf inf  1. inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf  1. inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf  1. inf inf inf  1. inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf  1.]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf inf inf inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf inf inf  1. inf]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1.]
 [inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf inf  1. inf inf inf  1. inf]]
<class 'numpy.float64'>

