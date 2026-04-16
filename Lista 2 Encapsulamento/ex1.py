import math
class Circulo:
    def __init__(self):
        self.__r = 0.0

    def set_raio(self, r):
        if r > 0:
            self.__r = r
        else:
            raise ValueError
        
    def get_raio(self):
        return self.__r
    
    def calc_area(self):
        area = math.pi * self.__r ** 2
        return area

    def calc_circuferencia(self):
        circ = math.pi * 2 * self.__r
        return circ

#--------------------------------------------

circulo = Circulo()
circulo.set_raio(float(input('o raio do circulo: ')))

area = circulo.calc_area()
print(f"esta é a àrea do círculo: {area}")
circ = circulo.calc_circuferencia()
print(f'essa é tua circuferencia: {circ}')

