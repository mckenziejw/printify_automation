import requests
import yaml
import json
from pprint import pprint
import os
from base64 import b64encode

# class Shop:

#     def __init__(self, shop_name):
#         self.shop_name = shop_name
#         return self

#     def getShopMetadata(self):
#         return self

# class Product:

#     def __init__(self, shop_id, product_id = False):
#         if product_id:
#             self.product_id = product_id
#         self.shop_id = shop_id
#         response = requests.get(self.base_url + "shops/{}/products/{}.json".format(self.product_id, self.shop_id), headers={"Authorization": "Bearer " + self.token + ""})
#         if response.status_code == 200:
#             self.details = response.json()

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
        # for p in self.get_products():
        #     self.products.append(p)

    def get_shops(self):
        response = requests.get(self.base_url + "shops.json", headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def connect(self):
        response = requests.get(self.base_url + "shops.json", headers={"Authorization": "Bearer " + self.token + ""})
    
    def get_catalog_blueprints(self):
        response = requests.get(self.base_url + "catalog/blueprints.json", headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def get_catalog_blueprint(self, blueprint_id):
        response = requests.get(self.base_url + "catalog/blueprints/{}.json".format(blueprint_id), headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def get_variants(self, blueprint_id, provider_id):
        response = requests.get(self.base_url + "catalog/blueprints/{}/print_providers/{}/variants.json".format(blueprint_id, provider_id), headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def get_products(self):
        response = requests.get(self.base_url + "shops/{}/products.json".format(self.shop_id), headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def get_product(self, product_id):
        response = requests.get(self.base_url + "shops/{}/products/{}.json".format(self.shop_id, product_id), headers={"Authorization": "Bearer " + self.token + ""})
        return response.json()
    
    def upload_image(self, filename, image):
        upload_data = {
            'file_name': filename,
            'contents': image.decode('utf-8')
        }
        response = requests.post(self.base_url + "uploads/images.json", headers={"Authorization": "Bearer " + self.token + ""}, json=upload_data)
        return response.json()['id']
    
    def create_product(self, product):
        response = requests.post(self.base_url + "shops/{}/products.json".format(self.shop_id), headers={"Authorization": "Bearer " + self.token + ""}, json=product)
        return response.json()

def main():
    token = ""
    template = 'square_canvas_template.json'
    upload_folder = 'to_publish'
    with open('token', 'r') as f:
        token = f.read()
    test_client = PrintifyClient(token, "Chaos Canvas")
    product_template = {}
    # Load the product template
    with open(template, 'r') as f:
        product_template = json.load(f)
    
    # Loop through images
    for filename in os.listdir(upload_folder):
        # Upload image
        f_path = os.path.join(upload_folder, filename)
        f = open(f_path, 'rb')
        upload_file = b64encode(f.read())
        f.close()
        image_id = test_client.upload_image(filename, upload_file)
        f = open(template)
        # Push product
        new_product = json.load(f)
        new_product['print_areas'][0]['placeholders'][0]['images'][0]['id'] = image_id
        added_product = test_client.create_product(new_product)
        pprint(added_product)

if __name__ == '__main__':
    main()