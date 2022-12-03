from flask import Flask, jsonify
import os
from sqlalchemy import create_engine

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank'

url = "mysql://root:@localhost/bank"


@app.route('/')
def index():
    engine = create_engine(url, echo=TRUE)
    connection = engine.connect()
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
