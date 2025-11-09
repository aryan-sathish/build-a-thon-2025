from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://aryan_peter:build-a-thon-2025@h2optimize.lojidbx.mongodb.net/?appName=H2Optimize" 
mongo = PyMongo(app)

@app.route('/')  # Added @ symbol
def home():
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)