from model import *


# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./MachineLearning/data/test_dataset_personality.csv"
colunas = ['Time_spent_Alone', 'Stage_fear', 'Social_event_attendance', 'Going_outside', 'Drained_after_socializing', 'Friends_circle_size', 'Post_frequency', 'Personality']
numeric_columns = ['Time_spent_Alone', 'Social_event_attendance', 'Going_outside', 'Friends_circle_size', 'Post_frequency']
categorical_columns = ['Stage_fear', 'Drained_after_socializing']
target_column = 'Personality'


# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

X = dataset[numeric_columns + categorical_columns]
y = dataset[target_column]

# Método para testar o modelo RandomForest a partir do arquivo correspondente

def test_modelo_rf():  
    # Importando o modelo RandomForest
    rf_path = './MachineLearning/pipelines/rf_personality_pipeline.pkl'
    
    modelo_rf = pipeline.carrega_pipeline(rf_path)   
  
    # Obtendo as métricas da Regressão Logística
    acuracia_rf = avaliador.avaliar(modelo_rf, X, y)
    print(acuracia_rf)
    
    # Testando as métricas da Regressão Logística 
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_rf >= 0.90

