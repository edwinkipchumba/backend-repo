import re
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS,cross_origin



app = Flask(__name__)
CORS(app)



def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("blogs.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn



@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM blog")
        blogs = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3], description=row[4])
            for row in cursor.fetchall()
        ]
        if blogs is not None:
            return jsonify(blogs)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        new_desc = request.form['description']
        sql = """INSERT INTO blog (author, language, title,description) VALUES (?,?,?,?)"""

        cursor = cursor.execute(sql, (new_author,new_lang,new_title,new_desc))
        conn.commit()
        return f"Blog with the id: {cursor.lastrowid} created successfully"

@app.route('/blog/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_blog(id):
    conn = db_connection()
    cursor = conn.cursor()
    blog = None
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM blog WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            blog = r
        if blog is not None:
            return jsonify(blog), 200
        else:
            return "Something Wrong!", 404


    if request.method == 'PUT':
        sql="""UPDATE blog SET title=?, author=?, language=?, description=? WHERE id=?"""
        title = request.form["title"]
        description =request.form["description"]
        author = request.form["author"]
        language = request.form["language"]
        updated_blog = {
            "id": id,
            "author": author,
            "language": language,
            "title": title,
            "description": description
        }
        conn.execute(sql, (author, language, title, description, id))
        conn.commit()
        return jsonify(updated_blog)

    if request.method == 'DELETE':
        sql = """DELETE FROM blog WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return "The blog with id: {} has been deleted.".format(id), 200
        


if __name__ == '__main__':
        app.run(debug=True)

