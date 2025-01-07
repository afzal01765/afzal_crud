from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Define the path to the uploads folder
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample book data
books_data = [
    {"id": 0, "title": "book1", "author": "author1"},
    {"id": 2, "title": "book2", "author": "author2"},
    {"id": 1, "title": "book0", "author": "author0"}
]


# Route to fetch all books
@app.route("/books")
def books():
    return jsonify(books_data)


# Route to fetch a specific book by its ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_by_id(book_id):
    for book in books_data:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify({"Error": "This book is not found"})


# Route to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = {"id": len(books_data) + 1, "title": request.json["title"], "author": request.json["author"]}
    books_data.append(new_book)
    return jsonify(new_book)


# Route to update an existing book
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    for book in books_data:
        if book["id"] == book_id:
            book["title"] = request.json["title"]
            book["author"] = request.json["author"]
            return jsonify(book)
    return jsonify({"Error": "This book is not found"})


# Route to delete a book by its ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    for book in books_data:
        if book["id"] == book_id:
            books_data.remove(book)
            return jsonify({"Message": "This book deleted successfully"})
    return jsonify({"Error": "This book is not found"})


# Helper function to check for allowed file types
def allowed_file(filename):
    ALLOWED_EXTS = ['png', 'jpg', 'jpeg']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS


# Route to upload a book file
@app.route("/upload_book", methods=["POST"])
def upload_book():
    upload_file = request.files.get('file')
    if upload_file and allowed_file(upload_file.filename):
        # Ensure the uploads directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        destination = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
        upload_file.save(destination)
        return jsonify({"Message": "File uploaded successfully"})
    else:
        return jsonify({"Error": "Invalid file type or no file provided"})


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
