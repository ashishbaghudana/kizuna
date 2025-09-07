from flask import Blueprint, jsonify

# Create a Blueprint
bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/hello')
def hello_world():
    return jsonify({"message": "Hello from Kizuna!"})