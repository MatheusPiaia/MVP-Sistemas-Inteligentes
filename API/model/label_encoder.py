import pickle


class Label:

    def __init__(self):
        """Inicializa o pipeline"""
        self.label_encoder = None

    def carrega_label_encoder(self, path):
        """Carregamos o pipeline construído durante a fase de treinamento
        """

        with open(path, 'rb') as file:
            self.label_encoder = pickle.load(file)
        return self.label_encoder