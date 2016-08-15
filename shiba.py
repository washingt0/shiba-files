import os


class Info:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath("."))
        self.files = os.listdir(self.path)


    #todo carga de informacoes a partir do os
    def loadinfo(self):
        for i in self.files:
            objs = []
            #objs.append(Object(i, )


class Object:
    def __init__(self, nome, owner, group, perm, size, datas):
        self.info = []
        self.info.append(nome)
        self.info.append(owner)
        self.info.append(group)
        self.info.append(perm)
        self.info.append(size)
        for i in datas:
            self.info.append(i)

    def getinfo(self):
        return self.info


if __name__ == "__main__":
    print "Testando"
