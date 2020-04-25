from lib.products import Products
from lib.product_requests import Requests
from lib.rates import Rates, Countries
from lib.message import Message
from lib.findingAPI import API
import json
import os
import ast
import operator
import datetime
from operator import itemgetter
from collections import Counter

currDir = os.getcwd()
productsDir = currDir + "/lib/textfiles/products.json"
product_requestsDir = currDir + "/lib/textfiles/product_requests.json"
user_dataDir = currDir + "/lib/textfiles/user_data.json"
messagesDir = currDir + "/lib/textfiles/messages.json"
ebayDir = currDir + "/lib/textfiles/ebay.json"
resultsDir = currDir + "/lib/textfiles/myresults.json"
ebayresultsDir = currDir + "/lib/textfiles/ebayresults.json"
now = datetime.datetime.now()

class System:
    product_data = {}
    request_data = {}
    user_data = {}

    def __init__(self):
        pass

    def update_username(self, username, newusername):
        with open(messagesDir, "r") as f:
            messagesData = json.load(f)
        with open(user_dataDir, "r") as f:
            users = json.load(f)
        products = System().show_products()
        requests = System().show_requests()
        for m in messagesData["allMessages"]:
            if m["sender"] == username:
                m["sender"] = newusername
            if m["receiver"] == username:
                m["receiver"] = newusername
            m["message"] = m["message"].replace(username, newusername)
        for p in products["products"]:
            if p["_customer"] == username:
                p["_customer"] = newusername
        for r in requests["request"]:
            if r["_customer"] == username:
                r["_customer"] = newusername
            if r["_traveller"] == username:
                r["_traveller"] = newusername
        for u in users["user"]:
            for r in u["review"]:
                if r["reviewer"] == username:
                    r["reviewer"] = newusername
                r["comment"] = r["comment"].replace(username, newusername)
        with open(messagesDir, "w") as f:
            json.dump(messagesData, f, indent=4)
        with open(productsDir, "w") as f:
            json.dump(products, f, indent=4)
        with open(product_requestsDir, "w") as f:
            json.dump(requests, f, indent=4)
        with open(user_dataDir, "w") as f:
            json.dump(users, f, indent=4)

    def get_user(self, name):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["username"] == name:
                return element
    
    def get_completed(self, offers):
        offer = []
        for o in offers:
            if o["_status"] == "Completed":
                offer.append(o)
        print(offer)
        for o in offer:
            product = System().get_product(o['_name'])
            o["_image"] = product['_image']
        return offer
        
    def get_users_reviews(self, user):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for r in user["review"]:
            for u in datastore["user"]:
                if r["reviewer"] == "GlobeShoppers":
                    images.append(0)
                if r["reviewer"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def get_images(self, user):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for u in datastore["user"]:
            if user == u["username"]:
                if u["image"]:
                    return u["image"]
        return 0

    def get_users_requests(self, requests):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for r in requests:
            if r["_traveller"] == 0:
                images.append(0)
            for u in datastore["user"]:
                if r["_traveller"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def show_users_trending(self, trending):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for t in trending:
            for u in datastore["user"]:
                if t["_customer"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def show_users_requesters(self, request):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for r in request:
            for u in datastore["user"]:
                if r["_customer"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def get_users_items(self, matchResults):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for r in matchResults:
            for u in datastore["user"]:
                if r["_customer"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def get_users_offers(self, offers):
        images = []
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for o in offers:
            for u in datastore["user"]:
                if o["_customer"] == u["username"]:
                    if u["image"]:
                        images.append(u["image"])
                    else :
                        images.append(0)
                    break
        return images

    def get_username(self):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["login"] == "True":
                return element["username"]

    def get_user_email(self):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["login"] == "True":
                return element["email"]

    def create_user(self,username,email, password,city):
        data = {
            "username":username,
            "email": email,
            "password": password,
            "login": "True",
            "city":city,
            "aveRating": "0",
            "review": [],
            "trip": []

        }
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        datastore["user"].append(data)
        with open(user_dataDir, "w") as file:
            json.dump(datastore, file,indent= 4)
        return ""

    def dump_my_results(self,data):
        with open(resultsDir, "w") as file:
            json.dump(data, file,indent= 4)
        return ""

    def delete_my_results(self):
        data = []
        with open(resultsDir, "w") as file:
            json.dump(data, file,indent= 4)
        return ""

    def check_user(self, email, password):
        user = ""
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["email"] == email and element["password"] == password:
                element["login"] = "True"
                with open(user_dataDir, 'w') as f:
                    f.write(json.dumps(datastore,indent= 4))
                return ""
        else:
            message = "You have entered an invalid email/password"
        return "You have entered an invalid email/password"

    def logout_user(self):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["login"] == "True":
                element["login"] = "False"
                with open(user_dataDir, 'w') as f:
                    f.write(json.dumps(datastore,indent= 4))
                return "You have successfully logged out"
        return ""

    def check_login(self):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["login"] == "True":
                return True
        return False

    def get_product(self, productName):
        products = System().show_products()
        for product in products["products"]:
            if productName == product["_name"]:
                return product

    def get_ebay_product(self, productName):
        products = System().show_ebay_products()
        for product in products["products"]:
            if productName in product["_name"]:
                return product

    def get_ongoing_requests(self, requestResult):
        ongoing = []
        for requests in requestResult:
            if requests["_status"] != "Accepted" and requests["_status"] != "Completed":
                ongoing.append(requests)
        return ongoing

    def get_requests_name(self, productName):
        requestResult = []
        requests = System().show_requests()
        for request in requests["request"]:
            if productName == request["_name"]:
                requestResult.append(request)
        return requestResult
    def get_request_by_name(self, productName, customer, traveller):
        requests = System().show_requests()
        for request in requests["request"]:
            if productName == request["_name"] and customer == request["_customer"] and traveller == request["_traveller"]:
                return request
        return None

    def get_requests_customer(self, customer):
        requestResult = []
        requests = System().show_requests()
        for request in requests["request"]:
            if customer == request["_customer"]:
                requestResult.append(request)
        return requestResult

    def get_offers(self, traveller):
        offerResult = []
        requests = System().show_requests()
        for request in requests["request"]:
            if traveller == request["_traveller"]:
                offerResult.append(request)
        return offerResult

    def get_pending_requests(self, customer):
        requests = System().get_requests_customer(customer)
        result = []
        for request in requests:
            if request["_status"] == "Pending":
                result.append(request)
        return result

    def get_accepted_requests(self, customer):
        requests = System().get_requests_customer(customer)
        result = []
        for request in requests:
            if request["_status"] == "Accepted":
                result.append(request)
        return result

    def get_pending_offers(self, traveller):
        offers = System().get_offers(traveller)
        result = []
        for offer in offers:
            if offer["_status"] == "Pending":
                result.append(offer)
        return result

    def get_accepted_offers(self, traveller):
        offers = System().get_offers(traveller)
        result = []
        for offer in offers:
            if offer["_status"] == "Accepted":
                result.append(offer)
        return result

    def get_search(self, text):
        matchResults = []
        with open(productsDir) as f:
            productdata = json.load(f)
        for product in productdata["products"]:
            if text in product["_name"] or text in product["_name"].upper() or text in product["_name"].lower():
                matchResults.append(product)
            elif text in product["_country"] or text in product["_country"].upper() or text in product["_country"].lower():
                matchResults.append(product)
        return matchResults

    def get_category(self, cat):
        matchResults = []
        with open(resultsDir, 'r') as f:
            results = json.load(f)
        if results == []:
            with open(productsDir, 'r') as f:
                data = json.load(f)
                for product in data["products"]:
                    if product["_category"] == cat:
                        matchResults.append(product)
                    if product["_country"] == cat:
                        matchResults.append(product)
        else:
            for product in results:
                if product["_category"] == cat:
                    matchResults.append(product)
                if product["_country"] == cat:
                    matchResults.append(product)
        return matchResults


    def sort_products_by_price(self,select):
        matchResult = []
        with open(resultsDir, 'r') as f:
            data = json.load(f)
        sorted_obj = data
        if select == "Price Low to High":
            sorted_obj = sorted(data, key=lambda x :x['_audPrice'], reverse=False)
        elif select == "Price High to Low":
            sorted_obj = sorted(data, key=lambda x :x['_audPrice'], reverse=True)
        with open(resultsDir, "w") as file:
            json.dump(data, file, indent=4)

        for product in sorted_obj:
            matchResult.append(product)
        return matchResult

    def sort_ebayproducts_by_price(self,select):
        matchResult = []
        with open(ebayresultsDir, 'r') as f:
            data = json.load(f)
        sorted_obj = dict(data)
        if select == "Price Low to High":
            sorted_obj["products"]= sorted(data["products"], key=lambda x :x['_audPrice'], reverse=False)
        elif select == "Price High to Low":
            sorted_obj["products"]= sorted(data["products"], key=lambda  x :x['_audPrice'], reverse=True)
        with open(ebayresultsDir, "w") as file:
            json.dump(sorted_obj, file, indent=4)

    def get_ebay_search(self,text):
       ebayResults = []
       with open(ebayresultsDir, 'r') as f:
            results = json.load(f)
       if results["products"] == []:
            with open(ebayDir, 'r') as f:
                 data = json.load(f)
            for product in data["products"]:
                if product["_category"] == text:
                        ebayResults.append(product)
                if product["_country"] == text:
                        ebayResults.append(product)
       else:
            for product in results["products"]:
                if product["_category"] == text:
                    ebayResults.append(product)
                if product["_country"] == text:
                    ebayResults.append(product)
       return ebayResults

    def add_product (self, name, link, country, category, audPrice, quantity, customer, image):
        if name == "japanese tea":
            image = "../static/img/OchaskiTea.jpg"
        otherCurrency = Rates.get_countries(country)
        otherPrice = Rates.get_currencies(otherCurrency, audPrice)
        product = Products(name, link, country, category, audPrice, quantity, otherPrice, otherCurrency, customer, image)
        product_dict = product.__dict__
        with open(productsDir) as product_database:
            product_data = json.load(product_database)
        product_data["products"].append(product_dict)
        with open(productsDir, "w") as file:
            json.dump(product_data, file, indent=4)

    def add_ebay_product (self, name, link, country, category, audPrice, quantity, customer, image):
        otherCurrency = Rates.get_countries(country)
        otherPrice = Rates.get_currencies(otherCurrency, audPrice)
        product = Products(name, link, country, category, audPrice, quantity, otherPrice, otherCurrency, customer, image)
        product_dict = product.__dict__
        with open(ebayDir) as product_database:
            product_data = json.load(product_database)
        product_data["products"].append(product_dict)
        with open(ebayDir, "w") as file:
            json.dump(product_data, file, indent=4)

    def dump_ebay_product (self, name, link, country, category, audPrice, quantity, customer, image):
        otherCurrency = Rates.get_countries(country)
        otherPrice = Rates.get_currencies(otherCurrency, audPrice)
        product = Products(name, link, country, category, audPrice, quantity, otherPrice, otherCurrency, customer, image)
        product_dict = product.__dict__
        with open(ebayresultsDir,"r") as f:
            datastore = json.load(f)
        datastore["products"].append(product_dict)
        with open(ebayresultsDir, "w") as file:
            json.dump(datastore, file, indent=4)

    def delete_ebay_results(self):
        with open(ebayresultsDir, 'r') as f:
            datastore = json.load(f)
        datastore["products"]=[]
        with open(ebayresultsDir, "w") as file:
            json.dump(datastore, file, indent=4)

    def add_request (self, name, customer, audPrice, quantity, country, status, traveller):
        totalAudPrice = round(audPrice * quantity)
        otherCurrency = Rates.get_countries(country)
        otherPrice = Rates.get_currencies(otherCurrency, audPrice)
        totalOtherPrice = round(otherPrice * quantity)
        request = Requests(name, customer, quantity, totalAudPrice, totalOtherPrice, otherCurrency, status, traveller, country)
        request_dict = request.__dict__
        with open(product_requestsDir) as request_database:
            request_data = json.load(request_database)
        request_data["request"].append(request_dict)
        with open(product_requestsDir, "w") as file:
            json.dump(request_data, file, indent=4)

    def show_products(self):
        with open(productsDir, "r") as products_database:
            products = json.load(products_database)
        return products

    def show_ebay_products(self):
        with open(ebayDir, "r") as products_database:
            products = json.load(products_database)
        return products

    def show_requests(self):
        with open(product_requestsDir, "r") as requests_database:
            requests = json.load(requests_database)
        return requests

    def show_users(self):
        with open(user_dataDir, "r") as user_database:
            user = json.load(user_database)
        return user["user"]

    def find_requests_btwn_users(self, user1, user2):
        requests = self.show_requests()
        btwnUsers = []
        for elements in requests["request"]:
            if elements["_customer"] == user1 and elements["_traveller"] == user2:
                btwnUsers.append(elements)
            if elements["_customer"] == user2 and elements["_traveller"] == user1:
                btwnUsers.append(elements)
        return btwnUsers

    def show_trending():
        requests = System().show_requests()
        trending = []
        products = System().show_products()
        trending_products = []
        for r in requests["request"]:
            trending.append(r["_name"])
        trending_names = Counter(trending)
        trending_names = trending_names.most_common(3)
        for t,v in trending_names:
            for p in products["products"]:
                if t == p["_name"]:
                    trending_products.append(p)
                    break
        return trending_products


    def check_add_product(self, name, country, category, audPrice):
        Message = "Invalid input, enter fields again"
        if audPrice is "" or name is "" or country is "" or category is "":
            return Message
        try:
            int(audPrice)
        except:
            return Message
        try:
            name is not None
        except:
            return Message
        try:
            str(country)
        except:
            return Message
        try:
            str(category)
        except:
            return Message

        return None

    def show_message_thread(self, username, currentUser):
        with open(messagesDir, "r") as f:
            messagesData = json.load(f)
        messageList = []
        for message in messagesData["allMessages"]:
            if message["sender"] == username and message["receiver"] == currentUser:
                messageList.append(message)
            if message["sender"] == currentUser and message["receiver"] == username:
                messageList.append(message)
        messageList = messageList[::-1]
        return messageList

    def show_chats(self, currentUser):
        with open(messagesDir, "r") as f:
            messagesData = json.load(f)
        chatList = []
        for message in messagesData["allMessages"]:
            if message["sender"] == currentUser:
                chatList.append(message["receiver"])
            if message["receiver"] == currentUser:
                chatList.append(message["sender"])
        chatList = list(dict.fromkeys(chatList))
        return chatList

    def add_message(self, message, sender, receiver, automated):
    # the message should be in the receiver's inbox
        now = datetime.datetime.now()
        time = now.strftime("%a %d/%m/%Y %I:%M%p")
        message = Message(sender, receiver, message,automated,time)
        message_dict = message.__dict__
        with open(messagesDir) as f:
            messagesData = json.load(f)
        messagesData["allMessages"].append(message_dict)
        with open(messagesDir, "w") as file:
            json.dump(messagesData, file, indent=4)

    def add_trip(self, user, country, date):
        trip = {}
        trip["country"] = country
        trip["date"] = date
        with open(user_dataDir) as user_database:
            user_data = json.load(user_database)
        for element in user_data["user"]:
            if element["username"] == user:
                if "trip" in element:
                    element["trip"].append(trip)
                else:
                    element["trip"] = []
                    element["trip"].append(trip)
        with open(user_dataDir, "w") as file:
            json.dump(user_data, file, indent=4)

    def delete_trip(self, user, country, date):
        with open(user_dataDir) as user_database:
            user_data = json.load(user_database)
        for element in user_data["user"]:
            if element["username"] == user:
                for trip in element["trip"]:
                    if country in trip.get("country") and date in trip.get("date"):
                        element["trip"].remove(trip)
                        break
        with open(user_dataDir, "w") as file:
            json.dump(user_data, file, indent=4)

    def update_request(self, productName, receiver, traveller,status):
        update_request = {}
        with open(product_requestsDir) as request_database:
            request_database = json.load(request_database)
        for requests in request_database["request"]:
            if productName == requests["_name"] and receiver == requests["_customer"]:
                update_request["_traveller"] = traveller
                update_request["_status"] = status
                requests.update(update_request)
        with open(product_requestsDir, "w") as file:
            json.dump(request_database, file, indent=4)

    def delete_request(self, productName, customer):
        with open(product_requestsDir) as request_database:
            request_database = json.load(request_database)
        for r in request_database["request"]:
            if productName == r["_name"] and customer == r["_customer"]:
                request_database["request"].remove(r)
                break
        with open(product_requestsDir, "w") as file:
            json.dump(request_database, file, indent=4)

    def delete_offer(self, productName, customer, traveller):
        with open(product_requestsDir) as request_database:
            request_database = json.load(request_database)
        for r in request_database["request"]:
            if productName == r["_name"] and customer == r["_customer"] and traveller == r["_traveller"]:
                request_database["request"].remove(r)
                break
        with open(product_requestsDir, "w") as file:
            json.dump(request_database, file, indent=4)

    def update_profile(self,info,input,email):
        with open(user_dataDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["user"]:
            if element["email"] == email:
                element[info] = input
                with open(user_dataDir, 'w') as f:
                    f.write(json.dumps(datastore,indent= 4))
                return "edited"
        return ""

    def get_offer_traveller(self, customer):
        requestResult = []
        requests = System().show_requests()
        for request in requests["request"]:
            if customer == request["_traveller"]:
                requestResult.append(request)
        return requestResult

    def remove_request(self, product):
        with open(product_requestsDir) as database:
            database = json.load(database)
        for i in range(len(database["request"])):
            if database["request"][i] == product:
                database["request"].pop(i)
        with open(product_requestsDir,"w") as f:
            json.dump(database, f, indent=4)

    def add_review_rating(self, user, reviewer, comment, rating):
        review = {}
        review["reviewer"] = reviewer
        review["comment"] = comment
        review["rating"] = rating
        with open(user_dataDir) as f:
            data = json.load(f)
        for users in data["user"]:
            if user == users["username"]:
                if "review" in users:
                    users["review"].append(review)
                else:
                    users["review"] = []
                    users["review"].append(review)
                numReviews = len(users["review"])
                count = 0
                for u in users["review"]:
                    count = count + int(u["rating"])
                users["aveRating"] = (count/numReviews)*2
                users["aveRating"] = str((round(users["aveRating"]))/2)
        with open(user_dataDir,"w") as f:
            json.dump(data, f, indent=4)

    def check_user_review(self, user, reviewer):
        requests = System().show_requests()
        for r in requests["request"]:
            if (r["_customer"] == user and r["_traveller"] == reviewer) or (r["_customer"] == reviewer and r["_traveller"] == user):
                return 1
        return 0

    def check_username_unique(self, username):
        users = System().show_users()
        for u in users:
            if username == u["username"]:
                return 1
        return 0

    def check_email_unique(self, email):
        users = System().show_users()
        for u in users:
            if email == u["email"]:
                return 1
        return 0

    def is_existing_product(self,productName, customer):
        with open(productsDir) as f:
            data = json.load(f)
        for products in data["products"]:
            if productName == products["_name"] and customer == products["_customer"]:
                return True
        return False
