from flask import Flask
from controllers.hello_controller import hello_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register controller (blueprint)
app.register_blueprint(hello_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
