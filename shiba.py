#! /usr/bin/python
import gtk
import funcoes


class MainWindow:
    def __init__(self):
        self.path = funcoes.get_local_path()
        self.files = {}
        self.window = gtk.Dialog()
        self.window.set_title("Shiba Files")
        self.window.set_size_request(800, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.fixed = gtk.Fixed()

        self.path_bar = gtk.Entry()
        self.path_bar.set_size_request(530, 40)
        self.path_bar.set_text(self.path)
        self.fixed.put(self.path_bar, 190, 15)

        self.button_acima = gtk.Button("Acima")
        self.button_voltar = gtk.Button("Voltar")
        self.button_ir = gtk.Button("Ir")
        self.button_copiar = gtk.Button("Copiar")
        self.button_colar = gtk.Button("Colar")
        self.button_recortar = gtk.Button("Recortar")
        self.button_excluir = gtk.Button("Excluir")
        self.button_propriedades = gtk.Button("Propriedades")

        self.button_acima.set_size_request(80, 40)
        self.button_voltar.set_size_request(80, 40)
        self.button_ir.set_size_request(50, 40)
        self.button_copiar.set_size_request(165, 35)
        self.button_colar.set_size_request(165, 35)
        self.button_recortar.set_size_request(165, 35)
        self.button_excluir.set_size_request(165, 35)
        self.button_propriedades.set_size_request(165, 35)

        self.fixed.put(self.button_voltar, 15, 15)
        self.fixed.put(self.button_acima, 100, 15)
        self.fixed.put(self.button_ir, 730, 15)
        self.fixed.put(self.button_copiar, 15, 80)
        self.fixed.put(self.button_colar, 15, 120)
        self.fixed.put(self.button_recortar, 15, 160)
        self.fixed.put(self.button_excluir, 15, 200)
        self.fixed.put(self.button_propriedades, 15, 240)

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600, 500)
        self.fixed.put(self.scrolled_window, 190, 80)

        self.list = gtk.ListStore(str, str, str, str, str)
        self.files_treeview = gtk.TreeView()
        self.files_treeview.set_model(self.list)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Nome", renderer, text=0)
        column.set_sort_column_id(0)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Tamanho", renderer, text=1)
        column.set_sort_column_id(1)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Permissoes", renderer, text=2)
        column.set_sort_column_id(2)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Dono", renderer, text=3)
        column.set_sort_column_id(3)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Tipo", renderer, text=4)
        column.set_sort_column_id(4)
        self.files_treeview.append_column(column)

        self.update_view()

        self.files_treeview.show()
        self.scrolled_window.add(self.files_treeview)


        self.window.vbox.pack_start(self.fixed)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    @staticmethod
    def destroy(self):
        gtk.main_quit(self)

    @staticmethod
    def main():
        gtk.main()

    def update_view(self):
        local = funcoes.get_local_path()
        lista = funcoes.get_list(local)
        for i in lista:
            if funcoes.existe(local + "/" + i):
                self.files[i] = funcoes.get_info(local + "/" + i)
        for j, i in self.files.iteritems():
            self.list.append([i["nome"], i["tamanho"], i["user_p"] + i["group_p"] + i["other_p"], i["uid"], i["tipo"]])


if __name__ == "__main__":
    main = MainWindow()
    main.main()
