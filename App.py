from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

# API Route to Add an Expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    title = data.get('title')
    amount = data.get('amount')
    category = data.get('category')

    if not title or not amount or not category:
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)', (title, amount, category))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully!"}), 201

# API Route to Fetch All Expenses
@app.route('/get_expense', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, amount, category, date FROM expenses ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()

    # Format data into a list of dictionaries
    expenses = [{"title": row[0], "amount": row[1], "category": row[2], "date": row[3]} for row in rows]
    return jsonify(expenses)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)