from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

# Initialize FastAPI app
app = FastAPI()

# Database connection details
db_config = {
    "host": "127.0.0.1",  # Replace with your database host
    "user": "root",        # Replace with your database username
    "password": "",        # Replace with your database password
    "database": "payments_db"  # Replace with your database name
}

# Pydantic model for request body
class PaymentRequest(BaseModel):
    user_id: str

@app.post("/mark_payment_as_completed")
async def mark_payment_as_completed(payment_request: PaymentRequest):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Extract user_id from the request
        user_id = payment_request.user_id

        # Update the payment status in the database
        sql = "UPDATE payments SET status = 'completed' WHERE user_id = %s AND status = 'pending'"
        cursor.execute(sql, (user_id,))
        conn.commit()

        # Check if any rows were updated
        if cursor.rowcount > 0:
            return {"success": True, "message": "Payment status updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="No pending payment found for the given user_id")

    except Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating payment status: {e}")

    finally:
        # Close the database connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()