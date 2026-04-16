class Viagem:
    def __init__(self):
        self.__distancia = 0.0
        self.__tempo = 0.0

    def set_distancia(self, d):
        if d < 0:
            raise ValueError
        else:
            self.__distancia = d

    def set_tempo(self, t):
        if t < 0:
            raise ValueError
        else:
            self.__tempo = t

    def get_distancia(self):
        return self.__distancia
    
    def get_tempo(self):
        return self.__tempo
    
    def velocidade_media(self):
        return self.__distancia / self.__tempo
    
viagem = Viagem()
viagem.set_distancia(float(input('diatancioa: ')))
viagem.set_tempo(float(input('tempo: ')))
vel = viagem.velocidade_media()
print(vel)