from flask import Blueprint, Flask, request, render_template, make_response
import simplejson
import pymongo
import xlrd, xlwt


test = Blueprint("test", __name__, 
            static_folder="./static",# TODO: the directory of static files
            static_url_path="/",    # `url` proxy for static files
            template_folder="./templates"   # TODO: the directory of templates
            )

# client = pymongo.MongoClient("mongodb://localhost:27017/")
client_url = "mongodb+srv://citithrive:citithrive@cluster0.jvrdo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(client_url)


import os


@test.route("/", methods=["POST", "GET"])
def index():
    # return r"<h1>Hello, CitiThrive!<h1/>"
    return render_template("hello.html")

@test.route("/admin", methods=["POST", "GET"])
def admin():
    return render_template("admin.html")

@test.route("/admin-update-industry", methods=["POST", "GET"])
def admin_update_industry():
    meta_data = request.values
    state = 1000
    try:
        file = request.files["file"]
        filename = file.filename
        sav_pth = os.path.join("flask_app", "test", "static", "private", "data", "industry", filename)
        file.save(sav_pth)
        ## 
        fh = xlrd.open_workbook(sav_pth, "rb")
        sheet = fh.sheet_by_index(0)
        n_rows, n_cols = sheet.nrows, sheet.ncols
        cache = {}
        for i in range(1, n_rows):
            cache[sheet.cell(i, 0).value] = True 

        db = client["citithrive"]
        collection = db["industry"]
        for name in cache:
            existed = len(list(collection.find({"name":name}))) > 0
            if existed == False:
                collection.insert_one({
                    "name":name,
                    "abled":True,
                    })
            else:
                collection.update_one({"name":name}, {"$set":{"abled":True}})
        state = 1111
 
    except:
        name = meta_data.get("name")
        action = int(meta_data.get("action"))

        db = client["citithrive"]
        collection = db["industry"]
        if action == 1:
            existed = len(list(collection.find({"name":name}))) > 0
            if existed == False:
                collection.insert_one({
                    "name":name,
                    "abled":True,
                    })
                state = 1001
            else:
                collection.update_one({"name":name}, {"$set":{"abled":True}})
                state = 1002
        else:
            state = 999

            collection.update_one({"name":name}, {"$set":{"abled":False}})


    return simplejson.dumps({
        "state": state,
        })


@test.route("/admin-update-enterprise", methods=["POST", "GET"])
def admin_update_enterprise():
    meta_data = request.values
    state = 1000
    try:
        file = request.files["file"]
        filename = file.filename
        sav_pth = os.path.join("flask_app", "test", "static", "private", "data", "enterprise", filename)
        file.save(sav_pth)

        ## get all industries
        db = client["citithrive"]
        collection = db["industry"]
        cache_industry2id = {}
        items = collection.find()
        for item in items:
            cache_industry2id[item["name"]] = item["_id"]
        # print(cache_industry2id)
        ## 
        fh = xlrd.open_workbook(sav_pth, "rb")
        sheet = fh.sheet_by_index(0)
        n_rows, n_cols = sheet.nrows, sheet.ncols
        cache_enterprises = {}
        for i in range(1, n_rows):
            industry_name = sheet.cell(i, 0).value
            stockcode = sheet.cell(i, 1).value
            enterprise_name = sheet.cell(i, 2).value
            if industry_name in cache_industry2id:
                industry_id = cache_industry2id[industry_name]
            else:
                # add industry
                collection.insert_one({
                    "name":industry_name,
                    "abled":True,
                    })
                industry_id = collection.find({"name":industry_name})[0]["_id"]

            if enterprise_name in cache_enterprises:
                cache_enterprises[enterprise_name]["industries"].append(industry_id)
            else:
                cache_enterprises[enterprise_name] = {
                    "industries":[industry_id],
                    "name":enterprise_name,
                    "other_names":[],
                    "stockcode":stockcode
                }
            # break

        collection = db["enterprise"]
        for enterprise in cache_enterprises:
            existed = len(list(collection.find({"name":enterprise}))) > 0
            if existed == False:
                collection.insert_one(cache_enterprises[enterprise])
            else:
                collection.update_one({"name":name}, {"$set":cache_enterprises[enterprise]}) 
                # pass
        state = 1111
 
    except:
        pass

    return simplejson.dumps({
        "state": state,
        })


@test.route("/admin-add-ESGmetric", methods=["POST"])
def admin_add_ESGmetric():
    meta_data = request.values
    state = 1000
    name = meta_data.get("name_to_edit_ESGmetric")
    description = meta_data.get("description_to_edit_ESGmetric")
    application = meta_data.get("application_to_edit_ESGmetric")
    second_scope = meta_data.get("2nd_scope_to_edit_ESGmetric")
    first_scope = meta_data.get("1st_scope_to_edit_ESGmetric")
    platform = meta_data.get("platform_to_edit_ESGmetric")

    db = client["citithrive"]
    collection = db["ESGmetric"]
    try:
        collection.insert_one({
            "name":name,
            "description":description,
            "application":application,
            "1st_scope":int(first_scope),
            "2nd_scope":second_scope,
            "platform":platform,
            })
    except:
        state = -1000
    return simplejson.dumps({
        "state": state,
        })

