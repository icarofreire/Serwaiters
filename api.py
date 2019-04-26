import json
from flask import Flask
from flask_restful import Resource, Api, reqparse, fields

# ---
from models import Pedidos, Pagamento_pedidos
from db import session
# ---
#from model_pee import Pedidos

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

# select * from 'tabela'
def listar(nome_tabela):
    result = session.execute(nome_tabela.__table__.select())
    con = 1
    res = {}
    for row in result:
        res[con] = dict(row)
        con+=1
    return res


class Criar_pedidos(Resource):
    def get(self, pedido_id=None):
        res = {}
        # buscar pedido pelo id;
        if pedido_id != None:
            result = session.query(Pedidos).filter(Pedidos.id == pedido_id).first()
            if result != None:
                res['mesa'] = result.mesa
                res['andar'] = result.andar
                res['pedidos'] = result.pedidos
                res['valor_pedidos'] = result.valor_pedidos
                res['data'] = result.data
                res['hora'] = result.hora
            else: res['nulo'] = 'id não existe;'
        else: 
            # buscar todos os pedidos;
            res = listar(Pedidos)
        return res

    def post(self):
        parser.add_argument('mesa')
        parser.add_argument('andar')
        parser.add_argument('pedidos', type=str, action='append', default=[])
        parser.add_argument('valor_pedidos', type=str, action='append', default=[])
        parser.add_argument('data')
        parser.add_argument('hora')
        args = parser.parse_args()

        _pedidos = args['pedidos'][0].split(',')
        _valor_pedidos = args['valor_pedidos'][0].split(',')

        #print(valor_pedidos)
        if len(_pedidos) == len(_valor_pedidos):
            ret_pedidos = Pedidos(mesa=args['mesa'],andar=args['andar'],pedidos=args['pedidos'][0],valor_pedidos=args['valor_pedidos'][0],data=args['data'],hora=args['hora'])
            session.add(ret_pedidos)
            session.commit()
            res = {}
            res['mesa'] = ret_pedidos.mesa
            res['andar'] = ret_pedidos.andar
            res['pedidos'] = ret_pedidos.pedidos
            res['valor_pedidos'] = ret_pedidos.valor_pedidos
            res['data'] = ret_pedidos.data
            res['hora'] = ret_pedidos.hora
            #ret_pedidos.save()
            return res
            #print(args)
        else: return {'erro' : 'lista com valor dos pedidos e lista de pedidos nao condizem em tamanho.'}
        return args

    def put(self, pedido_id):
        parser.add_argument('mesa')
        parser.add_argument('andar')
        parser.add_argument('pedidos', type=str, action='append', default=[])
        parser.add_argument('valor_pedidos', type=str, action='append', default=[])
        parser.add_argument('data')
        parser.add_argument('hora')
        args = parser.parse_args()

        _pedidos = args['pedidos'][0].split(',')
        _valor_pedidos = args['valor_pedidos'][0].split(',')

        #print(valor_pedidos)
        if len(_pedidos) == len(_valor_pedidos):

            row = session.query(Pedidos).filter(Pedidos.id == pedido_id).first()
            if row != None:
                row.mesa = args['mesa']
                row.andar = args['andar']
                row.pedidos = args['pedidos'][0]
                row.valor_pedidos = args['valor_pedidos'][0]
                row.data = args['data']
                row.hora = args['hora']
                session.commit()

                res = {}
                res['mesa'] = args['mesa']
                res['andar'] = args['andar']
                res['pedidos'] = args['pedidos'][0]
                res['valor_pedidos'] = args['valor_pedidos'][0]
                res['data'] = args['data']
                res['hora'] = args['hora']
                #ret_pedidos.save()
                return res
            #print(args)
        else: return {'erro' : 'lista com valor dos pedidos e lista de pedidos nao condizem em tamanho.'}
        return args

    def delete(self, pedido_id):
        res = session.query(Pedidos).filter(Pedidos.id == pedido_id).delete()
        session.commit()
        if res == 1:
            return {'ok' : 'deletado com sucesso;'}
        else: return {'erro' : 'nao existe id especificado;'}


