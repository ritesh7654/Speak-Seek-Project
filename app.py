from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Project is running!"
# 2. Configuration
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE'),
    'port': 4000,
    'ssl_ca': '/etc/ssl/certs/ca-certificates.crt',
    'ssl_verify_cert': True,
    'ssl_verify_identity': True
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- ROUTES ---

@app.route('/report-lost-item', methods=['POST'])
def report_lost_item():
    try:
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')
        file_to_upload = request.files.get('image')
        
        image_url = "No Image"
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            image_url = upload_result['secure_url']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO lost_items (item_name, description, location, contact_info, image_url) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (item_name, description, location, contact, image_url))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Report submitted!", "link": image_url}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit-issue', methods=['POST'])
def submit_issue():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO student_voice (category, severity, title, description, is_anonymous, student_contact) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (data.get('category'), data.get('severity'), data.get('title'), data.get('description'), data.get('is_anonymous', False), data.get('student_contact')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Issue submitted!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE: GET ISSUES (Safe Version) ---
@app.route('/get-issues', methods=['GET'])
def get_issues():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # We removed "ORDER BY date_reported" to prevent crashing
        cursor.execute("SELECT * FROM student_voice") 
        issues = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(issues), 200
    except Exception as e:
        print(f"Error: {e}") # This prints the error to your black window
        return jsonify({"error": str(e)}), 500

# --- ROUTE: GET LOST ITEMS (Restore this!) ---
@app.route('/get-lost-items', methods=['GET'])
def get_lost_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch all items, newest first
        cursor.execute("SELECT * FROM lost_items ORDER BY date_reported DESC")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- MAIN BLOCK (Must be at the very bottom) ---
if __name__ == '__main__':
    print("🚀 Speak & Seek Backend is running...")
    app.run(debug=True)