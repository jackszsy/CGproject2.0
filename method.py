import os
import sys
import pandas as pd
import random
import math
from jikanpy import Jikan
import time

anime_name = [] #get from user
jikan = Jikan() #initialization

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def csvReader(filepath):
    colName = ['name', 'comedy', 'fantasy', 'historical', 'slice of life', 'sports', 'school', 'drama', 'game',
               'original', 'novel', 'manga']
    df = pd.read_csv(filepath)
    return df

def randomInput():
    listInput = []
    for i in range(21):
        listInput.append(i)
    random.shuffle(listInput)
    for j in range(11):
        del listInput[j]
    return listInput


def randomTestSample():
    sample = []
    n = random.randint(2, 6)
    for i in range(11):
        if i < n:
            sample.append(1)
        else:
            sample.append(0)
    random.shuffle(sample)
    return sample


def knn(listSample, listInput, df, K):
    knn = []
    t = 0
    for i in range(21):
        distanceLike = math.sqrt(
            (listSample[0] - df.comedy[i]) ** 2 + (listSample[1] - df.fantasy[i]) ** 2 +
            (listSample[2] - df.historical[i]) ** 2 + (listSample[3] - df.sliceOfLife[i]) ** 2 +
            (listSample[4] - df.sports[i]) ** 2 + (listSample[5] - df.school[i]) ** 2 +
            (listSample[6] - df.drama[i]) ** 2 + (listSample[7] - df.game[i]) ** 2 +
            (listSample[8] - df.original[i]) ** 2 + (listSample[9] - df.novel[i]) ** 2 +
            (listSample[10] - df.manga[i]) ** 2)

        if i in listInput:
            knn.append(['Selected', round(distanceLike, 2)])
        else:
            knn.append(['nonselected', round(distanceLike, 2)])

    knn.sort(key=lambda dis: dis[1])
    knn = knn[:K]
    return knn


def classifier(listKnn, K):
    numLike = 0
    numDislike = 0
    for i in range(K):
        if listKnn[i][0] == 'Selected':
            numLike += 1
        else:
            numDislike += 1

    if numLike > numDislike:
        return True
    else:
        return False


def restrictor(listResult, N):
    listOutput = []
    for i in range(len(listResult)):
        tmp = listResult[i][1]
        sum = 0
        for j in range(len(listResult[i][1])):
            sum += tmp[j]
            if tmp[j] == 0:
                sum = 0
                break
        avg = round(sum / len(tmp), 2)
        listOutput.append([listResult[i][0], avg])

    listOutput.sort(key=lambda dis: dis[1])
    listOutput = listOutput[:N]

    output = []
    for i in range(len(listOutput)):
        output.append(listOutput[i][0])

    if len(output) < 5:
        for i in range(5 - len(output)):
            while True:
                tmp = random.randint(0, 39)
                if tmp not in output:
                    output.append(tmp)
                    break

    return output


def run(testingData, trainingData, listInput, K, N):
    testSample = []
    for i in range(40):
        testSample.append([testingData.comedy[i], testingData.fantasy[i], testingData.historical[i]
                              , testingData.sliceOfLife[i], testingData.sports[i], testingData.school[i]
                              , testingData.drama[i], testingData.game[i], testingData.original[i]
                              , testingData.novel[i], testingData.manga[i]])

    result = []
    for i in range(40):
        listKnn = knn(testSample[i], listInput, trainingData, K)
        if classifier(listKnn, K):
            tmp = []
            for j in range(K):
                if listKnn[j][0] == 'Selected':
                    tmp.append(listKnn[j][1])
            result.append([i, tmp])
    # print(len(result))
    # print(result)
    output = restrictor(result, N)
    return output


def machine_learning(input):
    K = 5
    N = 5
    trainingData = csvReader('static/data/training_data.CSV')
    testingData = csvReader('static/data/testing_data.CSV')
    # It is a random input to simulate the user input
    listInput = input
    a = run(testingData, trainingData, listInput, K, N)
    for i in range(len(a)):
        anime_name.append(testingData.name[a[i]])
    return anime_name


def get_recommended_anime(anime_name):
    #Initialization
    ani = []

    #Search anime
    i = anime_name
    tmp = jikan.search('anime',i)

    #Extract required information
    res = tmp['results']
    ani.append(res[0]['title'])
    ani.append(res[0]['image_url'])
    ani.append(res[0]['synopsis'])
    ani.append(res[0]['type'])
    ani.append(res[0]['episodes'])
    ani.append(res[0]['score'])
    ani.append(res[0]['start_date'])
    ani.append(res[0]['end_date'])
    ani.append(res[0]['rated'])
    ani.append(res[0]['members'])
    time.sleep(1)
    return ani

def get_url(anime_name):
    temp = jikan.search('anime',anime_name)
    time.sleep(1)
    return temp['results'][0]['image_url']