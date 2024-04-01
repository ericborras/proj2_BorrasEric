import json
import os

class Configuracio:
    def __init__(self, arxiu):
        self.arxiu = arxiu
        self.ruta_arxiu = os.path.join(os.path.dirname(__file__), arxiu)
        self.conf = self.carrega_conf()  # Utiliza el método carrega_conf() para inicializar conf

    def carrega_conf(self):
        try:
            with open(self.ruta_arxiu, 'r') as arxiu:
                return json.load(arxiu)
        except FileNotFoundError:
            return {}

    def guarda_conf(self):
        with open(self.ruta_arxiu, 'w') as arxiu:
            json.dump(self.conf, arxiu, indent=4)

    def get_valor(self, clau):
        return self.conf.get(clau)

    def modificar_valor(self, clau, nou_valor):
        self.conf[clau] = nou_valor
        self.guarda_conf()
