from domain import *
def epoca(noAnts, size, initial, energy, distances, trace, alpha, beta, q0, rho,max_cost):
    antSet = [ant(initial,energy,size) for i in range(noAnts)]
    for i in range(size):
        # numarul maxim de iteratii intr-o epoca este lungimea solutiei
        for x in antSet:
            x.addMove(q0, trace, alpha, beta, distances,max_cost)
    # actualizam trace-ul cu feromonii lasati de toate furnicile
    dTrace = [1.0 / antSet[i].fitness() for i in range(len(antSet))]
    for i in range(size):
        for j in range(size):
            trace[i][j] = (1 - rho) * trace[i][j]
    for i in range(len(antSet)):
        for j in range(len(antSet[i].path) - 1):
            x = antSet[i].path[j]
            y = antSet[i].path[j + 1]
            trace[x][y] = trace[x][y] + dTrace[i]
    # return best ant path
    f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
    f = max(f)
    return antSet[f[1]].path,antSet[f[1]].energy