#------- criar metodos delete<id> -----------;
class Registrar_pagamento_pedidos(Resource):
    def get(self, id_pagamento=None):
        res = {}
        # buscar pedido pelo id;
        if id_pagamento != None:
            result = session.query(Pagamento_pedidos).filter(Pagamento_pedidos.id == id_pagamento).first()
            if result != None:
                res['id_pedido'] = result.id_pedido
                res['tipo_de_pagamento'] = result.tipo_de_pagamento
                res['valor'] = result.valor
                res['data'] = result.data
                res['hora'] = result.hora
            else: res['nulo'] = 'id não existe;'
        else: 
            # buscar todos os pedidos;
            #res = listar(Pedidos)
            res = listar(Pagamento_pedidos)
        return res

    def post(self):
        parser.add_argument('id_pedido')
        parser.add_argument('tipo_de_pagamento')
        parser.add_argument('valor')
        parser.add_argument('data')
        parser.add_argument('hora')

        args = parser.parse_args()

        id_pedido = args['id_pedido']
        pri = session.query(Pedidos).filter_by( id = id_pedido ).first()
        pri_pagamento = session.query(Pagamento_pedidos).filter_by( id_pedido = id_pedido ).first()
        #print( pri_pagamento.id_pedido, int(id_pedido) )

        if pri != None and int(id_pedido) == pri.id:
            if pri_pagamento == None or (pri_pagamento != None and int(pri_pagamento.id_pedido) != int(id_pedido)):
                ret_pagamento = Pagamento_pedidos(id_pedido=args['id_pedido'], tipo_de_pagamento=args['tipo_de_pagamento'], valor=args['valor'], data=args['data'], hora=args['hora'])
                session.add(ret_pagamento)
                session.commit()
                res = {}
                res['id_pedido'] = ret_pagamento.id_pedido
                res['tipo_de_pagamento'] = ret_pagamento.tipo_de_pagamento
                res['valor'] = ret_pagamento.valor
                res['data'] = ret_pagamento.data
                res['hora'] = ret_pagamento.hora
                return res
            else: return {'nulo' : 'pagamento ja efetuado;'}
        else: return {'nulo' : 'id do pedido nao existe;'} 

    def put(self, id_pagamento=None):
        parser.add_argument('id_pedido')
        parser.add_argument('tipo_de_pagamento')
        parser.add_argument('valor')
        parser.add_argument('data')
        parser.add_argument('hora')

        args = parser.parse_args()

        id_pedido = args['id_pedido']

        row = session.query(Pagamento_pedidos).filter(Pagamento_pedidos.id == id_pagamento).first()
        if row != None:
            row.id_pedido = args['id_pedido']
            row.tipo_de_pagamento = args['tipo_de_pagamento']
            row.valor = args['valor']
            row.data = args['data']
            row.hora = args['hora']
            session.commit()

            res = {}
            res['id_pedido'] = args['id_pedido']
            res['tipo_de_pagamento'] = args['tipo_de_pagamento']
            res['valor'] = args['valor']
            res['data'] = args['data']
            res['hora'] = args['hora']
            return res
        else: return {'erro' : 'id do pagamento não existe;'}

    def delete(self, id_pagamento=None):
        res = session.query(Pagamento_pedidos).filter(Pagamento_pedidos.id == id_pagamento).delete()
        session.commit()
        if res == 1:
            return {'ok' : 'deletado com sucesso;'}
        else: return {'erro' : 'nao existe id especificado;'}


api.add_resource(Criar_pedidos, '/pedido', '/pedido/<pedido_id>')
api.add_resource(Registrar_pagamento_pedidos, '/pagamento_pedido', '/pagamento_pedido/<id_pagamento>')


if __name__ == '__main__': app.run(debug=True)
