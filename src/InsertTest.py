import pandas as pd

def InsertPercentage(targetList):

    resultList = []

    SortList = []

    length = len(targetList)

    i = 0

    while i < length:

        targetNum = targetList[i]

        SortListLength = len(SortList)

        #充值j
        j = 0

        while j <= SortListLength:

            if j == SortListLength:
                SortList.insert(length,targetNum)
                resultList.append(1)
                break

            if targetNum < SortList[j]:
                SortList.insert(j,targetNum)
                resultList.append(j/SortListLength)
                break

            j = j + 1

        i = i + 1

    return SortList,resultList


if __name__ == "__main__":

    targetList = [0,9,3,1,5,6,3,7,5]
    SortList,resultList = InsertPercentage(targetList)
    print(SortList)
    print(resultList)
