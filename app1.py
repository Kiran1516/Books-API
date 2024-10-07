from flask import Flask, request, jsonify

app = Flask(__name__)

# Initial list of books
books_list = [
    {"id": 0, "author": "Chinua Achebe", "language": "English", "title": "Things Fall Apart"},
    {"id": 1, "author": "Hans Christian Andersen", "language": "Danish", "title": "Fairy Tales"},
    {"id": 2, "author": "Samuel Beckett", "language": "French, English", "title": "Molly, Malone Dies, The Umbrella, The Trilogy"},
    {"id": 3, "author": "Giovanni Boccaccio", "language": "Italian", "title": "The Decameron"},
    {"id": 4, "author": "Jorge Luis Borges", "language": "Spanish", "title": "Ficciones"},
    {"id": 5, "author": "Emily Brontë", "language": "English", "title": "Wuthering Heights"},
]

# List to store deleted books
deleted_books = []

# Root route
@app.route('/')
def index():
    return "Welcome to the Book API! Use /books to access the books."

# Get all books or add a new book
@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        return jsonify(books_list), 200

    if request.method == 'POST':
        new_author = request.json.get('author')
        new_language = request.json.get('language')
        new_title = request.json.get('title')
        
        if not new_author or not new_language or not new_title:
            return jsonify({'error': 'Missing data. Please provide author, language, and title.'}), 400

        # Generate a new ID (the highest current ID + 1)
        new_id = max(book['id'] for book in books_list) + 1 if books_list else 0

        new_book = {
            'id': new_id,
            'author': new_author,
            'language': new_language,
            'title': new_title
        }
        books_list.append(new_book)
        return jsonify(new_book), 201

# Get, update, or delete a single book by ID
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    book = next((b for b in books_list if b['id'] == id), None)

    if request.method == 'GET':
        if book:
            return jsonify(book), 200
        else:
            return jsonify({'error': 'Book not found'}), 404

    if request.method == 'PUT':
        if book:
            book['author'] = request.json.get('author', book['author'])
            book['language'] = request.json.get('language', book['language'])
            book['title'] = request.json.get('title', book['title'])
            return jsonify(book), 200
        else:
            return jsonify({'error': 'Book not found'}), 404

    if request.method == 'DELETE':
        if book:
            books_list.remove(book)
            deleted_books.append(book)  # Move deleted book to deleted_books list
            return '', 204
        else:
            return jsonify({'error': 'Book not found'}), 404

# Restore a deleted book by ID
@app.route('/restore/<int:id>', methods=['POST'])
def restore_book(id):
    book = next((b for b in deleted_books if b['id'] == id), None)

    if book:
        deleted_books.remove(book)
        books_list.append(book)
        return jsonify(book), 200
    else:
        return jsonify({'error': 'Book not found in deleted books'}), 404

# Get all deleted books (optional)
@app.route('/deleted_books', methods=['GET'])
def get_deleted_books():
    return jsonify(deleted_books), 200

if __name__ == '__main__':
    app.run(debug=True)
