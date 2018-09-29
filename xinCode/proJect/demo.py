#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import jieba
import re

x1=[
        [
            195.3255078125,
            183.0486328125,
            179.351796875
        ],
        [
            214.309140625,
            210.658984375,
            211.2471484375
        ],
        [
            202.3790234375,
            166.9673046875,
            154.0208203125
        ],
        [
            209.0726171875,
            205.010390625,
            204.544453125
        ],
        [
            238.7366015625,
            238.7067578125,
            239.9407421875
        ],
        [
            218.8822265625,
            208.1213671875,
            205.4421875
        ],
        [
            117.9749609375,
            115.0467578125,
            115.4662890625
        ],
        [
            103.36140625,
            101.23453125,
            101.667578125
        ],
        [
            100.8632421875,
            100.454140625,
            102.7946875
        ],
        [
            217.9459765625,
            217.2511328125,
            220.060078125
        ],
        [
            214.361796875,
            212.471796875,
            213.341796875
        ],
        [
            139.04578125,
            138.388046875,
            139.7734765625
        ],
        [
            90.1326953125,
            90.1326953125,
            91.8684375
        ],
        [
            109.9859375,
            102.9802734375,
            103.1705078125
        ],
        [
            233.7355859375,
            229.3083984375,
            230.2776953125
        ],
        [
            202.9949609375,
            201.8049609375,
            200.4649609375
        ],
        [
            117.8308203125,
            117.295859375,
            117.7813671875
        ],
        [
            90.5236328125,
            90.5236328125,
            91.4126953125
        ],
        [
            125.9088671875,
            111.0253125,
            112.4703515625
        ],
        [
            240.01421875,
            214.895078125,
            207.477890625
        ],
        [
            189.5584765625,
            188.49328125,
            186.299921875
        ],
        [
            145.448984375,
            117.1910546875,
            94.8725390625
        ],
        [
            122.9123046875,
            92.393203125,
            70.0478515625
        ],
        [
            180.5613671875,
            125.00890625,
            110.461953125
        ],
        [
            231.6116015625,
            124.142109375,
            156.1423828125
        ]
    ]
x2 = [
        [
            161.168203125,
            153.7276171875,
            140.3741015625
        ],
        [
            172.8205078125,
            166.29578125,
            153.5386328125
        ],
        [
            185.085390625,
            179.6289453125,
            167.61
        ],
        [
            198.32890625,
            194.8431640625,
            182.7651953125
        ],
        [
            203.3753125,
            200.4071875,
            188.7715625
        ],
        [
            160.106796875,
            150.6096875,
            135.905859375
        ],
        [
            168.9613671875,
            160.5280859375,
            146.6840625
        ],
        [
            164.4393359375,
            155.6860546875,
            141.4343359375
        ],
        [
            145.2842578125,
            134.8740625,
            119.9710546875
        ],
        [
            192.369609375,
            186.5020703125,
            173.85953125
        ],
        [
            193.438359375,
            189.3488671875,
            178.03640625
        ],
        [
            192.8846875,
            186.9978515625,
            174.158046875
        ],
        [
            150.0584375,
            139.033203125,
            123.699765625
        ],
        [
            152.1544921875,
            140.7068359375,
            124.5706640625
        ],
        [
            179.315078125,
            171.3958984375,
            158.055078125
        ],
        [
            177.2054296875,
            170.633046875,
            157.0620703125
        ],
        [
            201.9102734375,
            198.4113671875,
            186.6328515625
        ],
        [
            179.1423828125,
            171.29203125,
            156.7809765625
        ],
        [
            188.39375,
            182.8172265625,
            169.993671875
        ],
        [
            192.2240234375,
            186.4007421875,
            173.8370703125
        ],
        [
            170.6685546875,
            166.0113671875,
            153.713359375
        ],
        [
            197.145,
            193.895625,
            182.205390625
        ],
        [
            178.7626953125,
            171.6416015625,
            157.3237109375
        ],
        [
            153.90546875,
            143.815,
            128.4088671875
        ],
        [
            152.6725390625,
            143.13921875,
            129.1109375
        ]
    ]

children = 100

def genRandomW(children):
    W = [np.random.rand(25) for i in range(children)]
    return W

def distance(x1,x2,w):
    D =[np.sum([(x1[i][j]-x2[i][j])**2 for j in range(3)]) for i in range(25)]
    d = np.sum(np.multiply(w,D))
    print(d)
    return d

def sortedLangauge(titleList):
    N = len(titleList)
    x = "".join(titleList)
    #print(x)
    y = re.findall(r"(-.*?jpg)",x,re.S)

    for string in y:
        x = x.replace(string, '')

    #print(x)
    z = jieba.cut(x)

    s = ", ".join(z)
    #print(s)
    sList = s.split(',')
    sList = [x.strip() for x in sList]

    h = [[item, np.sum([1 if elem == item else 0 for elem in sList ])] for item in sList]

    def getKey(item):
        return item[1]

    h=sorted(h,key=getKey,reverse=True)

    #print(h)

    sortedKeywordsList = []
    for item in h:
        if item not in sortedKeywordsList:
            sortedKeywordsList.append(item)
    return sortedKeywordsList,N

def describe(sortedKeywordsList,N):
    # N titles
    #Returns description = [[keyword,probability p]], where len(description) >= 3, and subsequent probability(n>3) >= 0.8
    for i in range(len(sortedKeywordsList)):
        sortedKeywordsList[i][1] /= float(N)
    description = sortedKeywordsList[:3]
    print(description)
    added = [keyword for keyword in sortedKeywordsList[3:] if keyword[1] >= 0.8]
    print(added)
    description += added
    return description

titleList = ['2017冬季加绒连帽卫衣女宽松韩版拼色拼接加厚套头外套上衣女绒衫-tmall.com天猫_561598419471_3.jpg', '2017春夏新品拼接拼色显瘦半身裙女高腰长裙中长款裙子亚麻A字裙-tmall.com天猫_547029300649_4.jpg', '2017新款秋季套装男青年时尚休闲帅气两件套长袖T恤长裤一套衣服-tmall.com天猫_555743109285_4.jpg', '2017新款男士秋季卫衣套头韩版修身春秋学生日系潮流圆领宽松衣服-tmall.com天猫_557569241786_1.jpg', '2017新款秋季圆领羽毛套头卫衣男士青少年休闲韩版潮流外套打底衫-tmall.com天猫_558453719809_0.jpg']
h,N = sortedLangauge(titleList)
print(h)
print(N)
print(describe(h,N))

def score(description, targetTitle):
    #targetTitle is a string
    #description  = [[keyword,probability]]
    score = 0
    for keyword in description:
        if keyword[0] in targetTitle:
            score += 1
    score = score/len(description)
    return score

sc = score(describe(h,N),"2017夏季新款韩版男士体恤POLO衫 丅恤夏装修身男士衬衫领短袖t恤")
print(sc)

