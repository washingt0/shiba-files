#! /usr/bin/python
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

if __name__ == "__main__":
    main = MainWindow()
    main.main()
