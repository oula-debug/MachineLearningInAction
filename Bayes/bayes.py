# -*- coding:utf8 -*-

from numpy import *
import numpy as np
def loadDataSet():
    '''
    实验样本
    :return:
    '''
    postingList = [['my', 'dog', 'has', 'flea', 'problem', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    # 0代表正常言论，1代表侮辱性言论
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    # 创建一个包含在所有文档中出现的不重复词列表
    # 创建一个空集
    vocabSet = set([])
    # 将每篇文档返回的新词集合添加到该集合中
    # 创建两个集合的并集
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    '''
    遍历输入的文件查看该单词是否出现，出现该单词则将该单词置为1
    :param vocabList:词汇表
    :param inputSet: 某个文档
    :return: 文档向量，向量的每一元素为1或0，分别表示词汇表中的单词在输入文档中是否出现
    '''
    # 创建一个所含元素都为0的向量；和词汇表等长
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            # index()函数用于从列表中找出某个值第一个匹配项的索引位置
            returnVec[vocabList.index(word)] = 1
        else:
            print("The word: %s is not in my Vocabulary!" % word)
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    '''
    朴素贝叶斯分类器训练函数
    :param trainMatrix: 文档矩阵[[1,0,1,0,0...],[...],[...]......]
    :param trainCategory: 每篇文档类别标签构成的向量[0,1,0,1,0,1]
    :return:每个单词在对应类别下的概率以及该类别出现的概率
    '''
    # 文件数
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    # 1是侮辱性，0是正常，将标签值全加起来即为侮辱性的总数
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    # 类别为0的单词出现的总数
    # 为了防止某个单词不出现导致计算结果为0，将所有单词初始出现次数改为1，p0Num = zero(numWords)改为：
    p0Num = ones(numWords)
    # 类别为1的单词出现的总数
    p1Num = ones(numWords)
    # 类别0单词的总数；防止下溢出将分母初始化为2.0（原值为0.0）
    p0Denom = 2.0
    # 类别1单词的总数
    p1Denom = 2.0
    for i in range(numTrainDocs):
        # 计算侮辱性出现的次数
        if trainCategory[i] == 1:
            # 得到每个单词出现的次数的矩阵
            p1Num += trainMatrix[i]
            # 单词的总个数，单词出现置为1，未出现置为0
            p1Denom += sum(trainMatrix[i])
        else:
            # 正常词语出现的次数
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    '''
    对每个元素做除法
    类别1下，即侮辱性文档下，每个单词出现的概率[p(F1|C1),P(F2|C2)......]
    p1Vect = p1Num / p1Denom # [1,3,5,6....] / 90 -> [1/90,3/90,5/90....]
    
    同理：
    类别0下，即侮辱性文档下，每个单词出现的概率[p(F1|C0),P(F2|C0)......]
    p0Vect = p0Num / p0Denom # [1,3,5,6....] / 90 -> [1/90,3/90,5/90....]
    '''
    # 太多小数相乘会导致结果为0，因此取对数
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    '''

    :param vec2Classify: 要分类的向量即待测数据 [0,1,1,0,...]
    使用trainNB0得到的三个概率
    :param p0Vec：类别1，即每个单词在侮辱性文档的概率[log(P(F1|C1)),log(P(F2|C1)),...]
    :param p1Vec：类别0，即每个单词在正常文档的概率[log(P(F1|C0)),log(P(F2|C0)),...]
    :param pClass1: 类别1，侮辱性文档出现的概率
    :return:1 or 0
    '''

    # 计算公式 log(P(F1|C1)) + log(P(F2|C1)) + ... + log(P(Fn|C1)) + log(P(C))
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    '''
    测试朴素贝叶斯
    :return:
    '''
    # 1. 加载数据集
    listOposts,listClasses = loadDataSet()
    # 2. 创建唯一的单词集合
    myVocabList = createVocabList(listOposts)
    # 3. 计算单词是否出现并创建数据矩阵，出现为1，未出现为0
    trainMat = []
    for postinDoc in listOposts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    # 4. 计算不同类别出现概率以及不同类别下属性出现的概率
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as:', classifyNB(thisDoc, p0V, p1V, pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as :', classifyNB(thisDoc, p0V, p1V, pAb))

def bagOfWords2VecMN(vocabList, inputSet):
    '''
    遍历输入的文件查看该单词是否出现，出现该单词则将该单词加1
    :param vocabList: 词汇表
    :param inputSet: 输入文档
    :return:
    '''
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


########################################################################################################################
############################################### Part2.垃圾邮件 ##########################################################

def textParse(bigString):
    '''
    切分文本
    :param bigString:输入文本
    :return:切分后的字符串
    '''
    # 使用正则表达式来切分句子，其中分隔符是除单词数字外的任何字符串
    # if len(tok) > 2过滤掉长度小于3的字符串
    # tok.lower()将字符串全部转化成小写
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    # 导入spam与ham文件夹,并解析为词列表
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        # Unicode Error
        # worldList = textParse(open('email/spam/%d.txt' % i).read())
        worldList = textParse(open('email/spam/%d.txt' % i, 'rb').read().decode('GBK', 'ignore'))
        docList.append(worldList)
        fullText.extend(worldList)
        classList.append(1)
        # Unicode Error
        # worldList = textParse(open('email/ham/%d.txt' % i).read())
        worldList = textParse(open('email/ham/%d.txt' % i, 'rb').read().decode('GBK', 'ignore'))
        docList.append(worldList)
        fullText.extend(worldList)
        classList.append(0)
    # 2. 创建唯一的单词集合
    vocabList = createVocabList(docList)
    # 3. 构建测试集与训练集
    trainingSet = list(range(50))
    testSet = []
    # 随机选10封邮件为测试集
    for i in range(10):
        # uniform(x, y) 方法将随机生成下一个实数，它在[x,y]范围内。
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    # 4. 计算单词是否出现并创建数据矩阵，出现为1，未出现为0
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    # 5. 计算不同类别出现概率以及不同类别下属性出现的概率
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print("The error rate is:", float(errorCount)/len(testSet))

########################################################################################################################
####################################### Part3.从个人广告中获取区域倾向 ####################################################
# 此处数据集缺失
# 朴素贝叶斯之新浪新闻分类: https://blog.csdn.net/c406495762/article/details/77500679

def calcMostFreq(vocabList, fullText):
    '''
    计算出现的频率
    :param vocabList:
    :param fullText:
    :return: 出现频率最高的前30个
    '''
    from operator import itemgetter
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sotrtedFreq = sorted(freqDict.items(), key=itemgetter(1), reverse=True)
    return sotrtedFreq[:30]

def localWords(feed1, feed0):
    docList = []
    classList = []
    fullText = []
    # 访问RSS源所有的列表条目 feed1['entries]
    # 找出两个中最小的一个
    minLen = min(len(feed1), len(feed0))
    for i in range(minLen):
        # 每次访问一条RSS源
        # 切分文本
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    # 2. 创建唯一的单词集合
    vocabList = createVocabList(docList)
    # 3. 去掉出现次数最高的30个词
    top30Words = calcMostFreq(vocabList, fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])

    # 4. 构建测试集与训练集
    import random
    # 生成随机取10个数, 为了避免警告将每个数都转换为整型
    testSet = [int(num) for num in random.sample(range(2 * minLen), 20)]
    # 并在原来的training_set中去掉这10个数
    trainingSet = list(set(range(2 * minLen)) - set(testSet))


    # 4. 计算单词是否出现并创建数据矩阵，出现为1，未出现为0
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    # 5. 计算不同类别出现概率以及不同类别下属性出现的概率
    p0v, p1v, pSpam = trainNB0(
        np.array(trainMat),
        np.array(trainClasses)
    )
    errorcount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),
                      p0v,
                      p1v,
                      pSpam
                      ) != classList[docIndex]:
            errorcount += 1
    print("The error rate is:{}".format(errorcount / len(testSet)))
    return vocabList, p0v, p1v


def getTopWords():
    import operator
    import feedparser
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0:
            topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0:
            topNY.append((vocabList[i], p1V[i]))
        sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
        print('\n-----------  SF ---------------\n')
        for item in sortedSF:
            print(item[0])
        sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
        print('\n-----------  NY ---------------\n')
        for item in sortedNY:
            print(item[0])



