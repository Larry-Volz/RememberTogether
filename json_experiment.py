import socket
from flask import jsonify 

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


order = {  
   "customer": {  
      "ZIPCODE":11779,
      "PHONE":1234567890,
      "ADDRESS2":" ",
      "STATE":"VA",
      "ADDRESS1":"123 Big St",
      "NAME":"John Doe",
      "COUNTRY":"US",
      "IP":ip_address,
      "EMAIL":"imaginologist@gmail.com",
      "CITY":"Richmond"
   },
   "products": [  
      {  
         "PRICE":39.95,
         "CARDMESSAGE":"This is a card message",
         "RECIPIENT":{  
            "ZIPCODE":11779,
            "PHONE":1234567890,
            "ADDRESS2":" ",
            "STATE":"DE",
            "ADDRESS1":"123 Big St",
            "NAME":"Howdy Doody",
            "COUNTRY":"US",
            "INSTITUTION":" ",
            "CITY":"Wilmington"
         },
         "DELIVERYDATE":"2016-02-29",
         "CODE":"F1-509"
      }
   ],
   "ccinfo": {  
      "AUTHORIZENET_TOKEN":"****"
   },
   "ordertotal":58.79
}
print(order)

""" NOTES:  CAST ZIPCODE AS TEXT!!! """

