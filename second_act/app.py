from flask import Flask, request, jsonify
import pandas as pd
import os
import logging
import sqlite3
from datetime import datetime
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from collections import deque
import atexit

from detector import detect_anomalies

app = Flask(__name__)

# 2
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False
)

mail = Mail(app)

# 3
logging.basicConfig(level=logging.INFO, filename='email_alerts.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

# 4
recent_transactions = deque(maxlen=60)

# 5
def get_db_connection():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row
    return conn
# 6
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time TEXT,
                        status TEXT,
                        count REAL
                    )''')
    conn.commit()
    conn.close()

create_table()

# 7
def send_alert(subject, body):
    try:
        msg = Message(subject, sender=os.environ.get('MAIL_USERNAME'), recipients=['team_email@example.com'])
        msg.body = body
        msg.html = "<p>" + body.replace('\n', '<br>') + "</p>"
        mail.send(msg)
        logging.info(f"Alert sent successfully: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert: {str(e)}")

# 8
@app.route('/transactions', methods=['POST'])
def receive_transactions():
    try:
        transaction_data = request.json
        if not all(k in transaction_data for k in ('time', 'status')) or not any(k in transaction_data for k in ('f0_', 'count')):
            return jsonify({'error': 'Invalid data format'}), 400

        new_transaction = pd.DataFrame([transaction_data])
        new_transaction['time'] = pd.to_datetime(new_transaction['time'], format='%Hh %M', errors='coerce')
        new_transaction['count'] = new_transaction.get('f0_', new_transaction.get('count'))

        conn = get_db_connection()
        new_transaction[['time', 'status', 'count']].to_sql('transactions', conn, if_exists='append', index=False)
        conn.close()

        recent_transactions.append(new_transaction)
        logging.info(f"Transaction received: {transaction_data}")

        return jsonify({'message': 'Transaction received'}), 200

    except Exception as e:
        logging.error(f"Error receiving transaction: {str(e)}")
        return jsonify({'error': str(e)}), 400

# 9
def check_alerts():
    if recent_transactions:
        recent_df = pd.concat(recent_transactions)
        anomalies = detect_anomalies(recent_df)
        if not anomalies.empty:
            alert_subject = 'Anomaly Detected in Transactions'
            alert_body = f"Anomalies detected at {datetime.now()}:\n\n{anomalies.to_dict()}"
            send_alert(alert_subject, alert_body)
            print(alert_body)

# 10
scheduler = BackgroundScheduler()
scheduler.add_job(check_alerts, 'interval', seconds=60)
scheduler.start()

# 11
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
