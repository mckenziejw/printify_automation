import requests
import yaml
import json
from pprint import pprint
import os
from base64 import b64encode

class PrintifyClient:
    base_url = "https://api.printify.com/v1/"

## curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer $PRINTIFY_API_TOKEN"
## content type shoudl be application/json;charset=utf-8
# Date/Time values are UTC


    def __init__(self, token, shop_name):
        self.token = token
        self.shop_id = 0
        #self.shop = shop
        response = requests.get(self.base_url + "shops.json", headers={"Authorization": "Bearer " + self.token + ""})
        for s in response.json():
            if s['title'] == shop_name:
                self.shop_id = s['id']
        # for p in self.get_listings():
        #     self.listings.append(p)

    def get_shops(self):

    def connect(self):

    
    def get_listings(self):

    
    def get_listing(self, listing_id):

    
    def upload_image(self, filename, image):
        upload_data = {
            'file_name': filename,
            'contents': image.decode('utf-8')
        }
        response = requests.post(self.base_url + "uploads/images.json", headers={"Authorization": "Bearer " + self.token + ""}, json=upload_data)
        return response.json()['id']
    
    def create_listing(self, listing):
        response = requests.post(self.base_url + "shops/{}/listings.json".format(self.shop_id), headers={"Authorization": "Bearer " + self.token + ""}, json=listing)
        return response.json()
