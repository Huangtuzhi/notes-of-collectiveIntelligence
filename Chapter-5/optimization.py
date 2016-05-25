import time
import random
import math

people = [('Seymour', 'BOS'),
('Franny', 'DAL'),
('Zooey', 'CAK'),
('Walt', 'MIA'),
('Buddy', 'ORD'),
('Les', 'OMA')]

destination = 'LGA'

flights = {}
for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    flights[(origin, dest)].append((depart, arrive, int(price)))


def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def printschedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[d]]
        ret = flights[(destination, origin)][r[d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, 
            out[0], out[1], out[2],
            ret[0], ret[1], ret[2])


def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d+1])]

        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the lastest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])

    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d+1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    if latestarrival > earliestdep: totalprice += 50
    return totalprice + totalwait


def randomoptimize(domin, costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        r = [random.randint(domin[i][0], domin[i][1]) for i in range(len(domin))]
        # Get the cost
        cost = costf(r)

        if cost < best:
            best = cost
            bestr = r
    return r


def hillclimb(domin, costf):
    sol = [random.randint(domin[i][0], domin[i][1]) 
          for i in range(len(domin))]

    while 1:
        neighbors = []
        for j in range(len(domin)):
            if sol[j] > domin[j][0]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
            if sol[j] < domin[j][1]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])

        # See what the best solution amonst the neighbors is
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]

        if best == current:
            break
    return sol


def annealingoptimize(domin, costf, T=10000.0, cool=0.95, step=1):
    vec = [random.randint(domin[i][0], domin[i][1]) 
          for i in range(len(domin))]

    while T > 0.1:
        i = random.randint(0, len(domin) - 1)
        dir = random.randint(-step, step)

        # Create a new list with one of the values changed
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domin[i][0]:
            vecb[i] = domin[i][0]
        elif vecb[i] > domin[i][1]:
            vecb[i] = domin[i][1]

        # Calculate the current cost and the new cost
        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e, (-eb-ea)/T)

        if (eb < ea or random.random() < p):
            vec = vecb

        T = T*cool
    return vec


def geneticoptimize(domain, costf, popsize=50, step=1, mutprod=0.2, elite=0.2, maxiter=100):
    # Mutation operation
    def mutate(vec):
        i = random.randint(0, len(domin) - 1)
        if random.random() < 0.5 and vec[i] > domin[i][0]:
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
        elif vec[i] < domin[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]

    # Crossover operation
    def crossover(r1, r2):
        i = random.randint(1, len(domin) - 2)
        return r1[0:i] + r2[i:]

    # Build the initial population
    pop = []
    for i in range(popsize):
        vec = [random.randint(domin[i][0], domin[i][1]) 
            for i in range(len(domin))]
        pop.append(vec)

    toplite = int(elite * popsize)

    # Main loop
    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]

        # Start with the pure winners
        pop = ranked[0: toplite]

        # Add mutated and bred forms of the winners
        while len(pop) < popsize:
            if random.random() < mutprod:
                # Mutation
                c = random.randint(0, toplite)
                pop.append(mutate(ranked[c]))
            else:
                # Crossover
                c1 = random.randint(0, toplite)
                c2 = random.randint(0, toplite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        # Print current best score
        print scores[0][0]
    return scores[0][1]



# domin = [(0, 8)]*(len(people)*2)
# s = geneticoptimize(domin, schedulecost)
# print s
# printschedule(s)