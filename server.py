from flask import Flask, jsonify, request
from http import HTTPStatus
import uuid 

app = Flask(__name__) # instance of flask 

# http://127.0.1:5000/home
@app.route("/home", methods=["GET"])
def home():
    return {"message": "Welcome to flask cohort 66!"} 


# http://127.0.1:5000/greet-student
@app.route("/greet-student", methods=["GET"])
def say_hi():
    return {"message": "ey hello students!"}


@app.route("/cohort-66" , methods=["GET"])
def get_students_66():
    students_list = ["Ariana", "Jesse", "Robert", "Leo"]
    return students_list


@app.route("/course", methods=["GET"])
def get_course_information():
    course_information = {
        "title": "introductory web API with flask",
        "duration": "4 sessions",
        "level": "beginner"
    }
    return course_information

"""
mini challenge

create a /user endpoint 
-return a dictionary with:
    name, role, is_active and favorite_tecnology
-test on thunder client http://127.0,0,1:5000/user
"""

@app.route("/user", methods=["GET"]) #get is dealt method, we can omit it
def get_user_information():
    user_information = {
        "name": "ariana",
        "role": "student",
        "is_active": True,
        "favorite_technology": ["react"]
    }
    return user_information



#------- products --------
products = [
    {
        "id": "1",
        "title": "laptop",
        "price": 1000,
        "category": "electronics",
        "image": "https://picsum.photos/200/300?random=1"
    },
    {
        "id": "2",
        "title": "headphones",
        "price": 200,
        "category": "electronics",
        "image": "https://picsum.photos/200/300?random=1"
    },
    {
        "id": "3",
        "title": "coffee maker",
        "price": 50,
        "category": "home",
        "image": "https://picsum.photos/200/300?random=1"
    }
    
]

# ----- Path parameters -----
# /greett/<type:name>

@app.route('/greett/<string:name>', methods=["GET"])
def greett(name):
    return f"Hello {name}", HTTPStatus.OK

# GET http://127.0.1:5000/api/products
@app.route('/api/products', methods=["GET"])
def get_products():
    return jsonify({"data": products}), HTTPStatus.OK 

# GET http://127.0.1:5000/api/products/2
@app.route('/api/products/<string:product_id>', methods=["GET"])
def get_product_by_id(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify({
                "success": True,
                "message": "product retrieved successfully",
                "data": product
                }), HTTPStatus.OK
    
    return jsonify({
        "success": False,
        "message": "product not found"
    }), HTTPStatus.NOT_FOUND


# POST http://127.0.0.1:5000/api/products
@app.route('/api/products', methods=["POST"])
def create_product():
    print(f"request information {request.get_json()}")
    new_product = request.get_json()
    new_product["id"] = str(uuid.uuid4())
    products.append(new_product)
    return jsonify({
        "success": True,
        "message": "product successfully added",
        "data": new_product
    }), HTTPStatus.CREATED  #201




#------- coupons --------
coupons = [
    {"_id": 1, "code": "WELCOME10", "discount": 10},
    {"_id": 2, "code": "SPOOKY25", "discount": 25},
    {"_id": 3, "code": "VIP50", "discount": 50}
]

@app.route('/api/coupons', methods=["GET"])
def get_coupons():
    return coupons, HTTPStatus.OK

@app.route('/api/coupons/count', methods=["GET"])
def get_coupons_count():
    count = len(coupons)
    return {"count": count}, HTTPStatus.OK
    

if __name__ == "__main__":
    app.run(debug=True) # run the server in debug mode
    #when this file is run directly: __name__ == "__main__"
    #when this file is imported as a module: __name__ == "server.py"
    
    

