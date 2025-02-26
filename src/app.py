"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user/task/username/<int:theid>', methods=['PUT'])
def update_task(theid=None):
    task= request.json
    if task('label') is None:
        return jsonify({"Menssage:wrong property"}), 400 
    if task ('done') is None:
        return jsonify({"Menssage:wrong property"}), 400
    user = User.query.get(theid)
    if user is None:
        return jsonify({"Message:user not found"}), 404
    
    print(update_task)
    return jsonify([], 200)    


@app.route("/user/<int:theid>", methods=["DELETE"])
def delete_user(theid=None):
    user = User.query.get(theid)

    if user is None:
        return jsonify({"message": "User not found"}), 404
    else:
        db.session.delete(user)

        try:
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 204
        except Exception as error:
            db.session.rollback()
            return jsonify({"message": f"error: {error}"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


