from flask import Flask, render_template
from flask_pymongo import PyMongo
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB Atlas cluster (points to your cluster, database specified in code)
app.config["MONGO_URI"] = (
    "mongodb+srv://aryan_peter:build-a-thon-2025@h2optimize.lojidbx.mongodb.net/H2Optimize?retryWrites=true&w=majority"
)
mongo = PyMongo(app)

@app.route('/')
def home():
    # Reference the correct database and collection
    db = mongo.db
    collection = db.weeklyWaterUsage

    # Define time window: past 7 days
    today = datetime.utcnow()
    week_ago = today - timedelta(days=7)

    # MongoDB aggregation pipeline
    pipeline = [
        # Match only data from the last 7 days
        {"$match": {"timestamp": {"$gte": week_ago, "$lte": today}}},
        
        # Group by user and day, summing liters
        {"$group": {
            "_id": {
                "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                "user": "$user_id"
            },
            "total_liters": {"$sum": "$liters"}
        }},
        
        # Sort chronologically
        {"$sort": {"_id.date": 1}}
    ]

    # Run the aggregation
    results = list(collection.aggregate(pipeline))

    # Organize data for frontend
    usage = {}
    for r in results:
        date = r["_id"]["date"]
        liters = r["total_liters"]
    weekly_totals = {user: sum(day[1] for day in days) for user, days in usage.items()}

    # Pass data to template
    return render_template('index.html', usage=usage, weekly_totals=weekly_totals)

if __name__ == '__main__':
    app.run(debug=True)
