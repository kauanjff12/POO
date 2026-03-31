#questao 5
class Pais:
    def __init__(self):
        self.nome= str
        self.populacao = 0
        self.area = 0

    def calculo_densidade(self):
        return self.populacao / self.area
    

pais = Pais()
pais.nome = input("Qual o nome do pais?")
pais.pupulacao = int(input("Qual o tamanho da população?"))
pais.area = int(input("Qual a área do país?"))

print(f"a densidade demográfica do {pais.nome} é de {pais.calculo_densidade() :.2f} hab/km²")