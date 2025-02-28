from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password',  # Replace with your MySQL password
    'database': 'payments_db'
}

# Route to update payment status in the database
@app.route('/update_payment/<user_id>', methods=['GET'])
def update_payment(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Update the payment status to 'completed'
        query = "UPDATE payments SET status = 'completed' WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({"status": "success", "message": "Payment updated successfully."})
        else:
            return jsonify({"status": "error", "message": "User ID not found."}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Route to check payment status
@app.route('/check_payment/<user_id>', methods=['GET'])
def check_payment(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check the payment status
        query = "SELECT status FROM payments WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            return jsonify({"status": result[0]})
        else:
            return jsonify({"status": "error", "message": "User ID not found."}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
