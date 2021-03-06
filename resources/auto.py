from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.auto import AutoModel
from marshmallow import ValidationError
from flask import jsonify
from flask import request
import json
import requests
from requests.structures import CaseInsensitiveDict
#cambiar recurso a plural. (autos) (no lo hago para no joder al front)

# url para el request del token http://concesionario-crud.herokuapp.com/me

def string_name(str, type):
    if str.isspace():
        raise ValidationError("El modelo no puede estar vacio.")
    return str

def string_color(str, type):
    if str not in colores:
        raise ValidationError("El color del auto solo puede ser: Gris, Negro, Blanco, Rojo o Azul.")
    return str

def float_precio(float, type):
    if float <=0:
        raise ValidationError("El precio del auto es obligatorio y debe ser un valor numérico mayor a 0")
    return float

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
        required=True
    )
    parser.add_argument('color',
        type=string_color,
        required=True
    )
    parser.add_argument('price',
        type=float_precio,
        required=True
    )


    parsarg = reqparse.RequestParser()
    parsarg.add_argument('year',
        type=int,
        required=False,
        help="El año de la unidad es obligatorio, solo se admiten autos del 2020 en adelante."
    )
    parsarg.add_argument('color',
        type=string_color,
        required=False
    )


    def post(self):
        data = Auto.parser.parse_args()
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            url = "https://concesionario-crud.herokuapp.com/me"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer {}".format(token)
            resp = requests.get(url, headers=headers)
            datos = resp.json()
            if resp.status_code == 200:
                if data['price'] is None or data['name'] is None or data['name'] == "" or data['year'] is None:
                    return {'message': {'campos': 'Los campos no pueden estar vacios'}}, 400
                if data['year'] <2020:
                    return {'message': {'year': 'El año de la unidad es obligatorio, solo se admiten autos del 2020 en adelante.'}}, 412
                auto = AutoModel.find_by_name(data['name'], data['year'], data['color'])
                if auto:
                    return {'message': {"modelo": "Ya existe el modelo '{}' como ese mismo año y color.".format(data['name'])}}, 409
                auto = AutoModel(data['year'], data['name'], data['color'], data['price'], datos['idUsuario'])
                try:
                    auto.save_to_db()
                except:
                    return {"message": "Surgió un error inesperado guardando el auto."}, 500

                return auto.json(), 201
            else:
                return {"message": "No autorizado."}, 401
        else:
            return {"message": "No autorizado."}, 401


    def get(self):
        #data = Auto.parsarg.parse_args()
        #color = data['color']
        #year = data['year']
        color = request.args.get('color')
        year = request.args.get('year')
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)
            url = "https://concesionario-crud.herokuapp.com/me"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer {}".format(token)
            resp = requests.get(url, headers=headers)
            print(resp.status_code)
            if resp.status_code == 200:
                if color is None and year is None: #sin parametros de busqueda
                    return jsonify([auto.json() for auto in AutoModel.query.order_by(AutoModel.id).all()])
                elif color:
                    if year: #busqueda por color y año
                        try:
                            val = int(year)
                        except ValueError:
                            return {'message': {'year': 'El año de la unidad debe ser un entero.'}}, 400
                        return jsonify([auto.json() for auto in AutoModel.query.filter(AutoModel.color==color).filter(AutoModel.year==year).order_by(AutoModel.id)])
                    else: #busqueda por color
                        return jsonify([auto.json() for auto in AutoModel.query.filter(AutoModel.color==color).order_by(AutoModel.id)])
                else: #busqueda por año
                    try:
                        val = int(year)
                    except ValueError:
                        return {'message': {'year': 'El año de la unidad debe ser un entero.'}}, 400
                    return jsonify([auto.json() for auto in AutoModel.query.filter(AutoModel.year==year).order_by(AutoModel.id)])
            else:
                return {"message": "No autorizado."}, 401
        else:
            return {"message": "No autorizado."}, 401

class AutoId(Resource):
    def get(self, id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            url = "https://concesionario-crud.herokuapp.com/me"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer {}".format(token)
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                auto = AutoModel.find_by_id(id)
                if auto:
                    return auto.json()
                return {'message': 'El auto solicitado no existe'}, 404
            else:
                return {"message": "No autorizado."}, 401
        else:
            return {"message": "No autorizado."}, 401

    def delete(self, id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            url = "https://concesionario-crud.herokuapp.com/me"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer {}".format(token)
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                auto = AutoModel.find_by_id(id)
                if auto:
                    auto.delete_from_db()
                    return {'': ''}, 204
                return {'message': 'No se encontró el auto buscado.'}, 404
            else:
                return {"message": "No autorizado."}, 401
        else:
            return {"message": "No autorizado."}, 401

    def put(self, id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            url = "https://concesionario-crud.herokuapp.com/me"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer {}".format(token)
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                data = Auto.parser.parse_args()
                if data['price'] is None or data['name'] is None or data['name'] == "" or data['year'] is None:
                    return {'message': {"campos": "Los campos no pueden estar vacios"}}, 400
                if data['year'] <2020:
                    return {'message': {'year': 'El año de la unidad es obligatorio, solo se admiten autos del 2020 en adelante.'}}, 412
                auto = AutoModel.find_by_id(id)
                if auto is None:
                    return {'message': 'No se encontró el auto buscado.'}, 404
                else:
                    auto2 = AutoModel.find_by_name(data['name'], data['year'], data['color'])
                    if auto2 and auto2.id != auto.id:
                        return {'message': "Ya existe el modelo '{}' como ese mismo año y color.".format(data['name'])}, 409

                    auto.name = data['name']
                    auto.year = data['year']
                    auto.color = data['color']
                    auto.price = data['price']


                auto.save_to_db()
                return auto.json()
            else:
                return {"message": "No autorizado."}, 401
        else:
            return {"message": "No autorizado."}, 401
