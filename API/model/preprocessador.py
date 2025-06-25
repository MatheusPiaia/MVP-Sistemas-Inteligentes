from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import pandas as pd

class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=42):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                  percentual_teste,
                                                                  seed)
        # normalização/padronização
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        X_input = pd.DataFrame({'Time_spent_Alone': [form.time_spent_alone], 
                            'Stage_fear': [form.stage_fear], 
                            'Social_event_attendance': [form.social_event_attendance], 
                            'Going_outside': [form.going_outside], 
                            'Drained_after_socializing': [form.drained_after_socializing], 
                            'Friends_circle_size': [form.friends_circle_size], 
                            'Post_frequency': [form.post_frequency]} )                           
                        
        return X_input