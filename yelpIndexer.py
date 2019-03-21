import json
import jsonlines

def reviewScanner(reviewData, foodDict, businessIDNamesDict):
    dataString = str(reviewData["text"])
    totalFoods = 0
    totalGL = 0
    prev = ''
    for word in dataString.split():
        if word in foodDict:
            totalGL += int(foodDict[word])
            totalFoods += 1
        elif prev + word in foodDict:
            totalGL += int(foodDict[prev + word])
            totalFoods += 1
        prev = word
    return totalGL, totalFoods

def jsonCreator(businessIDNamesDict, restaurantsGLDict):
    writer = jsonlines.open('indexedData.json', mode='w')
    tempDict = {}
    count = 0
    for key, value in businessIDNamesDict.items():
        tempDict['business_id'] = key
        tempDict['name'] = value[0]
        tempDict['address'] = value[1]
        tempDict['city'] = value[2]
        tempDict['state'] = value[3]
        tempDict['postal_code'] = value[4]
        tempDict['latitude'] = value[5]
        tempDict['longitude'] = value[6]
        tempDict['stars'] = value[7]
        tempDict['breakfast'] = value[8]
        tempDict['lunch'] = value[9]
        tempDict['dinner'] = value[10]
        tempDict['gluten_free'] = value[11]
        tempDict['dairy_free'] = value[12]
        
        DBFriendly = False
        if key in restaurantsGLDict:
            if restaurantsGLDict[key][1] > 5:
                val = restaurantsGLDict[key][0] / restaurantsGLDict[key][1]
                if val <= 10.5:
                    DBFriendly = True
                    
        tempDict['diabetic_friendly'] = DBFriendly
        tempDict['price_range'] = value[13]
        tempDict['categories'] = value[14]
        writer.write(tempDict)
    writer.close()

def indexer():
    restaurantsGLDict = {}
    with open('glycemicFood.json', 'r') as inputFile:
        glycemicDict = json.load(inputFile)
    with open('businessIDName.json', 'r') as inputFile:
        businessIDNamesDict = json.load(inputFile)
    with open('reviewDataset.json', 'r', encoding='utf8') as reviewJson:
        for jsonObjects in reviewJson:
            tempDict = json.loads(jsonObjects)
            businessID = tempDict['business_id']
            totalGL, totalFoods = reviewScanner(tempDict, glycemicDict, businessIDNamesDict)
            if businessID in restaurantsGLDict:
                restaurantsGLDict[businessID][0] += totalGL
                restaurantsGLDict[businessID][1] += totalFoods
            else:
                restaurantsGLDict[businessID] = [totalGL, totalFoods]
    jsonCreator(businessIDNamesDict, restaurantsGLDict)
def main():
    indexer()


if __name__ == '__main__':
    main()
