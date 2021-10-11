
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.auto import AutoModel

class Auto(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('year',
        type=int,
        required=True,
        help="Año de la unidad."
    )
    parser.add_argument('name',
        required=True,
        help="Modelo del auto"
    )
    parser.add_argument('color',
        required=True,
        help="Color del auto"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('user_id',
        type=int,
        required=True,
        help="Id del usuario."
    )

    def post(self):
        data = Auto.parser.parse_args()
        if AutoModel.find_by_name(data['name']):
            return {'message': "An auto whit name '{}' already exists.".format(data['name'])}, 400

        auto = AutoModel(**data)

        try:
            auto.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return auto.json(), 201


    def put(self, name):
        data = Auto.parser.parse_args()

        auto = AutoModel.find_by_name(name)

        if auto is None:
            auto = AutoModel(name, **data)
        else:
            auto.price = data['price']

        auto.save_to_db()

        return auto.json()


class AutoList(Resource):
    def get(self):
        return {'autos': [auto.json() for auto in AutoModel.query.all()]}


class AutoId(Resource):
    @jwt_required()
    def get(self, id):
        auto = AutoModel.find_by_id(id)
        if auto:
            return auto.json()
        return {'message': 'Auto not found'}, 404

    def delete(self, id):
        auto = AutoModel.find_by_id(id)
        if auto:
            auto.delete_from_db()
            return {'message': 'Auto deleted.'}
        return {'message': 'Item not found.'}, 404
