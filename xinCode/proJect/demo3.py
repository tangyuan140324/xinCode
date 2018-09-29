import random
from math import ceil
import matplotlib.pyplot as plt
import numpy
import numpy as np
from PIL import Image
import math


angle = 40
im = Image.open('xiaojiejie.jpg').resize((800,800))
region = im.rotate(angle)
#region.show()
#region.save('test.jpg')
data = np.array(region)
newdata = [[max(pixel) for pixel in row] for row in data]
#Image.fromarray(newdata).show()
#print(newdata)
count = 0
for row in newdata:
    for pixel in row:
        if pixel ==0 :
            count+=1
print(count)

def area(a,t):
    r = t*math.pi/180
    print("radian angle",r)
    return (2*math.cos(r)*math.sin(r)*a**2)/(1+math.cos(r)+math.sin(r))**2

#print(np.sum(countdata))
print(count/(800**2))

print(area(800,angle)/800**2)
E = ((area(800,angle)/800**2)-(count/(800**2)))/(area(800,angle)/800**2)
print("Relative Error", E)
#dat1 = np.array([[0 if v < 128 else 1 for v in row] for row in data])


ar = np.array(Image.open('test.jpg'))

def generateCropPoints(ar):
    i = 0
    j = 0
    begpoint = []
    endpoint = []
    while i < 1:
        x = random.choice(range(401))
        y = random.choice(range(401))
        if max(ar[x][y]) > 0:
            i += 1
        begpoint = [x,y]
    while j < 1:
        m = random.choice(range(400, 800))
        n = random.choice(range(400, 800))
        if max(ar[m][n]) > 0:
            j += 1
        endpoint = [m,n]
    return begpoint,endpoint



print(generateCropPoints(ar))

a = 800
t = 30
area = area(a,t)
print(area)