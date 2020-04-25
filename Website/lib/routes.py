from lib.server import app
from flask import request, Request, Flask, flash, redirect, render_template, \
     request, url_for, send_from_directory, session
from lib.system import System
from lib.rates import Countries
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from lib.User import User
import json
import os

@app.route('/')
def welcome():
    session['url'] = url_for('mainpage')
    return render_template("welcome.html")

@app.route('/mainpage', methods=['POST', 'GET'])
def mainpage():
    trending = System.show_trending()
    trending_users = System().show_users_trending(trending)
    countries = Countries.get_countries()
    System().delete_my_results()
    System().delete_ebay_results()
    if request.method == "POST":
        if (System().check_login() == False):
            session['url'] = url_for('mainpage')
            remessy = "You were redirected to login"
            return redirect(url_for('login',remess=remessy))
        name = request.form['name']
        link = "test"
        country = request.form['country']
        category = request.form['category']
        audPrice = request.form['audPrice']
        quantity = int(request.form['quantity'])
        image = "../static/img/essence.jpg"
        customer = System().get_username()
        System().add_product(name, link, country, category, int(audPrice), quantity, customer, image)
        System().add_request(name, customer, int(audPrice), quantity, country, "Open", 0)
        return redirect(url_for('mainpage'))
    return render_template('mainpage.html', trending = trending, countries = countries, trending_users = trending_users)

@app.route('/login/<remess>', methods=['GET', 'POST'])
def login(remess):
    message = ""
    email = ""
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        message = System().check_user(email, password)
        if message is "":
            if 'url' in session:
                return redirect(session['url'])
            return redirect(url_for('mainpage', check = check))

        return render_template("login.html", message=message,remessa="Welcome to the login page")
    return render_template("login.html", message=message, remessa=remess)


