from PriorityQueue import PriorityQueue

def manhattanHeuristic(xi, yi, xf, yf):
    return abs(xi - xf) + abs(yi - yf)
def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY, h):

    visited = set()
    toVisit = PriorityQueue()
    toVisit.add((initialX, initialY), h(initialX, initialY, finalX, finalY)) # add the initial position to the priority queue
    droneD.roadGreedy[(initialX, initialY)] = None
    found = False

    while((not toVisit.isEmpty()) and (not found)):

        # no route had been found
        if toVisit.isEmpty():
            return False

        #add the next spot to the visited
        node = toVisit.pop()[0]
        visited.add(node)
        # node is equal to the destination
        if node == (finalX, finalY):
            found = True

        # add the neighbours with respective priorities
        neighbours = mapM.get_neighbours(node[0], node[1])


        for n in neighbours:
            if (not toVisit.contains(n)) and (n not in visited):
                toVisit.add(n, h(n[0], n[1], finalX, finalY))
                droneD.roadGreedy[(n[0], n[1])] = (node[0], node[1])

    # if a route was found, contruct it using the road from the drone
    if found == True:
        route = []
        route.append((finalX, finalY))
        while(droneD.roadGreedy[route[-1]] != None):
            route.append(droneD.roadGreedy[route[-1]])



        return len(route)-1

def searchGreedyP(mapM, droneD, initialX, initialY, finalX, finalY, h):

    visited = set()
    toVisit = PriorityQueue()
    toVisit.add((initialX, initialY), h(initialX, initialY, finalX, finalY)) # add the initial position to the priority queue
    droneD.roadGreedy[(initialX, initialY)] = None
    found = False

    while((not toVisit.isEmpty()) and (not found)):

        # no route had been found
        if toVisit.isEmpty():
            return False

        #add the next spot to the visited
        node = toVisit.pop()[0]
        visited.add(node)
        # node is equal to the destination
        if node == (finalX, finalY):
            found = True

        # add the neighbours with respective priorities
        neighbours = mapM.get_neighbours(node[0], node[1])


        for n in neighbours:
            if (not toVisit.contains(n)) and (n not in visited):
                toVisit.add(n, h(n[0], n[1], finalX, finalY))
                droneD.roadGreedy[(n[0], n[1])] = (node[0], node[1])

    # if a route was found, contruct it using the road from the drone
    if found == True:
        route = []
        route.append((finalX, finalY))
        while(droneD.roadGreedy[route[-1]] != None):
            route.append(droneD.roadGreedy[route[-1]])



        return reversed(route)