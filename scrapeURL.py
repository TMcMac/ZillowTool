import csv
import json
import pyzill
import sys

def ingestProperty(url):
    # data_dict is the dictionary of info we will compose to put into a spreadsheet
    data_dict = {}
    # pyzilla is the open source package to grab all data from a listing
    data = pyzill.get_from_property_url(url,"")
    jsondata = json.dumps(data, indent=2)

    # write the full data to a json file for review
    f = open("details.json", "w")
    f.write(jsondata)
    f.close()

    # load the full json to parse through
    propertyDict = json.loads(jsondata)
    
    # Get certain key data points and build a dict to load into a csv
    data_dict["zpid"] = propertyDict["zpid"]
    data_dict["address"] = propertyDict["address"]['streetAddress'] + ", " + propertyDict["address"]["city"] + " " + propertyDict["address"]["state"]+ ", " + propertyDict["address"]["zipcode"]

    data_dict["bedrooms"] = propertyDict["bedrooms"]
    data_dict["bathrooms"] = propertyDict["bathrooms"]
    data_dict["livingArea"] = propertyDict["livingArea"]
    data_dict["lotSize"] = propertyDict["resoFacts"]["lotSize"]
    data_dict["yearBuilt"] = propertyDict["yearBuilt"]

    data_dict["price"] = propertyDict["price"]
    data_dict["zestimate"] = propertyDict["zestimate"]
    data_dict["rentZestimate"] = propertyDict["rentZestimate"]
    data_dict["monthlyHoaFee"] = propertyDict["monthlyHoaFee"]
    match = ["Elementary","Primary","Intermediate"]
    for school in propertyDict["schools"]:
        grades = str(school["grades"])
        name = school["name"]
        distance = school["distance"]
        rating = school["rating"]

        if any(x in name for x in match):
            level = "Primary"
        elif "Middle" in name:
            level = "Middle"
        elif "High" in name:
            level = "High"
        else:
            level = "Null"
            print("Working on: {}\nSchool names not lining up by level.".format(data_dict["zpid"]))

        details = f"{name}\nDistance: {distance}\nGrades: {grades}\nRating: {rating}/10"
        data_dict[level] = details

    data_dict["description"] = propertyDict["description"]
    data_dict["URL"] = url
    data_dict["timeOnZillow"] = propertyDict["timeOnZillow"]
    
    

            
    return(data_dict)

def addHouseToCSV(house):
    if(type(house) is dict):
        field_names=house.keys()
        houses = []
        houses.append(house)
    elif(type(house) is list):
        field_names=house[0].keys()
        houses = house

    with open('Homes.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(houses)

if __name__ == '__main__':
    
    if (len(sys.argv) > 1):
    # Take in a single URL when the program is run with python3.11 scrapeURL.py URL
        # Check the url looks valid
        url = sys.argv[1]
        https = url[0:5]
        zpid = url[-5:len(url)]
        if(https == "https" and zpid == "zpid/"):
            # If it looks good begining and end run the runction
            a_house = ingestProperty(url)
            addHouseToCSV(a_house)
    else:
        #If you have several URLS to run you can put them in an array and then run that
        urls = ["https://www.zillow.com/homedetails/8227-Amber-Cove-Dr-Humble-TX-77346/28208964_zpid/",
                "https://www.zillow.com/homedetails/1814-Venus-Dr-New-Caney-TX-77357/28743344_zpid/",
                "https://www.zillow.com/homedetails/7815-Tamarron-Ct-Humble-TX-77346/28258463_zpid/",
                "https://www.zillow.com/homedetails/7902-Twining-Oaks-Ln-Spring-TX-77379/28163753_zpid/",
                "https://www.zillow.com/homedetails/5011-Cottage-Glen-Ct-Kingwood-TX-77345/52410710_zpid/",
                "https://www.zillow.com/homedetails/3331-Lost-Maple-Forest-Ct-Kingwood-TX-77345/84010388_zpid/"
                ]
        houses = []
        for url in urls:
            result = ingestProperty(url)
            houses.append(result)
        addHouseToCSV(houses)