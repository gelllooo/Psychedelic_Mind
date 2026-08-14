import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ FIX: Use absolute path for uploads folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ AUTO-CREATE uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Data storage
albums = []
posts = []

# 🏠 Home
@app.route("/")
def home():
    return render_template("index.html", posts=posts)

# 📁 View all albums
@app.route("/albums")
def view_albums():
    return render_template("albums.html", albums=albums)

# 📁 View posts inside an album
@app.route("/album/<int:album_id>")
def view_album(album_id):
    album = next((a for a in albums if a["id"] == album_id), None)

    if not album:
        return "Album not found", 404

    album_posts = [p for p in posts if p["album_id"] == album_id]

    return render_template("album_posts.html", posts=album_posts, album=album)

# 📄 View single post
@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        return "Post not found", 404

    return render_template("post.html", post=post)

# ➕ Create album
@app.route("/create_album", methods=["GET", "POST"])
def create_album():
    if request.method == "POST":
        name = request.form["name"]

        new_album = {
            "id": len(albums) + 1,
            "name": name
        }

        albums.append(new_album)
        return redirect(url_for("view_albums"))

    return """
    <h1>Create Album</h1>
    <form method="POST">
        <input name="name" placeholder="Album Name" required>
        <button type="submit">Create</button>
    </form>
    """

# ✍️ Create post (with image + album)
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]

        album_id = request.form.get("album_id")
        if not album_id:
            return "Please select an album", 400

        album_id = int(album_id)

        # 📸 Handle image upload safely
        image = request.files.get("image")
        filename = None

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            # ✅ Save using absolute path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(file_path)

        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "date": date,
            "image": filename,
            "album_id": album_id
        }

        posts.append(new_post)
        return redirect(url_for("home"))

    return render_template("create.html", albums=albums)

# ▶️ Run app
if __name__ == "__main__":
    app.run(debug=True)