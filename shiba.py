#! /usr/bin/python

# Instituto Federal de Ciencia Educacao e Tecnologia do Ceara - Campus Crato
# Curso: Bacharelado em Sistemas de Informacao
# Disciplina: Sistemas Operacionais
# Professor Orientador: Guilherme Esmeraldo
# Equipe: Hyago Sayomar
#         Marcelo Bezerra
#         Washington Santos
# Resumo: Gerenciador de arquivos para GNU/Linux, escrito em python 2.7 + PyGTK
# Requerimentos: Python 2.7+, PyGTK2

import gtk
import funcoes


# classe principal da GUI
class MainWindow:
    def __init__(self):
        # inicializa alguns atributos
        self.open_window = self.cuserid = self.cgroupid = self.cpermissoes = self.sym_win = self.symlink_uri = None
        self.link_name = self.folder_win = self.folder_name = self.file_win = self.file_name = self.copy_uri = None
        self.oculto = True
        self.path = funcoes.get_local_path()
        self.old_path = []
        self.files = {}
        self.crop = False

        # instancia o dialogo que sera exibido e configura alguns parametros
        self.window = gtk.Dialog()
        self.window.set_title("Shiba Files")
        self.window.set_size_request(800, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.fixed = gtk.Fixed()
        self.shiba = gtk.Image()
        self.shiba.set_from_file("./pics/shiba.jpg")
        self.fixed.put(self.shiba, 15, 440)

        # instancia uma subjanela com scroll e configura alguns parametros
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600, 500)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        # instancia a barra de enderecos e configura alguns parametros
        self.path_bar = gtk.Entry()
        self.path_bar.connect("activate", self.action_go)
        self.path_bar.set_size_request(530, 40)
        self.path_bar.set_text(self.path)
        self.fixed.put(self.path_bar, 190, 15)

        # instancia a model que ira compor a TreeView
        self.list = gtk.ListStore(str, str, str, str, str)
        self.update_view(self.oculto)

        # instancia a TreeView
        self.files_treeview = gtk.TreeView()
        self.files_treeview.set_model(self.list)

        # instacia as colunas da TreeView, o renderizador e configura alguns parametros
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Nome", renderer, text=0)
        column.set_sort_column_id(0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(270)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Tamanho", renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(80)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Permissoes", renderer, text=2)
        column.set_sort_column_id(2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(80)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Dono", renderer, text=3)
        column.set_sort_column_id(3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(80)
        self.files_treeview.append_column(column)
        column = gtk.TreeViewColumn("Tipo", renderer, text=4)
        column.set_sort_column_id(4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(80)
        self.files_treeview.append_column(column)

        # instancia os botoes
        self.button_acima = gtk.Button("Acima")
        self.button_voltar = gtk.Button("Voltar")
        self.button_ir = gtk.Button("Ir")
        self.button_copiar = gtk.Button("Copiar")
        self.button_colar = gtk.Button("Colar")
        self.button_recortar = gtk.Button("Recortar")
        self.button_excluir = gtk.Button("Excluir")
        self.button_propriedades = gtk.Button("Propriedades")
        self.button_symlink = gtk.Button("Criar SymLink")
        self.button_novo = gtk.Button("Novo Arquivo")
        self.button_pasta = gtk.Button("Nova Pasta")
        self.button_oculto = gtk.Button("Mostrar Ocultos")

        # configura o tamanho dos botoes
        self.button_acima.set_size_request(80, 40)
        self.button_voltar.set_size_request(80, 40)
        self.button_ir.set_size_request(50, 40)
        self.button_copiar.set_size_request(165, 35)
        self.button_colar.set_size_request(165, 35)
        self.button_recortar.set_size_request(165, 35)
        self.button_excluir.set_size_request(165, 35)
        self.button_propriedades.set_size_request(165, 35)
        self.button_symlink.set_size_request(165, 35)
        self.button_novo.set_size_request(165, 35)
        self.button_pasta.set_size_request(165, 35)
        self.button_oculto.set_size_request(165, 35)

        # configura a acao de cada botao
        self.button_acima.connect("clicked", self.action_up)
        self.button_voltar.connect("clicked", self.action_back)
        self.button_ir.connect("clicked", self.action_go)
        self.button_oculto.connect("clicked", self.action_oculto)
        self.button_copiar.connect("clicked", self.action_copy)
        self.button_colar.connect("clicked", self.action_paste)
        self.button_recortar.connect("clicked", self.action_crop)
        self.button_excluir.connect("clicked", self.action_delete)
        self.button_propriedades.connect("clicked", self.action_properties)
        self.button_symlink.connect("clicked", self.action_symlink)
        self.button_novo.connect("clicked", self.action_file)
        self.button_pasta.connect("clicked", self.action_folder)

        # inclui os botoes no painel fixo
        self.fixed.put(self.scrolled_window, 190, 80)
        self.fixed.put(self.button_voltar, 15, 15)
        self.fixed.put(self.button_acima, 100, 15)
        self.fixed.put(self.button_ir, 730, 15)
        self.fixed.put(self.button_copiar, 15, 80)
        self.fixed.put(self.button_colar, 15, 120)
        self.fixed.put(self.button_recortar, 15, 160)
        self.fixed.put(self.button_excluir, 15, 200)
        self.fixed.put(self.button_propriedades, 15, 240)
        self.fixed.put(self.button_symlink, 15, 280)
        self.fixed.put(self.button_novo, 15, 320)
        self.fixed.put(self.button_pasta, 15, 360)
        self.fixed.put(self.button_oculto, 15, 400)

        # configura acao para quando um registro for ativado
        self.files_treeview.connect('row-activated', self.open_folder)

        # torna a TreeView visivel e adiciona ela na janela com scroll
        self.files_treeview.show()
        self.scrolled_window.add(self.files_treeview)

        # cria uma referencia para o registro selecionado e e configura alguns parametros
        self.selected = self.files_treeview.get_selection()
        self.selected.set_mode(gtk.SELECTION_SINGLE)
        self.selected.select_path(0)

        # torna todos os componentes do dialogo visiveis e conecta a funcao de destruicao
        self.window.vbox.pack_start(self.fixed)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    # realiza a mudanca de path a partir da ativacao da coluna
    def open_folder(self, treeview, path, column):
        sel = funcoes.get_local_path() + "/" + self.get_selected()
        self.path_bar.set_text(sel)
        self.action_go(self)
        return 0

    # atualiza a lista que compoe a TreeView
    def update_view(self, oculto):
        self.list.clear()
        self.files.clear()
        local = funcoes.get_local_path()
        lista = funcoes.get_list(local)
        self.path_bar.set_text(local)
        for i in lista:
            if funcoes.existe(local + "/" + i):
                self.files[i] = funcoes.get_info(local + "/" + i, 0)
        for j, i in self.files.iteritems():
            if oculto and i["nome"][0] == '.':
                pass
            else:
                self.list.append([i["nome"], i["tamanho"], i["user_p"] + i["group_p"] + i["other_p"], i["uid"],
                                  i["tipo"]])
        return 0

    # acao de subir um nivel
    def action_up(self, widget):
        self.old_path.append(self.path)
        self.path = funcoes.ir_acima()
        self.update_view(self.oculto)
        return 0

    # acao de voltar
    def action_back(self, widget):
        try:
            if len(self.old_path) == 0:
                pass
            else:
                self.path = self.old_path.pop()
                funcoes.ir_para(self.path)
                self.update_view(self.oculto)
        except ValueError:
            pass
        return 0

    # acao de alterar o diretorio a partir da barra de enderecos
    def action_go(self, widget):
        self.old_path.append(self.path)
        self.path = self.path_bar.get_text()
        funcoes.ir_para(self.path)
        self.update_view(self.oculto)
        return 0

    # exibe/mostra arquivos/pastas ocultas
    def action_oculto(self, widget):
        if self.oculto:
            self.oculto = False
            self.button_oculto.set_label("Esconder Ocultos")
            self.update_view(self.oculto)
        else:
            self.oculto = True
            self.button_oculto.set_label("Mostrar Ocultos")
            self.update_view(self.oculto)
        return 0

    # obtem apenas o nome do arquivo/diretorio selecionado
    def get_selected(self):
        try:
            selec = self.selected.get_selected()
            selecionado = self.list.get_value(selec[1], 0)
        except ValueError:
            selecionado = None
        return selecionado

    # prepara as variaveis para efetuar a copia de um arquivo/pasta
    def action_copy(self, widget):
        self.copy_uri = funcoes.get_local_path() + "/" + self.get_selected()
        return 0

    # prepara as variaveis para efetuar o movimento de um arquivo/pasta
    def action_crop(self, widget):
        self.crop = True
        self.copy_uri = funcoes.get_local_path() + "/" + self.get_selected()
        return 0

    # cola um arquivo/pasta
    def action_paste(self, widget):
        funcoes.colar(self.copy_uri)
        if self.crop:
            funcoes.excluir(self.copy_uri)
            self.crop = False
        self.update_view(self.oculto)
        return 0

    # exclui um arquivo
    def action_delete(self, widget):
        funcoes.excluir(funcoes.get_local_path() + "/" + self.get_selected())
        self.update_view(self.oculto)
        return 0

    # carrega a janela de visualizacao/edicao de um arquivo/diretorio
    def action_properties(self, widget):
        selecionado = self.get_selected()
        self.open_window = funcoes.get_local_path()+"/"+selecionado
        info = funcoes.get_info(self.open_window, 1)
        if selecionado is None:
            pass
        else:
            win = gtk.Dialog()
            win.set_title("Propriedades")
            win.set_size_request(350, 300)
            win.set_resizable(False)

            fix = gtk.Fixed()
            tnome = gtk.Label("Nome: ")
            ttamanho = gtk.Label("Tamanho: ")
            tuserid = gtk.Label("UID: ")
            tgroupid = gtk.Label("GID: ")
            tpermissoes = gtk.Label("Permissoes: ")
            tdtcriacao = gtk.Label("Data de Criacao: ")
            tdtacesso = gtk.Label("Data de Acesso: ")
            tdtmod = gtk.Label("Data de Modificacao: ")

            cnome = gtk.Label(info["nome"])
            ctamanho = gtk.Label(info["tamanho"])

            self.cuserid = gtk.Entry()
            self.cuserid.set_size_request(50, 25)
            self.cuserid.set_max_length(4)
            self.cuserid.set_text(str(info["uid"]))

            self.cgroupid = gtk.Entry()
            self.cgroupid.set_size_request(50, 25)
            self.cgroupid.set_text(str(info["gid"]))
            self.cgroupid.set_max_length(4)

            self.cpermissoes = gtk.Entry()
            self.cpermissoes.set_size_request(50, 25)
            self.cpermissoes.set_text(info["perm"])
            self.cpermissoes.set_max_length(3)

            cdtcriacao = gtk.Label(info["data_cr"]+"  "+info["hora_cr"])
            cdtacesso = gtk.Label(info["data_ac"]+"  "+info["hora_ac"])
            cdtmod = gtk.Label(info["data_mo"]+"  "+info["hora_mo"])
            button_permissao = gtk.Button("Aplicar")
            button_uid = gtk.Button("Aplicar")
            button_gid = gtk.Button("Aplicar")

            button_permissao.set_size_request(100, 25)
            button_permissao.connect("clicked", self.action_alter_perm)
            button_uid.set_size_request(100, 25)
            button_uid.connect("clicked", self.action_alter_uid)
            button_gid.set_size_request(100, 25)
            button_gid.connect("clicked", self.action_alter_gid)

            fix.put(tnome, 30, 20)
            fix.put(ttamanho, 30, 50)
            fix.put(tuserid, 30, 80)
            fix.put(tgroupid, 30, 110)
            fix.put(tpermissoes, 30, 140)
            fix.put(tdtcriacao, 30, 170)
            fix.put(tdtmod, 30, 200)
            fix.put(tdtacesso, 30, 230)
            fix.put(cnome, 180, 20)
            fix.put(ctamanho, 180, 50)
            fix.put(self.cuserid, 180, 75)
            fix.put(self.cgroupid, 180, 105)
            fix.put(self.cpermissoes, 180, 135)
            fix.put(cdtcriacao, 180, 170)
            fix.put(cdtmod, 180, 200)
            fix.put(cdtacesso, 180, 230)

            fix.put(button_permissao, 240, 135)
            fix.put(button_gid, 240, 105)
            fix.put(button_uid, 240, 75)

            win.vbox.pack_start(fix)
            win.show_all()
        return 0

    # prepara os dados para alterar UID
    def action_alter_uid(self, widget):
        new_uid = self.cuserid.get_text()
        funcoes.alter_uid(self.open_window, new_uid)
        self.update_view(self.oculto)
        return 0

    # prepara os dados para alterar GID
    def action_alter_gid(self, widget):
        new_gid = self.cgroupid.get_text()
        funcoes.alter_gid(self.open_window, new_gid)
        self.update_view(self.oculto)
        return 0

    # prepara os dados para alterar as permissoes
    def action_alter_perm(self, widget):
        new_perm = '0'
        new_perm += self.cpermissoes.get_text()
        funcoes.alter_perm(self.open_window, new_perm)
        return 0

    # carrega a janela para criacao de um symlink
    def action_symlink(self, widget):
        self.sym_win = gtk.Dialog()
        self.sym_win.set_title("Criar Link")
        self.sym_win.set_size_request(400, 150)
        self.sym_win.set_resizable(False)
        fix = gtk.Fixed()
        title = gtk.Label("Origem: ")
        subtitle = gtk.Label("Nome do symlink:")
        self.symlink_uri = gtk.Entry()
        self.symlink_uri.set_max_length(200)
        self.symlink_uri.set_size_request(150, 30)
        self.link_name = gtk.Entry()
        self.link_name.set_size_request(150, 30)
        self.link_name.set_max_length(200)
        button_criar = gtk.Button("Criar")
        button_criar.set_size_request(60, 30)
        button_criar.connect("clicked", self.go_link)
        fix.put(title, 15, 15)
        fix.put(self.symlink_uri, 180, 15)
        fix.put(self.link_name, 180, 50)
        fix.put(subtitle, 15, 50)
        fix.put(button_criar, 170, 100)
        self.sym_win.vbox.pack_start(fix)
        self.sym_win.show_all()
        return 0

    # prepara os dados para criar um symlink
    def go_link(self, widget):
        dest = funcoes.get_local_path() + "/" + self.link_name.get_text()
        origem = self.symlink_uri.get_text()
        funcoes.create_symlink(origem, dest)
        self.sym_win.destroy()
        self.update_view(self.oculto)
        return 0

    # carrega a janela para criacao de uma nova pasta
    def action_folder(self, widget):
        self.folder_win = gtk.Dialog()
        self.folder_win.set_title("Criar pasta")
        self.folder_win.set_size_request(400, 80)
        self.folder_win.set_resizable(False)
        fix = gtk.Fixed()
        title = gtk.Label("Nome: ")
        self.folder_name = gtk.Entry()
        self.folder_name.set_size_request(300, 30)
        self.folder_name.set_max_length(200)
        button_criar = gtk.Button("Criar")
        button_criar.set_size_request(60, 30)
        button_criar.connect("clicked", self.go_folder)
        fix.put(title, 15, 15)
        fix.put(self.folder_name, 65, 10)
        fix.put(button_criar, 170, 45)
        self.folder_win.vbox.pack_start(fix)
        self.folder_win.show_all()
        return 0

    # prepara os dados para criar uma nova pasta
    def go_folder(self, widget):
        funcoes.create_folder(funcoes.get_local_path()+"/"+self.folder_name.get_text())
        self.folder_win.destroy()
        self.update_view(self.oculto)
        return 0

    # carrega janela para criacao de novo arquivo
    def action_file(self, widget):
        self.file_win = gtk.Dialog()
        self.file_win.set_title("Criar arquivo")
        self.file_win.set_size_request(400, 80)
        self.file_win.set_resizable(False)
        fix = gtk.Fixed()
        title = gtk.Label("Nome: ")
        self.file_name = gtk.Entry()
        self.file_name.set_size_request(300, 30)
        self.file_name.set_max_length(200)
        button_criar = gtk.Button("Criar")
        button_criar.set_size_request(60, 30)
        button_criar.connect("clicked", self.go_file)
        fix.put(title, 15, 15)
        fix.put(self.file_name, 65, 10)
        fix.put(button_criar, 170, 45)
        self.file_win.vbox.pack_start(fix)
        self.file_win.show_all()
        return 0

    # prepara os dados para a criacao de novo arquivo
    def go_file(self, widget):
        funcoes.create_file(funcoes.get_local_path()+"/"+self.file_name.get_text())
        self.file_win.destroy()
        self.update_view(self.oculto)
        return 0

    # metodo estatico para destruicao do dialogo principal
    @staticmethod
    def destroy(self):
        gtk.main_quit(self)

    # metodo estatico para iniciar o dialogo principal
    @staticmethod
    def main():
        gtk.main()


if __name__ == "__main__":
    main = MainWindow()
    print "Rodando"
    print "Possiveis saidas referentes a acesso negado, serao impressas abaixo."
    main.main()
    
