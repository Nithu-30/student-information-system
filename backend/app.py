from flask import Flask, jsonify, request
import mysql.connector, os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "sis_user"),
        password=os.getenv("DB_PASSWORD", "changeme"),
        database=os.getenv("DB_NAME", "student_db")
    )

@app.route("/students", methods=["GET"])
def get_students():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students")
    return jsonify(cur.fetchall())

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO students (name, course) VALUES (%s, %s)",
                (data["name"], data["course"]))
    db.commit()
    return jsonify({"message": "Student added"}), 201

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
