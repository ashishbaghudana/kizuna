from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from .model import User, Contact, ContactPhoneNumber
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


@bp.route('/users/<uuid:user_id>/contacts', methods=['GET'])
def get_contacts(user_id):
    """Endpoint to get all contacts for a specific user."""
    user = User.query.get_or_404(user_id)

    contacts_list = []

    # Loop through the contact objects associated with the user
    for contact in user.contacts:
        contact_data = {
            'id': contact.id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'created_at': contact.created_at.isoformat()
        }
        contacts_list.append(contact_data)

    return jsonify(contacts_list)

@bp.route('/contacts/<uuid:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Endpoint to get a single contact's details."""
    contact = Contact.query.get_or_404(contact_id)

    # Convert the main contact object to a dictionary
    contact_data = {
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'created_at': contact.created_at.isoformat(),
        'phone_numbers': [],
        'emails': [],
        'addresses': []
    }

    # (This part can be added later once you create these models)
    # for phone in contact.phone_numbers:
    #     contact_data['phone_numbers'].append({
    #         'id': phone.id,
    #         'phone_number': phone.phone_number,
    #         'label': phone.label,
    #         'is_primary': phone.is_primary
    #     })

    # (Add similar loops for emails and addresses here)

    return jsonify(contact_data)

@bp.route('/contacts/<uuid:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Endpoint to update an existing contact."""
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body cannot be empty"}), 400

    # Update fields with new data if provided
    contact.first_name = data.get('first_name', contact.first_name)
    contact.last_name = data.get('last_name', contact.last_name)

    db.session.commit()

    return jsonify({"message": "Contact updated successfully"})

@bp.route('/contacts/<uuid:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Endpoint to delete a contact."""
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted successfully"})