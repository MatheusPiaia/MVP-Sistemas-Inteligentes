import pytest
import json
from app import app
from model import Session, Usuario

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_user_data():
    """Dados de exemplo para teste de Usuario"""
   
    return {
        "name": "Roberto",
        "time_spent_alone": 5,
        "stage_fear": "Yes",
        "social_event_attendance": 5,
        "going_outside": 2,
        "drained_after_socializing": "Yes",
        "friends_circle_size": 2,
        "post_frequency": 1        
    }


def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/FrontEnd/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_users_empty(client):
    """Testa a listagem de usuarios quando não há nenhum"""
    response = client.get('/usuarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'usuarios' in data
    assert isinstance(data['usuarios'], list)

def test_add_user_prediction(client, sample_user_data):
    """Testa a adição de um usuario com predição da personalidade"""
    # Primeiro, vamos limpar qualquer Usuario existente com o mesmo nome
    session = Session()
    existing_user = session.query(Usuario).filter(Usuario.name == sample_user_data['name']).first()
    if existing_user:
        session.delete(existing_user)
        session.commit()
    session.close()
    
    # Agora testamos a adição
    response = client.post('/usuario', data=sample_user_data)       
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verifica se o usuario foi criado com todas as informações
    assert data['name'] == sample_user_data['name']
    assert data['time_spent_alone'] == sample_user_data['time_spent_alone']
    assert data['stage_fear'] == sample_user_data['stage_fear']
    assert data['social_event_attendance'] == sample_user_data['social_event_attendance']
    assert data['going_outside'] == sample_user_data['going_outside']
    assert data['drained_after_socializing'] == sample_user_data['drained_after_socializing']
    assert data['friends_circle_size'] == sample_user_data['friends_circle_size']    
    assert data['post_frequency'] == sample_user_data['post_frequency']   
    
    # Verifica se a predição foi feita (personality deve estar presente)
    assert 'personality' in data
    assert data['personality'] in ["Introvert", "Extrovert"]

def test_add_duplicate_user(client, sample_user_data):
    """Testa a adição de um usuario duplicado"""
    # Primeiro adiciona o usuario
    response = client.post('/usuario', data=sample_user_data)
    
    # Tenta adicionar novamente
    response = client.post('/usuario', data=sample_user_data)
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']


def test_delete_user(client, sample_user_data):
    """Testa a remoção de um usuario"""
    # Primeiro adiciona o usuario
    client.post('/usuario', 
                data=sample_user_data)
    
    # Remove o usuario
    response = client.delete(f'/usuario?name={sample_user_data["name"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removido com sucesso' in data['message']

def test_delete_nonexistent_user(client):
    """Testa a remoção de um usuario que não existe"""
    response = client.delete('/usuario?name=UsuarioInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_prediction_min(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    session = Session()
    existing_user = session.query(Usuario).filter(Usuario.name == "Usuario Maximo Introvertido").first()
    if existing_user:
        session.delete(existing_user)
        session.commit()
    session.close()

    min_data = {
        "name": "Usuario Maximo Introvertido",
        "time_spent_alone": 11, # Quanto maior esse valor + Introvert
        "stage_fear": "Yes",
        "social_event_attendance": 0,
        "going_outside": 0,
        "drained_after_socializing": "Yes",
        "friends_circle_size": 0,
        "post_frequency": 0 
    }      
    
    response = client.post('/usuario', data=min_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'personality' in data  
    

def test_prediction_max(client):
    # Teste com valores máximos típicos
    session = Session()
    existing_user = session.query(Usuario).filter(Usuario.name == "Usuario Maximo Extrovertido").first()
    if existing_user:
        session.delete(existing_user)
        session.commit()
    session.close()
    max_data = {
        "name": "Usuario Maximo Extrovertido",
        "time_spent_alone": 0,
        "stage_fear": "No",
        "social_event_attendance": 10,
        "going_outside": 7,
        "drained_after_socializing": "No",
        "friends_circle_size": 15,
        "post_frequency": 10 
    }    
    
    response = client.post('/usuario', data=max_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'personality' in data

def cleanup_test_patients():
    """Limpa Usuarios de teste do banco"""
    session = Session()
    test_users = session.query(Usuario).filter(
        Usuario.name.in_(['Roberto', 'Usuario Maximo Introvertido', 'Usuario Maximo Extrovertido'])
    ).all()
    
    for user in test_users:
        session.delete(user)
    session.commit()
    session.close()

# Executa limpeza após os testes

def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_patients()
