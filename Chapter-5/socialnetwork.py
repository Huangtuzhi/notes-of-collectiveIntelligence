import math
from PIL import Image, ImageDraw
import optimization

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'),
('Mike', 'Joe'),
('Miranda', 'Mike'),
('Violet', 'Augustus'),
('Miranda', 'Willy'),
('Charlie', 'Mike'),
('Veruca', 'Joe'),
('Miranda', 'Augustus'),
('Willy', 'Augustus'),
('Joe', 'Charlie'),
('Veruca', 'Augustus'),
('Miranda', 'Joe')]


def crosscount(v):
    loc = dict([(people[i], (v[i*2], v[i*2 + 1])) for i in range(0, len(people))])
    total = 0
    
    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i + 1, len(links)):
            # Get the locations

            (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
            (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]

            den = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)

            # den == 0 if the lines are parallel
            if den == 0:
                continue

            # Otherwise ua and ub are the fraction of the line where they cross
            ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)) / den
            ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / den
            # print ua, ub

            # print "here"
            if ua > 0 and ua < 1 and ub > 0 and ub < 1:
                # print "here"
                total += 1
    return total


def drawnetwork(sol):
    img = Image.new('RGB', (400, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Create the position dict
    pos = dict([(people[i], (sol[i*2], sol[i*2 + 1])) for i in range(0, len(people))])

    # Draw links
    for (a, b) in links:
        draw.line((pos[a], pos[b]), fill=(255, 0, 0))

    # Draw people
    for n, p in pos.items():
        draw.text(p, n, (0, 0, 0))

    img.save('test.jpg', 'JPEG')


domain = [(10, 370)] * (len(people)*2)
# sol = optimization.randomoptimize(domain, crosscount)
# print sol
# print crosscount(sol)

sol = optimization.annealingoptimize(domain, crosscount, step=50, cool=0.99)
print sol
drawnetwork(sol)
# print crosscount(sol)