@app.route('/logout')
def logout():
    CurrentUser = System().get_username()
    message = ""
    message = System().logout_user()
    return redirect(url_for('login',remess="Welcome back to the login page"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = ""
    password = ""
    cities = ["Adelaide", "Brisbane", "Canberra", "Darwin", "Hobart", "Melbourne", "Perth", "Sydney"]
    if request.method == 'POST':
        cities = ["Adelaide", "Brisbane", "Canberra", "Darwin", "Hobart", "Melbourne", "Perth", "Sydney"]
        newemail = request.form["email"]
        newpassword = request.form["password"]
        newusername = request.form["username"]
        newcity = request.form["city"]
        System().add_message("Hi, Welcome to Globeshoppers! Message us if you have any questions or issues", "Globeshoppers", newusername, "Yes")
        if newemail is "" or newpassword is "" or newusername is "" or newcity is "":
            return render_template("signup.html", cities = cities, signupError = 0)
        check = System().check_username_unique(newusername)
        if check == 1:
            return render_template("signup.html", cities = cities, signupError = 1)
        check = System().check_email_unique(newemail)
        if check == 1:
            return render_template("signup.html", cities = cities, signupError = 2)
        System().create_user(newusername,newemail, newpassword, newcity)
        if 'url' in session:
            return redirect(session['url'])
        return redirect(url_for('mainpage'))
    return render_template("signup.html", cities = cities)

@app.route('/categories/<cat>')
def categories(cat): #cat is passed from main page button clicked
    matchResults = System().get_category(cat)
    items = System().get_users_items(matchResults)
    ebayResults = []
    ebayResultsName = []
    ebayResultsPrice = []
    ebayResultsUrl = []
    ebayResultsImage = []
    if (cat == "clear"):
        matchResults = []
        System().delete_my_results()
        System().delete_ebay_results()
        return render_template("searchResults.html",matchResults = matchResults,
    			   ebayResultsName = ebayResultsName, ebayResultsPrice = ebayResultsPrice, ebayResultsUrl = ebayResultsUrl,
    			   ebayResultsImage = ebayResultsImage, text = cat,cat = cat)

    ebayResults = System().get_ebay_search(cat)
    if cat == "Price Low to High" or cat == "Price High to Low":
        matchResults = System().sort_products_by_price(cat)
        items = System().get_users_items(matchResults)
    else :
        System().dump_my_results(matchResults)
        System().delete_ebay_results()
        matchResults = System().get_category(cat)
        items = System().get_users_items(matchResults)
        ebayResults = System().get_ebay_search(cat)
    for item in ebayResults:
        if isinstance(item,dict):
            ebayResultsName.append(item["_name"])
            ebayResultsPrice.append(item["_audPrice"])
            ebayResultsUrl.append(item["_link"])
            ebayResultsImage.append(item["_image"])
        else:
            ebayResultsName.append(item.title.string)
            ebayResultsPrice.append(int(round(float(item.currentprice.string))))
            ebayResultsUrl.append(item.viewitemurl.string.lower())
            ebayResultsImage.append(str(item.galleryurl).lower())
    for i in range(len(ebayResultsName)):
    #     if System().is_existing_product(ebayResultsName[i], "Ebay") == False:
            #System().add_ebay_product(ebayResultsName[i],ebayResultsUrl[i] , "United States",cat,ebayResultsPrice[i], 0, "Ebay", ebayResultsImage[i])
        System().dump_ebay_product(ebayResultsName[i],ebayResultsUrl[i] , "United States",cat,ebayResultsPrice[i], 0, "Ebay", ebayResultsImage[i])
    if cat == "Price Low to High" or cat == "Price High to Low":
        ebayResults = System().sort_ebayproducts_by_price(cat)
        currDir = os.getcwd()
        ebayresultsDir = currDir + "/lib/textfiles/ebayresults.json"
        ebayResultsName = []
        ebayResultsPrice = []
        ebayResultsUrl = []
        ebayResultsImage = []
        with open(ebayresultsDir, 'r') as f:
            datastore = json.load(f)
        for element in datastore["products"]:
            ebayResultsName.append(element["_name"])
            ebayResultsPrice.append(element["_audPrice"])
            ebayResultsUrl.append(element["_link"])
            ebayResultsImage.append(element["_image"])
    return render_template("searchResults.html",matchResults = matchResults,
			   ebayResultsName = ebayResultsName, ebayResultsPrice = ebayResultsPrice, ebayResultsUrl = ebayResultsUrl,
			   ebayResultsImage = ebayResultsImage, text = cat,cat = cat, items = items)


@app.route('/search', methods=['GET', 'POST'])
def search():
    matchResults = []
    ebayResults = []
    ebayResultsName = []
    ebayResultsPrice = []
    ebayResultsUrl = []
    ebayResultsImage = []
    if request.method == "POST":
        text = request.form["search"]
        matchResults = System().get_search(text)
        ebayResults = System().get_ebay_search(text)
        System().dump_my_results(matchResults)
        items = System().get_users_items(matchResults)
        for item in ebayResults:
            ebayResultsName.append(item.title.string)
            ebayResultsPrice.append(int(round(float(item.currentprice.string))))
            ebayResultsUrl.append(item.viewitemurl.string.lower())
            ebayResultsImage.append(item.galleryurl.string.lower())
        for i in range(len(ebayResultsName)):
            if System().is_existing_product(ebayResultsName[i], "Ebay") == False:
                System().dump_ebay_product(ebayResultsName[i],ebayResultsUrl[i] , "United States","Makeup",ebayResultsPrice[i], 0, "Ebay", ebayResultsImage[i])
    return render_template("searchResults.html",matchResults = matchResults,ebayResultsName = ebayResultsName,
			   ebayResultsPrice = ebayResultsPrice, ebayResultsUrl = ebayResultsUrl,
			   ebayResultsImage = ebayResultsImage, text = text, items = items)

@app.route('/inbox', methods=['POST', 'GET'])
def inbox():
    if (System().check_login() == False):
        session['url'] = url_for('inbox')
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    CurrentUser = System().get_username()
    chats = [] #list of people current user have conversations with
    inbox = [] # list of message threads between all users in chats
    allRequests = [] #list of requests between all users in chats
    chats = System().show_chats(CurrentUser)
    index = 0 #displays first persons chat when first opened
    receiver = None
    user_images = System().get_images(chats[index])
    user = System().get_user(CurrentUser)
    for people in chats:
        inbox.append(System().show_message_thread(people, CurrentUser))
        requestsPerPerson = System().find_requests_btwn_users(CurrentUser, people)
        allRequests.append(requestsPerPerson)
    if request.method == 'POST':

        if 'inbox-details' in request.form:
            index = int(request.form["inbox-details"])
            user_images = System().get_images(chats[index])
            return render_template("inbox.html",inbox = inbox, currentUser = CurrentUser, chats = chats, allRequests = allRequests, index = index, user_images = user_images, user = user)

        else:
            person = None
            message = request.form["textarea"]
            for k in range(len(chats)):
                if chats[k] in request.form:
                    receiver = chats[k]
                    System().add_message(message, CurrentUser, receiver, "No")
                    person = k

            for k in range(len(allRequests)):
                if allRequests[k]:
                    for j in range(len(allRequests[k])):
                        if ("Accepted " + str(k) + "," + str(j)) in request.form:
                            System().update_request(allRequests[k][j]["_name"], allRequests[k][j]["_customer"], allRequests[k][j]["_traveller"], "Accepted")
                            message = "This is an automated notification. " + allRequests[k][j]["_customer"] + " has accepted " + allRequests[k][j]["_traveller"]\
                                    + "'s offer to purchase " + allRequests[k][j]["_name"]
                            System().add_message(message,allRequests[k][j]["_customer"], allRequests[k][j]["_traveller"], "Yes")
                            person = k
                        if ("Declined " + str(k) + "," + str(j)) in request.form:
                            if allRequests[k][j]["_status"] != "Accepted":
                                System().update_request(allRequests[k][j]["_name"], allRequests[k][j]["_customer"], 0, "Open")
                            message = "This is an automated notification. " + allRequests[k][j]["_customer"] + " has declined " + allRequests[k][j]["_traveller"]\
                                    + "'s offer to purchase " + allRequests[k][j]["_name"]
                            System().add_message(message,allRequests[k][j]["_customer"], allRequests[k][j]["_traveller"],"Yes")
                            person = k
                        if ("Completed " + str(k) + "," + str(j)) in request.form:
                            System().update_request(allRequests[k][j]["_name"], allRequests[k][j]["_customer"], allRequests[k][j]["_traveller"], "Completed")
                            message = "This is an automated notification. " + allRequests[k][j]["_name"] + " has been completed. Thank you for using Globe Shoppers! Please leave a review on your experience."
                            System().add_message(message,allRequests[k][j]["_customer"], allRequests[k][j]["_traveller"],"Yes")
                            person = k
            user_images = System().get_images(chats[person])

        if (System().check_login() == False):
            session['url'] = url_for('inbox')
            remessy = "You were redirected to login"
            return redirect(url_for('login',remess=remessy))
        CurrentUser = System().get_username()
        chats = [] #list of people current user have conversations with
        inbox = [] # list of message threads between all users in chats
        allRequests = [] #list of requests between all users in chats
        chats = System().show_chats(CurrentUser)
        index = person #displays first persons chat when first opened
        receiver = None
        for people in chats:
            inbox.append(System().show_message_thread(people, CurrentUser))
            requestsPerPerson = System().find_requests_btwn_users(CurrentUser, people)
            allRequests.append(requestsPerPerson)
    return render_template("inbox.html",inbox = inbox, currentUser = CurrentUser, chats = chats, allRequests = allRequests, index = index, user_images = user_images, user = user)

@app.route('/otherProfile/<user>', methods = ['POST', 'GET'])
def otherProfile(user):
    if (System().check_login() == False):
        session['url'] = url_for('otherProfile', user = user)
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    User = System().get_user(user)
    CurrentUser = System().get_username()
    check = System().check_user_review(user, CurrentUser)
    reviews = System().get_users_reviews(User)
    offerResult = System().get_offer_traveller(user)
    offers = System().get_completed(offerResult)
    if user == CurrentUser:
        return redirect(url_for('profile'))
    if request.method == "POST":
        CurrentUser = System().get_username()
        if 'about' in request.form:
            return redirect(url_for('aboutus'))
        if 'how' in request.form:
            return redirect(url_for('howitworks'))
        if 'terms' in request.form:
            return redirect(url_for('termsandconditions'))
        if 'reviewButton' in request.form:
            rating = request.form['rating']
            review = request.form['review']
            System().add_review_rating(user, CurrentUser, review, rating)
            return redirect(url_for('otherProfile', user = user))
        if 'messageButton' in request.form:
            message = request.form["message"]
            System().add_message(message, CurrentUser, user, "No")
            return redirect(url_for('otherProfile', user = user))
    return render_template("otherProfile.html", User = User, check = check, reviews = reviews, offers = offers)

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if (System().check_login() == False):
        session['url'] = url_for('profile')
        remessy = "You were redirected to login"
        return redirect(url_for('login',remess=remessy))
    CurrentUser = System().get_username()
    user = System().get_user(CurrentUser)
    reviews = System().get_users_reviews(user)
    bio = 0
    if "about" in user:
        bio = 1;
    requestResult = System().get_requests_customer(CurrentUser)
    for r in requestResult:
        product = System().get_product(r['_name'])
        r["_image"] = product['_image']
    offerResult = System().get_offer_traveller(CurrentUser)
    for r in offerResult:
        product = System().get_product(r['_name'])
        r["_image"] = product['_image']
    countries = Countries.get_countries()
    travellers = System().get_users_requests(requestResult)
    customers = System().get_users_offers(offerResult)
    if request.method == "POST":
        CurrentUser = System().get_username()
        if 'about' in request.form:
            return redirect(url_for('aboutus'))
        if 'how' in request.form:
            return redirect(url_for('howitworks'))
        if 'terms' in request.form:
            return redirect(url_for('termsandconditions'))
        if 'logout' in request.form:
            session['url'] = url_for('mainpage')
            return redirect(url_for('logout'))
        if 'editButton' in request.form:
            useremail = System().get_user_email()
            msg = ""
            newusername = request.form['name']
            newemail = request.form['email']
            newabout = request.form['bio']
            newpassword = request.form['password']
            newcity = request.form['city']
            if newusername is not "":
                check = System().check_username_unique(newusername)
                if check == 1:
                    return render_template("profile.html", user = user, requestResult = requestResult, offerResult = offerResult, bio = bio, countries = countries, tripError = 2, reviews = reviews, customers = customers, travellers = travellers)
                msg = System().update_profile("username",newusername,useremail)
                System().update_username(CurrentUser, newusername)
            if newabout is not "":
                System().update_profile("about",newabout,useremail)
            if newcity is not "":
                System().update_profile("city",newcity,useremail)
            if newpassword is not "":
                System().update_profile("password",newpassword,useremail)
            if newemail is not "":
                check = System().check_email_unique(newemail)
                if check == 1:
                    return render_template("profile.html", user = user, requestResult = requestResult, offerResult = offerResult, bio = bio, countries = countries, tripError = 3, reviews = reviews, customers = customers, travellers = travellers)
                System().update_profile("email",newemail,useremail)
            return redirect(url_for('profile'))
        if 'tripButton' in request.form:
            country = request.form["country"]
            startdate = request.form["startdate"]
            enddate = request.form["enddate"]
            date = startdate + " to " + enddate
            if country is not "" and startdate is not "" and date is not "":
                System().add_trip(CurrentUser, country, date)
            else:
                return redirect(url_for('profile'))
            return redirect(url_for('profile'))
        for r in requestResult:
            if r['_name'] in request.form:
                if "Accepted" in r['_status']:
                    #need to add a 0 rating/penalty
                    review = "This user deleted their accepted request and a 0 rating was given."
                    message = CurrentUser + " has deleted their request"
                    System().add_message(message, r['_customer'], r['_traveller'], "Yes")
                    System().add_review_rating(CurrentUser, "GlobeShoppers", review, 0)
                System().delete_request(r['_name'], CurrentUser)
                return redirect(url_for('profile'))
        for r in offerResult:
            reference = r['_name'] + "-" + r['_customer']
            if reference in request.form:
                if "Accepted" in r['_status']:
                    #need to add a 0 rating/penalty
                    review = "This user deleted their accepted offer and a 0 rating was given."
                    message = CurrentUser + " has deleted their offer"
                    System().add_message(message, r['_traveller'], r['_customer'], "Yes")
                    System().add_review_rating(CurrentUser, "GlobeShoppers", review, 0)
                System().delete_offer(r['_name'], r['_customer'], CurrentUser)
                return redirect(url_for('profile'))
        for t in user["trip"]:
            reference = t['date'] + "-" + t['country']
            if reference in request.form:
                System().delete_trip(CurrentUser, t['country'], t['date'])
                return redirect(url_for('profile'))
    return render_template("profile.html", user = user, requestResult = requestResult, offerResult = offerResult, bio = bio, countries = countries, reviews = reviews, customers = customers, travellers = travellers)


@app.route('/product/<productName>', methods=['POST', 'GET'])
def product(productName):
    CurrentUser = System().get_username()
    if (System().check_login() == False):
        loggedIn = False
    else:
        loggedIn = True
    offer_help = "yes"
    productResult = System().get_product(productName)
    requestResult = System().get_requests_name(productName)
    requestResult = System().get_ongoing_requests(requestResult)
    requesters = System().show_users_requesters(requestResult)
    if CurrentUser != None:
        if CurrentUser in productResult["_name"]:
            offer_help = "no"
    if request.method == "POST":
        if 'want_button' in request.form:
            if (System().check_login() == False):
                session['url'] = url_for('product', productName = productName)
                remessy = "You were redirected to login"
                return redirect(url_for('login',remess=remessy))
            quantity = int(request.form["quantity"])
            System().add_request(productName, CurrentUser, productResult["_audPrice"], quantity, productResult["_country"], "open", 0)
            return redirect(url_for('product', productName = productName))
        for requests in requestResult:
            if requests["_customer"] in request.form:
                if (System().check_login() == False):
                    session['url'] = url_for('product', productName = productName)
                    remessy = "You were redirected to login"
                    return redirect(url_for('login',remess=remessy))
                receiver = requests["_customer"]
                message = request.form["message"]
                System().update_request(productName, receiver, CurrentUser, "Pending")

                pendingRequest = System().get_request_by_name(productName, receiver, CurrentUser)
                messageAuto = "This is an automated notification. " + pendingRequest["_traveller"] + " has offered to purchase " + receiver \
                                + "'s request for " + pendingRequest["_name"]
                System().add_message(messageAuto,pendingRequest["_traveller"], pendingRequest["_customer"],"Yes")
                        #note: we want automated messages to appear in the same chat box as customer and travellers
                        #but just faded (like when fb notifies you when chat colour changes)
                System().add_message(message, CurrentUser, receiver,"No")
                return redirect(url_for('product', productName = productName))
    return render_template("product.html", product = productResult, offer_help = offer_help, requests = requestResult, loggedIn = loggedIn, requesters = requesters, CurrentUser = CurrentUser)

@app.route('/productEbay/<productName>', methods=['POST', 'GET'])
def productEbay(productName):
    CurrentUser = System().get_username()
    if (System().check_login() == False):
        loggedIn = False
    else:
        loggedIn = True
    offer_help = "yes"
    productResult = System().get_ebay_product(productName)
    requestResult = System().get_requests_name(productName)
    requestResult = System().get_ongoing_requests(requestResult)
    if CurrentUser != None:
        if CurrentUser in productResult["_name"]:
            offer_help = "no"
    if request.method == "POST":
        if (System().check_login() == False):
                session['url'] = url_for('product', productName = productName)
                remessy = "You were redirected to login"
                return redirect(url_for('login',remess=remessy))
        if 'want_button' in request.form:
            if (System().check_login() == False):
                session['url'] = url_for('product', productName = productName)
                remessy = "You were redirected to login"
                return redirect(url_for('login',remess=remessy))
            quantity = int(request.form["quantity"])
            System().add_request(productName, CurrentUser, productResult["_audPrice"], quantity, productResult["_country"], 0, 0)
            return redirect(url_for('product', productName = productName))
        for requests in requestResult:
            if requests["_customer"] in request.form:
                if (System().check_login() == False):
                    session['url'] = url_for('product', productName = productName)
                    remessy = "You were redirected to login"
                    return redirect(url_for('login',remess=remessy))
                receiver = requests["_customer"]
                message = request.form["message"]
                System().update_request(productName, receiver, CurrentUser, "Pending")

                pendingRequest = System().get_request_by_name(productName, receiver, CurrentUser)
                messageAuto = "This is an automated notification. " + pendingRequest["_traveller"] + " has offered to purchase " + receiver  + "'s request for " + pendingRequest["_name"]
                System().add_message(messageAuto,pendingRequest["_traveller"], pendingRequest["_customer"],"Yes")
                        #note: we want automated messages to appear in the same chat box as customer and travellers
                        #but just faded (like when fb notifies you when chat colour changes)
                System().add_message(message, CurrentUser, receiver,"No")
                return redirect(url_for('product', productName = productName))
    return render_template("product.html", product = productResult, offer_help = offer_help, requests = requestResult, loggedIn = loggedIn)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/whatwedo')
def whatwedo():
    return render_template("whatwedo.html")

@app.route('/howitworks')
def howitworks():
    return render_template("howitworks.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/tandc')
def termsandconditions():
    return render_template("tandc.html")

#end
