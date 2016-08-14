import os


class Info:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.files = os.listdir(self.path)

    def getfiles(self):
        sorted(self.files)
        for i in self.files:
            print i

if __name__ == "__main__":
    info = Info()
    info.getfiles()
