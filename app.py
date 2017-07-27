#!/usr/bin/env python

import urllib
import json
import os
import re


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
QR=['0','1','2','3','4','5','6','7']

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "search_property":
        return {}
    global city_names
    city_names=processlocation(req)
    global QR
    global intent_name
    intent_name=processIntentName(req)

    if "ChooseCity" in intent_name:        
        QR[0]="Sector in "+city_names
        QR[1]="Other City?Specify"
        QR[2]="(Y)"
        QR[3]="Hot Property"
        QR[4]="Price Range"
        QR[5]="Land Area"
        QR[6]="Property Type"
    elif "ChooseSector" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Sector?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type" 
        QR[6]="Change Location" 
    elif "ChangeType" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Type?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type"  
        QR[6]="Change Location"  
    elif "ChooseHotProperties" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Change Location"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type" 
        QR[6]="Change City" 
    elif "ChoosePlotArea" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Area?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"
        QR[6]="Property Type" 
    elif "DefinePriceRange" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Range?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type" 
        QR[6]="Change Location"
    elif "serach_property" in intent_name:
	R[0]="(Y)"
        QR[1]="Other Range?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type" 
        QR[6]="Change Location"

    city_names=processlocation(req)
    sector_names=processSector(req)
    property_type=processPropertyType(req)
    unit_property=processUnit(req)
    area_property=processArea(req)
    NoOfDays=processDate(req)
    DateUnit=processDateUnit(req)
    school=processSchool(req)
    malls=processMalls(req)
    transport=processTransport(req)
    security=processSecurity(req)
    airport=processAirport(req)
    fuel=processFuel(req)
    #minimum_value=processMinimum(req)
    maximum_value=processMaximum(req)
    latest=processLatestProperties(req)
    project_name=processProjectName(req)
    #if minimum_value > maximum_value:
    #    minimum_value,maximum_value=maximum_value,minimum_value
    #else:
    # minimum_value,maximum_value=minimum_value,maximum_value    
    #baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&loc1="+sector_names+"&price_min="+maximum_value+"&price_max=0&land_area="+unit_property+"&min_r=0&max_r="+area_property+"&estate_agent=&hot="+latest+"&purpose=Sell&property_type="+property_type+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    result = urllib.urlopen(baseurl).read()
    print(result)
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processIntentName(req):
    result = req.get("result")
    parameters = result.get("metadata")
    intent = parameters.get("intentName")
    return intent

def process_location(req):
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")
print(result)
    return location

def process_city(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("")
    return city
def processSector(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sector = parameters.get("Location")
    return sector

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    minimum = parameters.get("number")
    return minimum

def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("number1")
    return maximum


def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType

def processLatestProperties(req):
    result = req.get("result")
    parameters = result.get("parameters")
    latest = parameters.get("LatestProperties")
    return latest

def processUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    unit = parameters.get("Unit")
    return unit

def processArea(req):
    result = req.get("result")
    parameters = result.get("parameters")
    area = parameters.get("AreaNumber")
    return area

def processDate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    days = parameters.get("NoOfDays")
    return days

def processDateUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    dayUnit = parameters.get("DayUnit")
    return dayUnit

def processSchool(req):
    result = req.get("result")
    parameters = result.get("parameters")
    school = parameters.get("school")
    return school

def processMalls(req):
    result = req.get("result")
    parameters = result.get("parameters")
    malls = parameters.get("malls")
    return malls

def processTransport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    transport = parameters.get("transport")
    return transport

def processSecurity(req):
    result = req.get("result")
    parameters = result.get("parameters")
    security = parameters.get("security")
    return security

def processAirport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    airport = parameters.get("airport")
    return airport

def processFuel(req):
    result = req.get("result")
    parameters = result.get("parameters")
    fuel = parameters.get("fuelstation")
    return fuel

def processProjectName(req):
    result = req.get("result")
    parameters = result.get("parameters")
    project_name = parameters.get("ProjectName")
    return project_name    
   
def makeWebhookResult(data):
    i=0
    length=len(data)
    varibale1='344'
    variable2='322'
    variable3='4332'
    variable4='4321'
    row_id=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_title=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_location=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_price=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_slug=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_number=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    row_image=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
    while (i <length):
        row_id[i]=data[i]['property_id']
        row_title[i]=data[i]['title']
        row_location[i]=data[i]['address']
        row_price[i]=data[i]['price']
        row_slug[i]=data[i]['slug']
        row_number[i]=data[i]['number']
        row_image[i]=data[i]['image']
        i+=1
    variable1=str(row_number[0])
    variable2=str(row_number[1])
    variable3=str(row_number[2])
    variable4=str(row_number[3]) 
    
    if "unable" in row_title[0]:
        message={
         "text":row_title[0],
         "quick_replies": [
           
                 {
                "content_type":"text",
                "title": "Buy Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
           
    }
    elif length==1:
                 message={
                   "attachment":{
                    "type":"template",
                       "payload":{
            "template_type":"generic",
            "elements":[
          {
             "title":row_title[0],
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0] ,
             "subtitle":row_location[0],
             "buttons":[
              {
              "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
              },
                 {
                "type":"element_share"
                  }
            ]
          }
        ]
      }
    },
                      "quick_replies": [
            {
                "content_type":"text",
                "title": QR[0],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[1],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[2],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[3],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[4],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[5],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                  {
                "content_type":"text",
                "title": QR[6],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": "Buy Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
  }
    elif length==2:
         message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row_title[0],
               "subtitle": row_location[0],
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
             "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                   {
                "title": row_title[1],
                "subtitle": row_location[1],
                 "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
             "payload":"+92"+variable2[1:]
            },
                     {
                "type":"element_share"
                    
                    }, 
                   ]
          }]
            
        }
      },
             "quick_replies": [
            {
                "content_type":"text",
                "title": QR[0],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[1],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[2],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[3],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[4],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                  {
                "content_type":"text",
                "title": QR[5],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                  {
                "content_type":"text",
                "title": QR[6],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": "Buy Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
    }
    else:
         message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [
                   {
               "title": row_title[0],
               "subtitle": row_location[0],
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                  
            }, 
                   ],
          }, 
                   {
               "title": row_title[1],
               "subtitle": row_location[1],
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                   {
               "title": row_title[2],
               "subtitle": row_location[2],
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[2],               
               "image_url":"https://www.aarz.pk/"+row_image[2]  ,
                "buttons": [{
               "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable3[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                   {
                "title": row_title[3],
                "subtitle": row_location[3],
                 "item_url": "https://www.aarz.pk/property-detail/"+row_slug[3],               
               "image_url":"https://www.aarz.pk/"+row_image[3]  ,
                "buttons": [{
               "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable4[1:]
            },
                     {
                "type":"element_share"
                    
                    }, 
                   ]
          }]
            
        }
      },
             "quick_replies": [
            {
                "content_type":"text",
                "title": QR[0],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[1],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[2],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[3],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[4],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                  {
                "content_type":"text",
                "title": QR[5],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                  {
                "content_type":"text",
                "title": QR[6],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": "Buy Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
    }
    speech = "Here are some properties with your choice: https://www.aarz.pk/search/"+row_slug[0] + " https://www.aarz.pk/property-detail/"+row_slug[1] +" Type: 'Hot Property','Price Range','Land Area','Change Location','Buy Property' "
      
    return {
        "speech": speech,
        "displayText": speech,
        "data":{"facebook":message}
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
