import os
import gtk
# os.exists(path)
# os.isfile(path)
# os.stat(path)


class MainWindow:
    def __init__(self):
        self.window = gtk.Dialog()
        self.window.set_title("Shiba Files")
        self.window.set_size_request(800, 600)
        self.window.set_resizable(True)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    @staticmethod
    def destroy(self):
        gtk.main_quit(self)

    @staticmethod
    def main():
        gtk.main()


class Info:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath("."))
        self.files = os.listdir(self.path)


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
    main = MainWindow()
    main.main()
