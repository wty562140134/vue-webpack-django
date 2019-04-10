#coding=utf-8
from math import cos,sin,pow,tan,sqrt,asin,degrees
# Create your views here.

def lengs(lengs, y):
    f = 0
    if lengs < 0:
        f = 0
    else:
        f = 1
    lengs = abs(lengs)
    if y == 1:
        lengs = lengs  - lengs * 0.1821
    else:
        lengs = lengs  - lengs * 0.10131

    a = asin(lengs / (6371 * 2000))
    jd = degrees(a)
    bc = 2 * 3.1415926 * 6371 * 1000 * (jd / 180)
    return (f, bc)

def pmtobd(zblatitude,zblongitude):

    x = 11438346.185071
    y = 2873446.894376
    l = 102.751291 * 100000
    b = 25.130219 * 100000
    r = lengs(x - zblongitude, 0)
    if r[0] == 0:
        nl = l + r[1]
    else:
        nl = l - r[1]
    r1 = lengs(y - zblatitude, 1)
    if r1[0] == 0:
        nb = b + r1[1]
    else:
        nb = b - r1[1]

    renl=nl / 100000
    renb=nb / 100000
    return (renl,renb)
