from flask import Blueprint, jsonify, request
from services.hello_service import get_message, get_sorted_hospitals

hello_bp = Blueprint('hello', __name__)

@hello_bp.route('/hello', methods=['GET'])
def hello():
    return get_message()



@hello_bp.route("/get-hospitals", methods=["POST"])
def api_get_hospitals():
    data = request.json
    prompt = data.get("prompt")
    lat = data.get("latitude")
    lon = data.get("longitude")
    print("inside controller ", prompt, float(lat), float(lon))

    result = get_sorted_hospitals(prompt, float(lat), float(lon))
    return jsonify(result)
