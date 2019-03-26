# project/api/v1/vehicles.py

from flask import Blueprint, request
from sqlalchemy import exc, or_
from flask_accept import accept

from project.models.user import UserRole
from project.models.vehicle import Vehicle
from project import db
from project.api.common.utils.decorators import authenticate, privileges
from project.api.common.utils.exceptions import NotFoundException, BusinessException, InvalidPayload


vehicles_blueprint = Blueprint('vehicles', __name__, template_folder='../templates/vehicles')


@vehicles_blueprint.route('/vehicles', methods=['POST'])
@accept('application/json')
@authenticate
@privileges(roles=UserRole.BACKEND_ADMIN)
def add_vehicle(_):
    post_data = request.get_json()
    if not post_data:
        raise InvalidPayload()
    plate = post_data.get('plate')

    try:
        vehicle = Vehicle.first(Vehicle.plate == plate)
        if not vehicle:
            vehicleModel = Vehicle(plate=plate)
            db.session.add(vehicleModel)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'Vehicle with plate: {plate} was added!'
            }
            return response_object, 201
        else:
            raise BusinessException(message='Sorry. That plate already exists.')
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        raise InvalidPayload()

@vehicles_blueprint.route('/vehicles/<plate>', methods=['GET'])
@accept('application/json')
@authenticate
@privileges(roles=UserRole.BACKEND_ADMIN)
def get_single_vehicle(_, plate):
    """Get single vehicle details"""
    try:
        vehicle = Vehicle.get(plate)
        if not vehicle:
            raise NotFoundException(message='Vehicle does not exist.')
        return {
            'status': 'success',
            'data': {
              'plate': vehicle.plate,
              'created_at': vehicle.created_at
            }
        }
    except ValueError:
        raise NotFoundException(message='Vehicle does not exist.')


@vehicles_blueprint.route('/vehicles', methods=['GET'])
@accept('application/json')
@authenticate
@privileges(roles=UserRole.BACKEND_ADMIN)
def get_all_vehicles(_):
    """Get all vehicles"""
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    vehicles_list = [{
            'plate': vehicle.plate,
            'created_at': vehicle.created_at
        } for vehicle in vehicles]
    return {
        'status': 'success',
        'data': {
            'vehicles': vehicles_list
        }
    }
