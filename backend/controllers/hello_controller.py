from flask import Blueprint
from services.hello_service import get_message

hello_bp = Blueprint('hello', __name__)

@hello_bp.route('/hello', methods=['GET'])
def hello():
    return get_message()
