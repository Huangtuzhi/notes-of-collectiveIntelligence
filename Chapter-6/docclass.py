import re
import math

def getwords(doc):
    splitter = re.compile('\\W*')
    words = [s.lower() for s in splitter.split(doc)
        if len(s) > 2 and len(s) < 20]

    return dict([(w, 1) for w  in words])


class classifier:
    def __init__(self, getfeatures, filename=None):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures

    # Increase the count of a feature/category pair
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # Increase the count of a category
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    # The number of times a feature has appeared in a categoru
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # The number of items in a category
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # The total number of items
    def totalcount(self):
        return sum(self.cc.values())

    # The list of all categories
    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)

        # Increase the count for this category
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')

class naivebayes(classifier):
    def docprob(self, item, cat):
        features = self.getfeatures(item)

        # Multiply the probabilities of all the features together
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
            return p

# print getwords("This function breaks up the text into words words")
cl = classifier(getwords)
sampletrain(cl)
print cl.fcount('quick', 'good')
print cl.catcount('good')
print cl.fprob('quick', 'good')