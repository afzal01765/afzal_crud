from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for items (usually you would use a database)
items = {}

@app.route('/items', methods=['GET'])
def get_items():
    """Retrieve all items"""
    return jsonify(items), 200

@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve a single item"""
    item = items.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item), 200

@app.route('/item', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()
    item_id = data.get('id')
    if not item_id or item_id in items:
        return jsonify({'error': 'Invalid or duplicate item ID'}), 400
    items[item_id] = data
    return jsonify({'message': 'Item created'}), 201

@app.route('/item/<item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    item = items.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json()
    items[item_id] = data
    return jsonify({'message': 'Item updated'}), 200

@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an existing item"""
    item = items.pop(item_id, None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
