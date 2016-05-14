import math

critics = {
'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: 
        return 0

    sim_of_squares = 0
    for item in si:
        sim_of_squares += pow(prefs[person1][item] - prefs[person2][item], 2)
    return 1 / (1 + sim_of_squares)


# Returns the Person correlation coefficient
def sim_person(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)

    if n == 0:
        return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    return num / den


def topMatches(prefs, person, n=5, similarity=sim_person):
    scores = [(similarity(prefs, person, other), other) 
                  for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_person):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    result = {}
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(itemPrefs))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:
            if item2 in userRatings:
                continue

            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path=r'C:\Users\titus\Desktop\Doing\CollectiveIntelligence\Chapter-2\ml-100k'):
    movies = {}
    for line in open(path+'\u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    # load data
    prefs = {}
    for line in open(path+'\u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs



# print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
# print sim_person(critics, 'Lisa Rose', 'Gene Seymour')
# print topMatches(critics, 'Toby')
# print getRecommendations(critics, 'Toby')
# print getRecommendations(critics, 'Toby', similarity=sim_distance)
# print transformPrefs(critics)

# movies = transformPrefs(critics)
# print getRecommendations(movies, 'Just My Luck')

# itemsim = calculateSimilarItems(critics)
# print getRecommendedItems(critics, itemsim, 'Toby')

# user-based recommendation
# prefs = loadMovieLens()
# print getRecommendations(prefs, '87')[0:30]

# item-based recommendation
prefs = loadMovieLens()
itemsim = calculateSimilarItems(prefs, n=50)
print getRecommendedItems(prefs, itemsim, '87')[0:30]