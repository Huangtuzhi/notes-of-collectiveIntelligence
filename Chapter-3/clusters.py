from math import sqrt

def readfile(filename):
    lines = [line for line in file(filename)]

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def person(p1, p2):
    sum1 = sum(p1)
    sum2 = sum(p1)

    sum1Sq = sum([pow(p, 2) for p in p1])
    sum2Sq = sum([pow(p, 2) for p in p2])

    pSum = sum([p1[i] * p2[i] for i in range(len(p1))])

    num = pSum - (sum1 * sum2 / len(p1))
    den = sqrt(abs((sum1Sq - pow(sum1, 2)/len(p1)) * (sum2Sq - pow(sum2, 2)/len(p1))))
    if den == 0:
        return 0
    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=person):
    distances = {}
    currentclustid = -1

    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate the average of the two clusters
        mergevec = [
        (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
        for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
            right=clust[lowestpair[1]],
            distance=closest, id=currentclustid)

        # cluster ids that werenot in the original set are negtive
        currentclustid = -1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    for i in range(n): 
        print ' ',
    if clust.id < 0:
        print '-'
    else:
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

    if clust.left != None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n+1)


blognames, words, data = readfile('blogdata.txt')
clust = hcluster(data)
printclust(clust, labels=blognames)
