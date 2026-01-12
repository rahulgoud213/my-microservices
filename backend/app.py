from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# 1. Pull environment variables from K8s Deployment
db_host = os.getenv('DB_HOST', 'localhost') 
db_user = os.getenv('DB_USER', 'postgres')
db_pass = os.getenv('DB_PASS', 'mypassword')
db_name = os.getenv('DB_NAME', 'postgres') # Note: default postgres db is usually 'postgres'

# 2. Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Define the Data Model
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, server_default=db.func.now())
    user_agent = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
# 4. Create tables automatically
with app.app_context():
    db.create_all()

@app.route('/api/data')
def get_data():
    # Record the visit in the database
    try:
        new_visitor = Visitor(user_agent=request.headers.get('User-Agent'))
        db.session.add(new_visitor)
        db.session.commit()
        return jsonify({"message": "Hello from the Backend! Visit recorded."})
    except Exception as e:
        return jsonify({"message": "Backend is up, but DB connection failed.", "error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # 1. Query all users from the database, newest first
        users = User.query.order_by(User.created_at.desc()).all()
        
        # 2. Convert the database objects into a simple list of dictionaries
        user_list = [
            {
                "id": u.id, 
                "firstName": u.first_name, 
                "lastName": u.last_name,
                "date": u.created_at.strftime("%Y-%m-%d %H:%M")
            } for u in users
        ]
        
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    # Validation: Ensure we have the data we need
    if not data or not data.get('firstName') or not data.get('lastName'):
        return jsonify({"error": "Missing first name or last name"}), 400

    try:
        # Create a new User object
        new_user = User(
            first_name=data.get('firstName'),
            last_name=data.get('lastName')
        )
        # Save to PostgreSQL
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": f"Welcome, {new_user.first_name}!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# 5. Start the server (Must be at the very bottom!)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)