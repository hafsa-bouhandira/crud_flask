from flask import Flask , Response , request
from flask_cors import CORS, cross_origin
import pymongo
import json
from bson.objectid import ObjectId
from flask import jsonify

app = Flask(__name__)
CORS(app)

try: 
    mongo = pymongo.MongoClient(host ="localhost", port = 27017 , serverSelectionTimeoutMS = 1000)
    db = mongo.company
    mongo.server_info()
except: 

    print("ERROR - Cannot connect to db")
####################################

@app.route("/users" , methods = ["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data :
            user["_id"] = str(user["_id"])
            # response = json.dumps(data)
            # response.headers.add('Access-Control-Allow-Origin', '*')
        return Response( response = json.dumps(data) ,status = 200 , mimetype = "application/json")
        
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"cannot read users"}), status = 500 , mimetype = "application/json")


#####################################
@app.route("/users" , methods = ["POST"])

def  create_user():
    try :
        user = {"name": request.form.get('name'),"lastName":request.form.get('lastName'),"age": request.form.get('age') }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        
        return Response(response = json.dumps({"message":"user created", "id": f"{dbResponse.inserted_id}"}),status = 200 , mimetype = "application/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"cannot add user"}), status = 500 , mimetype = "application/json")
#####################################
# Update 
@app.route("/users/<id>", methods = ["PATCH"])
def update_users(id):
    try: 
     
        dbResponse  = db.users.update_one({"_id": ObjectId(id)},{"$set":{"name": request.form["name"]}})
      
        if dbResponse.modified_count == 1: 
            
            return Response(response = json.dumps({"message":" updated user "}), status = 200 , mimetype = "application/json")
        else:
            print(dbResponse.modified_count)
            return Response(response = json.dumps({"message":"  Nothing to update"}), status = 200 , mimetype = "application/json")
    except Exception as ex:
        return Response(response = json.dumps({"message":"cannot update user"}), status = 500 , mimetype = "application/json")

#####################################
@app.route("/users/<id>", methods = ["DELETE"])

def delete_users(id):
    try: 
         
        dbResponse  = db.users.delete_one({"_id": ObjectId(id)})
       
        if dbResponse.deleted_count == 1: 
            return Response(response = json.dumps({"message":" deleted user ",  "id": f"{id}"}), status = 200 , mimetype = "application/json")
        else:
            return Response(response = json.dumps({"message":"  user does not exist" ,"id": f"{id}"}), status = 200 , mimetype = "application/json")
    except Exception as ex:
        return Response(response = json.dumps({"message":"cannot delete user"}), status = 500 , mimetype = "application/json")








#####################################
# @app.route('/')
# def get_users():
#     print ("hello world")

#     try:
#         data = list(db.users.find())
#         for user in data :
#             user["_id"] = str(user["_id"])
#         # response = json.dumps(data), status = 500 , mimetype = "application/json"
#         # print(response)
#         return Response(response = json.dumps(data),status = 200 , mimetype = "application/json")
#     except Exception as ex:
#         print(ex)
#         return Response(response = json.dumps({"message":"cannot read users"}), status = 500 , mimetype = "application/json")
# ######################################
if __name__ == "__main__":
    app.run(port= 80 , debug = True )