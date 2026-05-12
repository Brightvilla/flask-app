from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.products import Product
from app.utils.decorators import role_required

products_bp = Blueprint('products_bp', __name__)


@products_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_product():
    data = request.get_json(silent=True, force=True)
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}), 400

    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock', 0)

    if not name:
        return jsonify({"status": "error", "message": "Product name is required"}), 400
    if price is None or price < 0:
        return jsonify({"status": "error", "message": "Valid price is required"}), 400

    product = Product(name=name, price=price, stock=stock)
    product.save()

    return jsonify({"status": "success", "message": "Product created successfully", "data": product.to_dict()}), 201


@products_bp.route('/', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    min_stock = request.args.get('min_stock', type=int)
    max_stock = request.args.get('max_stock', type=int)

    query = Product.query
    if min_stock is not None:
        query = query.filter(Product.stock >= min_stock)
    if max_stock is not None:
        query = query.filter(Product.stock <= max_stock)

    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "status": "success",
        "data": [p.to_dict() for p in paginated.items],
        "meta": {"page": page, "limit": limit, "total": paginated.total, "pages": paginated.pages}
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    return jsonify({"status": "success", "data": product.to_dict()}), 200


@products_bp.route('/<int:product_id>', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    data = request.get_json(silent=True, force=True)
    if not data:
        return jsonify({"status": "error", "message": "No input data provided"}), 400

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        if data['price'] < 0:
            return jsonify({"status": "error", "message": "Price cannot be negative"}), 400
        product.price = data['price']
    if 'stock' in data:
        if data['stock'] < 0:
            return jsonify({"status": "error", "message": "Stock cannot be negative"}), 400
        product.stock = data['stock']

    db.session.commit()
    return jsonify({"status": "success", "message": "Product updated successfully", "data": product.to_dict()}), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404

    product.delete()
    return jsonify({"status": "success", "message": "Product deleted successfully"}), 200
