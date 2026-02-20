from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def connect():
    return sqlite3.connect("skills.db")

# ---------------- INITIALIZE DATABASE ----------------
def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill TEXT NOT NULL,
            level TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

init_db()

# ---------------- PAGE ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/skills")
def skills_page():
    return render_template("skills.html")

# ---------------- API ROUTES ----------------

# GET ALL SKILLS
@app.route("/api/skills", methods=["GET"])
def get_skills():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM skills")
    data = cur.fetchall()
    con.close()

    skills_list = []
    for row in data:
        skills_list.append({
            "id": row[0],
            "name": row[1],
            "skill": row[2],
            "level": row[3]
        })

    return jsonify(skills_list)


# ADD NEW SKILL
@app.route("/api/skills", methods=["POST"])
def add_skill():
    data = request.json

    if not data.get("name") or not data.get("skill") or not data.get("level"):
        return jsonify({"error": "All fields are required"}), 400

    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO skills(name, skill, level) VALUES(?,?,?)",
        (data["name"], data["skill"], data["level"])
    )
    con.commit()
    con.close()

    return jsonify({"message": "Skill added successfully"})


# UPDATE SKILL
@app.route("/api/skills/<int:id>", methods=["PUT"])
def update_skill(id):
    data = request.json

    con = connect()
    cur = con.cursor()
    cur.execute("""
        UPDATE skills
        SET name=?, skill=?, level=?
        WHERE id=?
    """, (data["name"], data["skill"], data["level"], id))
    con.commit()
    con.close()

    return jsonify({"message": "Skill updated successfully"})


# DELETE SKILL
@app.route("/api/skills/<int:id>", methods=["DELETE"])
def delete_skill(id):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM skills WHERE id=?", (id,))
    con.commit()
    con.close()

    return jsonify({"message": "Skill deleted successfully"})


# SEARCH BY SKILL NAME
@app.route("/api/search/<skill>", methods=["GET"])
def search_skill(skill):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM skills WHERE skill LIKE ?", ('%' + skill + '%',))
    data = cur.fetchall()
    con.close()

    results = []
    for row in data:
        results.append({
            "id": row[0],
            "name": row[1],
            "skill": row[2],
            "level": row[3]
        })

    return jsonify(results)


# TOTAL SKILLS COUNT
@app.route("/api/count", methods=["GET"])
def total_skills():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM skills")
    count = cur.fetchone()[0]
    con.close()

    return jsonify({"total_skills": count})


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
