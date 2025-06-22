# server/routes.py

from flask import Blueprint, request, jsonify, abort
from models import db, Plant   # adjust if your import path is different

plants_bp = Blueprint('plants', __name__, url_prefix='/plants')

@plants_bp.route('/<int:id>', methods=['PATCH'])
def update_plant(id):
    data = request.get_json()
    if not data:
        return jsonify({ "error": "Invalid JSON body" }), 400

    plant = Plant.query.get(id)
    if not plant:
        abort(404, description=f"Plant with id={id} not found")

    # Update only the fields provided
    for field in ('name', 'image', 'price', 'is_in_stock'):
        if field in data:
            setattr(plant, field, data[field])

    db.session.commit()
    return jsonify(plant.to_dict()), 200


@plants_bp.route('/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description=f"Plant with id={id} not found")

    db.session.delete(plant)
    db.session.commit()
    return '', 204
