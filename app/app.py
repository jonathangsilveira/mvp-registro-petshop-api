from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, Response, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

info = Info(title="MVP Registro Petshop API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

@app.route('/api')
def documentation():
    """Redireciona para visualização do estilo de documentação Swagger.
    """
    return redirect('/openapi/swagger')