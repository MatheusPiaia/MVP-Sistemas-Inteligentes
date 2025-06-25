from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify, render_template
from urllib.parse import unquote
import joblib

from sqlalchemy.exc import IntegrityError

from model import Session, Model, Avaliador, Usuario, Pipeline, PreProcessador
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info, static_folder='../front', static_url_path='/front')
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização, remoção e predição da personalidade do usuário")


# Rota home - redireciona para o frontend
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend.
    """
    return redirect('/openapi')


# Rota para documentação OpenAPI
@app.get('/docs', tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#Rota get para listar todos usuarios cadastrados
@app.get('/usuarios', tags=[usuario_tag],
         responses={"200" : UsuarioViewSchema, "404" : ErrorSchema})
def get_usuarios():
    '''Lista todos os usuarios cadastrados na base
    '''
    logger.debug("Coletando dados sobre todos os usuarios")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os usuarios
    usuarios = session.query(Usuario).all()
    
    if not usuarios:
        # Se não houver usuarios
        return {"usuarios": []}, 200
    else:
        logger.debug(f"%d usuarios econtrados" % len(usuarios))
        print(usuarios)
        return apresenta_usuarios(usuarios), 200


#Roda post para adicionar usuario ao banco
@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def predict(form: UsuarioSchema):
    '''Adiciona um novo usuario a base de dados
        Retorna uma representação dos usuarios e a predição da personalidade
    '''

    preprocessador = PreProcessador()
    pipeline = Pipeline()
    #label_encoder = Label()

    # Recuperando dados do formulario
    name = form.name
    time_spent_alone = form.time_spent_alone
    stage_fear = form.stage_fear
    social_event_attendance = form.social_event_attendance
    going_outside = form.going_outside
    drained_after_socializing = form.drained_after_socializing
    friends_circle_size = form.friends_circle_size
    post_frequency = form.post_frequency    
    #Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    logger.debug(f"{X_input}")
    
    # Carregando o modelo
    model_path = './MachineLearning/pipelines/rf_personality_pipeline.pkl'   
    modelo = pipeline.carrega_pipeline(model_path)
    #Realizando a predição
    #modelo = joblib.load("./MachineLearning/pipelines/rf_personality_pipeline.pkl")
    label_encoder = joblib.load("./MachineLearning/encoder/label_encoder.pkl")    
    y_pred_encoded = modelo.predict(X_input)[0]
    personality = label_encoder.inverse_transform([y_pred_encoded])[0]

    usuario = Usuario(
        name = name,
        time_spent_alone = time_spent_alone,
        stage_fear = stage_fear,
        social_event_attendance = social_event_attendance,
        going_outside = going_outside,
        drained_after_socializing = drained_after_socializing,
        friends_circle_size = friends_circle_size,
        post_frequency = post_frequency,
        personality= personality,
    )
    logger.debug(f"Adicionando usuario de nome: '{usuario.name}'")

    try:
        #Criando conexão com a base
        session = Session()

        # Checanco se usuario já existe na base
        if session.query(Usuario).filter(Usuario.name == form.name).first():
            error_msg = "Usuario já existente na base"
            logger.warning(f"Erro ao adicionar usuario '{usuario.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        session.add(usuario)
        session.commit()
        logger.debug(f"Adiciona usuario de nome '{usuario.name}'")
        return apresenta_usuario(usuario), 200
    
    except Exception as e:
        error_msg = "Não foi possível salvar usuario na base"
        logger.warning(f"Erro ao adicionar usuario '{usuario.name}'")
        return {"message": error_msg}, 400

# Rota delete para remover usuario pelo nome da base
@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def delete_usuario(query: UsuarioBuscaSchema):
    '''Remove um usuario cadastrado na base pelo nome
    '''

    usuario_name = unquote(query.name)
    logger.debug(f"Deletando dados sobre o usuario '{usuario_name}'")

    session = Session()

    usuario = session.query(Usuario).filter(Usuario.name == usuario_name).first()

    if not usuario:
        error_msg = "Usuario não encontrado na base"
        logger.warning(f"Erro ao deletar o usuario '{usuario_name}'")
        return{"message": error_msg}, 404

    else:
        session.delete(usuario)
        session.commit()
        logger.debug(f"Deletado usuario '{usuario_name}'")
        return {"message": f"Usuario {usuario_name} removido com sucesso"}

if __name__ == '__main__':
    app.run(debug=True)
