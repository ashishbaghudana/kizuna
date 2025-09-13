from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from .model import User, Contact
from . import db
from .utils import is_valid_uuid
import uuid

# Create a Blueprint
bp = Blueprint('main', __name__, url_prefix='/api')


@bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to create a new user."""
    data = request.get_json()

    if not data or not 'email' in data or not 'password' in data:
        return jsonify({"error": "Missing email or password"}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email address already in use"}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
        email=data['email'],
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

@bp.route('/contacts', methods=['POST'])
def create_contact():
    """Endpoint to create a new contact."""
    data = request.get_json()

    if not data or not 'first_name' in data or not 'user_id' in data:
        return jsonify({"error": "Missing required fields: first_name, user_id"}), 400
    
    if not is_valid_uuid(data['user_id']):
        return jsonify({"error": "Owner user not found"}), 404

    # Check if the owner user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "Owner user not found"}), 404

    new_contact = Contact(
        first_name=data['first_name'],
        last_name=data.get('last_name'), # .get() safely handles optional fields
        owner=user
    )

    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact created successfully", "contact_id": new_contact.id}), 201
