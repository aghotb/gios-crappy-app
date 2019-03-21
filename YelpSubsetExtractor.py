import jsonlines
import json
from ast import literal_eval

def businessData(cities):
    """Writes a new json file containing business subset of Yelp dataset given a list of cities and returns a dictionary of their business IDs"""
    businessIDs = {}
    glutenCount = 0
    lactoseCount = 0
    categList = ['Pasta', 'Veggies', 'Barbeque', 'Fast Food', 'Pizza', 'Burgers', 'German', 'Japanese', 'Korean', 'Indian', 'Arabian', 'Italian', 'Chinese', 'Brazilian', 'Thai']
    writer = jsonlines.open('businessDataset.json', mode='w')
    with open('business.json', 'r', encoding='utf8') as businessJson:
        for jsonObjects in businessJson:
            tempDict = json.loads(jsonObjects)
            if tempDict['city'].lower() in cities and 'Restaurants' in str(tempDict['categories']) or 'Food' in str(tempDict['categories']):
                writer.write(tempDict)
                #name, address, city, state, postal_code, latitude, longitude, stars, breakfast, lunch, dinner, gluten-free, dairy-free
                businessIDs[tempDict['business_id']] = [tempDict['name'], tempDict['address'], tempDict['city'],
                                                        tempDict['state'], tempDict['postal_code'], tempDict['latitude'], tempDict['longitude'], tempDict['stars'], False, False, False, False, False, 2, []]
                if tempDict['attributes'] != None:
                    if 'GoodForMeal' in tempDict['attributes'] and tempDict['attributes']['GoodForMeal'] != 'None' and tempDict['attributes']['GoodForMeal'] != '{}':
                        businessIDs[tempDict['business_id']][8] = literal_eval(tempDict['attributes']['GoodForMeal'])['breakfast']
                        businessIDs[tempDict['business_id']][9] = literal_eval(tempDict['attributes']['GoodForMeal'])['lunch']
                        businessIDs[tempDict['business_id']][10] = literal_eval(tempDict['attributes']['GoodForMeal'])['dinner']
                    if 'DietaryRestrictions' in tempDict['attributes'] and tempDict['attributes']['DietaryRestrictions'] != 'None' and tempDict['attributes']['DietaryRestrictions'] != '{}':
                        businessIDs[tempDict['business_id']][11] = literal_eval(tempDict['attributes']['DietaryRestrictions'])['gluten-free']
                        if literal_eval(tempDict['attributes']['DietaryRestrictions'])['dairy-free'] == True or literal_eval(tempDict['attributes']['DietaryRestrictions'])['vegan'] == True:
                            businessIDs[tempDict['business_id']][12] = True
                    if 'RestaurantsPriceRange2' in tempDict['attributes'] and tempDict['attributes']['RestaurantsPriceRange2'] != 'None' and tempDict['attributes']['RestaurantsPriceRange2'] != '{}':
                        businessIDs[tempDict['business_id']][13] = int(tempDict['attributes']['RestaurantsPriceRange2'])
                if 'Gluten-Free' in str(tempDict['categories']):
                    businessIDs[tempDict['business_id']][11] = True
                if 'Vegan' in str(tempDict['categories']):
                    businessIDs[tempDict['business_id']][12] = True
                for word in categList:
                    if word in str(tempDict['categories']):
                        businessIDs[tempDict['business_id']][14].append(word)
    writer.close()
    with open('businessIDName.json', 'w') as outputFile:
        json.dump(businessIDs, outputFile)
    return businessIDs

def createDataset(businessIDs, dataset):
    """Writes a new json file containing subset of given Yelp dataset given a dictionary of business IDs to specify which businesses"""
    writer = jsonlines.open(dataset + 'Dataset.json', mode='w')
    with open(dataset + '.json', 'r', encoding='utf8') as dataJson:
        for jsonObjects in dataJson:
            tempDict = json.loads(jsonObjects)
            if tempDict['business_id'] in businessIDs:
                writer.write(tempDict)
    writer.close()

def createGlycemicFood():
    foodDict = {}
    tempArr = []
    with open('glycemicIndexed.txt', 'r') as inputFile:
        for line in inputFile:
            tempArr = line.split()
            if len(tempArr) == 2:
                foodDict[tempArr[0]] = tempArr[1]
            else:
                foodDict[tempArr[0] + ' ' + tempArr[1]] = tempArr[2]
    
    with open('glycemicFood.json', 'w') as outputFile:
        json.dump(foodDict, outputFile)
        

def main():
    cityUsed = ['las vegas', 'phoenix', 'tempe', 'henderson']
    businessIDs = businessData(cityUsed)
    createDataset(businessIDs, 'review')
    createDataset(businessIDs, 'photo')
    createDataset(businessIDs, 'tip')
    createGlycemicFood()
    
    


if __name__ == '__main__':
    main()
