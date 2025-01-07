from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Sample book data
books_data = [
    {"id": 0, "title": "book1", "author": "author1"},
    {"id": 2, "title": "book2", "author": "author2"},
    {"id": 1, "title": "book0", "author": "author0"}
]

# Route to get all books
@app.route("/books", methods=["GET"])
def books():
    return jsonify(books_data)

# Route to get a book by its ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_by_id(book_id):
    for book in books_data:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify({"Error": "This book is not found"}), 404

# Route to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        "id": len(books_data) + 1,
        "title": request.json.get("title"),
        "author": request.json.get("author")
    }
    books_data.append(new_book)
    return jsonify(new_book), 201

# Route to update a book by its ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    for book in books_data:
        if book["id"] == book_id:
            book["title"] = request.json.get("title")
            book["author"] = request.json.get("author")
            return jsonify(book)
    return jsonify({"Error": "This book is not found"}), 404

# Route to delete a book by its ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books_data
    for book in books_data:
        if book["id"] == book_id:
            books_data = [b for b in books_data if b["id"] != book_id]
            return jsonify({"Message": "This book deleted successfully"})
    return jsonify({"Error": "This book is not found"}), 404

# Function to check if file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload a book cover (image file)
@app.route("/upload_book", methods=["POST"])
def upload_book():
    if 'file' not in request.files:
        return jsonify({"Error": "No file part"}), 400
    upload_file = request.files['file']
    
    if upload_file.filename == '':
        return jsonify({"Error": "No selected file"}), 400
    
    if upload_file and allowed_file(upload_file.filename):
        upload_folder = 'uploads/'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        destination = os.path.join(upload_folder, upload_file.filename)
        upload_file.save(destination)
        return jsonify({"Message": "File uploaded successfully"})
    else:
        return jsonify({"Error": "Invalid file format"}), 400

if __name__ == "__main__":
    app.run(debug=True)
