#! /usr/bin/python
import gtk
import os
import funcoes
# os.exists(path)
# os.isfile(path)
# os.stat(path)


class MainWindow:
    def __init__(self):
        self.path = os.getcwd()
        self.files = {}
        self.window = gtk.Window()
        self.window.set_title("Shiba Files")
        self.window.set_size_request(800, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(750, 500)
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.window.vbox.pack_start(self.scrolled_window, True, True, 0)
        self.scrolled_window.show()
        self.store = gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str, str)

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
