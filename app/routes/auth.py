from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.user import User
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app import db

auth_bp = Blueprint('auth', __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()

# register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = register_schema.load(request.get_json(silent=True, force=True) or {})
    except ValidationError as e:
        return jsonify({"status": "error", "message": e.messages}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"status": "error", "message": "email already in use"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"status": "error", "message": "username already taken"}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    user.save()

    return jsonify({"status": "success", "message": "account created", "data": user.to_dict()}), 201


# login and get a token back
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.get_json(silent=True, force=True) or {})
    except ValidationError as e:
        return jsonify({"status": "error", "message": e.messages}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"status": "error", "message": "wrong email or password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "status": "success",
        "data": {
            "token": token,
            "user": user.to_dict()
        }
    }), 200


# get the currently logged in user
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "user not found"}), 404
    return jsonify({"status": "success", "data": user.to_dict()}), 200