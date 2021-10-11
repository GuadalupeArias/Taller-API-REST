
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.auto import AutoModel


def string_name(str, type):
    if str.isspace():
        raise ValidationError("No puede ingresar solo espacios")
    return str

def string_color(str, type):
    if str not in colores:
        raise ValueError("No puede ingresar solo espacios")
    return str

colores = ["Gris", "Negro", "Blanco", "Rojo", "Azul"]


class Auto(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('year',
        type=int,
        required=True,
        help="El año de la unidad es obligatorio y debe ser un valor numérico."
    )
    parser.add_argument('name',
        type=string_name,
        required=True,
        help="Error al ingresar el modelo"
    )
    parser.add_argument('color',
        type=string_color,
        required=True,
        help="El color del auto no puede estar en blanco."
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help="El precio del auto es obligatorio y debe ser un valor numérico."
    )
    parser.add_argument('user_id',
        type=int,
        required=True,
        help="El ID del vendedor es obligatorio y debe ser un valor numérico."
    )

    def post(self):
        data = Auto.parser.parse_args()
        auto = AutoModel.find_by_name(data['name'], data['year'], data['color'])
        if auto:
            return {'message': "Ya existe el modelo '{}' como ese mismo año y color.".format(data['name'])}, 400
        auto = AutoModel(**data)
        try:
            auto.save_to_db()
        except:
            return {"message": "Surgió un error inesperado guardando el auto."}, 500

        return auto.json(), 201


class AutoList(Resource):
    def get(self):
        return {'autos': [auto.json() for auto in AutoModel.query.order_by(AutoModel.id).all()]}


class AutoId(Resource):
    @jwt_required()
    def get(self, id):
        auto = AutoModel.find_by_id(id)
        if auto:
            return auto.json()
        return {'message': 'El auto solicitado no existe'}, 404

    def delete(self, id):
        auto = AutoModel.find_by_id(id)
        if auto:
            auto.delete_from_db()
            return {'message': 'Auto eliminado.'}
        return {'message': 'No se encontró el auto buscado.'}, 404

    def put(self, id):
        data = Auto.parser.parse_args()
        auto = AutoModel.find_by_id(id)
        if auto is None:
            auto = AutoModel(**data)
        else:
            auto2 = AutoModel.find_by_name(data['name'], data['year'], data['color'])
            if auto2 and auto2.id != auto.id:
                return {'message': "Ya existe el modelo '{}' como ese mismo año y color.".format(data['name'])}, 400

            auto.name = data['name']
            auto.year = data['year']
            auto.color = data['color']
            auto.price = data['price']

        auto.save_to_db()
        return auto.json()
