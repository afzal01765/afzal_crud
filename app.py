# CRUD Flask API
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data storage
data = {}
next_id = 1

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(list(data.values()))

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    global next_id
    item = request.json
    item['id'] = next_id
    data[next_id] = item
    next_id += 1
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = data.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    updated_item = request.json
    updated_item['id'] = item_id
    data[item_id] = updated_item
    return jsonify(updated_item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id in data:
        del data[item_id]
        return jsonify({"message": "Item deleted"})
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
