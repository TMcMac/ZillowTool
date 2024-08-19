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
        urls = ["https://www.zillow.com/homedetails/3501-Chesapeake-Blvd-Norfolk-VA-23513/79234313_zpid/",
                "https://www.zillow.com/homedetails/3501-Chesapeake-Blvd-Norfolk-VA-23513/79234313_zpid/",
                "https://www.zillow.com/homedetails/5968-Glen-View-Dr-Virginia-Beach-VA-23464/60625798_zpid/",
                "https://www.zillow.com/homedetails/9405-Alpine-Ct-Norfolk-VA-23503/79199510_zpid/",
                "https://www.zillow.com/homedetails/8608-Sturgis-St-Norfolk-VA-23503/79195058_zpid/",
                "https://www.zillow.com/homedetails/1121-Kempsville-Rd-Norfolk-VA-23502/79194341_zpid/",
                "https://www.zillow.com/homedetails/1104-Minden-Rd-Virginia-Beach-VA-23464/60642896_zpid/",
                "https://www.zillow.com/homedetails/1297-River-Oaks-Dr-Norfolk-VA-23502/79235974_zpid/",
                "https://www.zillow.com/homedetails/2557-Elon-Dr-Virginia-Beach-VA-23454/60718176_zpid/",
                "https://www.zillow.com/homedetails/9557-10th-Bay-St-Norfolk-VA-23518/79197512_zpid/",
                "https://www.zillow.com/homedetails/817-Orkney-Ct-Chesapeake-VA-23322/61412242_zpid/",
                "https://www.zillow.com/homedetails/3021-E-Ocean-View-Ave-Norfolk-VA-23518/338689383_zpid/",
                "https://www.zillow.com/homedetails/334-Dorwin-Dr-Norfolk-VA-23502/79231793_zpid/",
                "https://www.zillow.com/homedetails/5279-E-Valleyside-Ct-Virginia-Beach-VA-23464/60642724_zpid/",
                "https://www.zillow.com/homedetails/3884-Stumpy-Lake-Ln-Virginia-Beach-VA-23456/81334098_zpid/",
                "https://www.zillow.com/homedetails/2505-Pinto-Dr-Virginia-Beach-VA-23456/60657732_zpid/"
                ]
        houses = []
        for url in urls:
            result = ingestProperty(url)
            houses.append(result)
        addHouseToCSV(houses)