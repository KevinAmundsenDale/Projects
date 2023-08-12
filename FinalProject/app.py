from flask import Flask
from views import views

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(views, url_prefix="/views")

if __name__ == '__main__':
    app.run(debug=True, port=8000)

