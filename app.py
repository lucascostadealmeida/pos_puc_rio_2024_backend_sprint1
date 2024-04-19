from datetime import timedelta
import traceback

from flask import jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restful import Api, reqparse

from blacklist import BLACKLIST
from model.vinho import VinhoModel
from schemas.error import ErrorAuthorizationSchema, ErrorSchema, ServerErrorSchema
from schemas.vinho import ListagemVinhosSchema, VinhoViewSchema 

info = Info(title= "Gerenciamento de vinhos", 
            description= "Esse projeto seria um piloto para gerenciamento de adegas.",
            version="1.0.0")
app = OpenAPI(__name__, info=info)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grytkRF325Fss'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

api = Api(app)
jwt = JWTManager(app)
CORS(app) 

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
vinho_tag = Tag(name="Vinho", description="Rotas para Vinhos")

security_scheme = {
    "Bearer Token": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
app.security_schemes = security_scheme

@app.get('/', tags=[home_tag])
def home():
    """ Home da aplicação.

        Redireciona para /openapi/swagger, abrindo a documentação da API.
    """
    return redirect('/openapi/swagger')

@app.get('/vinhos', tags=[vinho_tag], responses={"200" : ListagemVinhosSchema, "400":ErrorSchema, "401": ErrorAuthorizationSchema, "500":ErrorSchema})
def get_vinhos():
    """ Faz a busca por todos os Vinhos cadastrados.

        Retorna uma lista de listagem de vinhos.
    """
    try:
        vinhos = VinhoModel.query.all()
        return {'Vinhos': [vinho.json() for vinho in vinhos]}
    except Exception as e:
        traceback.print_exc()
        return {'message': 'Ocorreu um erro ao buscar vinhos.'}, 500

@app.post('/vinho', tags=[vinho_tag], responses={"201": ListagemVinhosSchema, "400":ErrorSchema, "401": ErrorAuthorizationSchema, "500":ErrorSchema})
def post_vinhos(body: VinhoViewSchema):
    """ Cria um novo vinho.

        Cria um novo vinho se tiver chave de acesso.
    """
    try:
        # Verifica se os dados obrigatórios estão presentes na requisição
        if not body.vinho or not body.uva or not body.safra:
            return {'message': 'Dados incompletos. Certifique-se de enviar vinho, uva e safra.'}, 400
        vinho = VinhoModel(vinho=body.vinho, uva=body.uva, safra=body.safra)
        vinho.save_vinho()
        return vinho.json(), 201
    except Exception as e:
        traceback.print_exc()
        return {'message': 'Ocorreu um erro ao tentar salvar o vinho.'}, 500

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)