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

# GET http://127.0.1:5000/api/products?price=0&category=all
@app.route('/api/products', methods=["GET"])
def get_products():
    price = request.args.get("price")
    print(f"price: {price}")
    
    category = request.args.get("category")
    print(f"category: {category}")
    
    if not request.args: 
        return jsonify({"data": products}), HTTPStatus.OK 
    else:
        filtered_products = []
        
        for product in products:
            if product["category"].lower() == category.lower() and product["price"] < float(price):
                filtered_products.append(product)
            
        return jsonify({
            "success": True,
            "message": "products retrieved successfully",
            "data": filtered_products
        }), HTTPStatus.OK

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

#PUT http://127.0.0.1:5000/api/products

@app.route('/api/products/<string:product_id>', methods=["PUT"])
def update_product(product_id):
    updated_product = request.get_json()
    print(updated_product)
    for product in products:
        if product["id"] == product_id:
            product["title"] = updated_product.get("title", product["title"])
            product["price"] = updated_product.get("price", product["price"])
            product["category"] = updated_product.get("category", product["category"])
            product["image"] = updated_product.get("image", product["image"])
            return jsonify({
                "success": True,
                "message": "product updated successfully",
                "data": product
            }), HTTPStatus.OK  #200
            
    return jsonify({
        "success": False,
        "message": "product not found"
    }), HTTPStatus.NOT_FOUND #404


#DELETE http://127.0.1:5000/api/products/2
@app.route('/api/products/<string:product_id>', methods=["DELETE"])
def delete_product(product_id):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return jsonify({
                    "success": True,
                    "message": "product deleted successfully",
                    }), HTTPStatus.OK  #200
            # httpStatus.NO_CONTENT we can use it but just when me dont need to return info

    return jsonify({
        "success": False,
        "message": "product not found"
    }), HTTPStatus.NOT_FOUND #404

#------- coupons --------
coupons = [
    {"id": "1", "code": "WELCOME10", "discount": 10},
    {"id": "2", "code": "SPOOKY25", "discount": 25},
    {"id": "3", "code": "VIP50", "discount": 50}
]

@app.route('/api/coupons', methods=["GET"])
def get_coupons():
    return coupons, HTTPStatus.OK

@app.route('/api/coupons/count', methods=["GET"])
def get_coupons_count():
    count = len(coupons)
    return {"count": count}, HTTPStatus.OK
    
    
@app.route('/api/coupons/<string:coupon_id>', methods=["GET"])
def get_coupon_by_id(coupon_id):
    for coupon in coupons:
        if coupon["id"] == coupon_id:
            return jsonify({
                "success": True,
                "message": "coupon retrieved successfully",
                "data": coupon
                }), HTTPStatus.OK

    return jsonify({
        "success": False,
        "message": "coupon not found"
    }), HTTPStatus.NOT_FOUND


@app.route('/api/coupons', methods=["POST"])
def create_coupon():
    print(f"request information {request.get_json()}")
    new_coupon = request.get_json()
    new_coupon["id"] = str(uuid.uuid4())
    coupons.append(new_coupon)
    return jsonify({
        "success": True,
        "message": "coupon successfully added",
        "data": new_coupon
    }), HTTPStatus.CREATED  #201


if __name__ == "__main__":
    app.run(debug=True) # run the server in debug mode
    #when this file is run directly: __name__ == "__main__"
    #when this file is imported as a module: __name__ == "server.py"