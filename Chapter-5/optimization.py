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


domin = [(0, 8)]*(len(people)*2)
print domin
s = hillclimb(domin, schedulecost)
print schedulecost(s)
printschedule(s)