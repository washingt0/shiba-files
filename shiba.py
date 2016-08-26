#! /usr/bin/python
import gtk
import funcoes


class MainWindow:
    def __init__(self):
        self.oculto = True
        self.path = funcoes.get_local_path()
        self.old_path = []
        self.files = {}
        self.copy_uri = None
        self.crop = False
        self.window = gtk.Dialog()
        self.window.set_title("Shiba Files")
        self.window.set_size_request(800, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.fixed = gtk.Fixed()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600, 500)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.path_bar = gtk.Entry()
        self.path_bar.set_size_request(530, 40)
        self.path_bar.set_text(self.path)
        self.fixed.put(self.path_bar, 190, 15)

        self.list = gtk.ListStore(str, str, str, str, str)
        self.update_view(self.oculto)
        self.files_treeview = gtk.TreeView()
        self.files_treeview.set_model(self.list)

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

        self.button_acima = gtk.Button("Acima")
        self.button_voltar = gtk.Button("Voltar")
        self.button_ir = gtk.Button("Ir")
        self.button_copiar = gtk.Button("Copiar")
        self.button_colar = gtk.Button("Colar")
        self.button_recortar = gtk.Button("Recortar")
        self.button_excluir = gtk.Button("Excluir")
        self.button_propriedades = gtk.Button("Propriedades")
        self.button_symlink = gtk.Button("Criar Link")
        self.button_novo = gtk.Button("Novo Arquivo")
        self.button_pasta = gtk.Button("Nova Pasta")
        self.button_oculto = gtk.Button("Mostrar Ocultos")

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

        self.button_acima.connect("clicked", self.action_up)
        self.button_voltar.connect("clicked", self.action_back)
        self.button_ir.connect("clicked", self.action_go)
        self.button_oculto.connect("clicked", self.action_oculto)
        self.button_copiar.connect("clicked", self.action_copy)
        self.button_colar.connect("clicked", self.action_paste)
        self.button_recortar.connect("clicked", self.action_crop)
        self.button_excluir.connect("clicked", self.action_delete)
        self.button_propriedades.connect("clicked", self.action_properties)

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

        self.files_treeview.show()
        self.scrolled_window.add(self.files_treeview)

        self.selected = self.files_treeview.get_selection()
        self.selected.set_mode(gtk.SELECTION_SINGLE)
        self.selected.select_path(0)

        self.window.vbox.pack_start(self.fixed)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)


    def update_view(self, oculto):
        self.list.clear()
        self.files.clear()
        local = funcoes.get_local_path()
        lista = funcoes.get_list(local)
        self.path_bar.set_text(local)
        for i in lista:
            if funcoes.existe(local + "/" + i):
                self.files[i] = funcoes.get_info(local + "/" + i)
        for j, i in self.files.iteritems():
            if oculto and i["nome"][0] == '.':
                pass
            else:
                self.list.append([i["nome"], i["tamanho"], i["user_p"] + i["group_p"] + i["other_p"], i["uid"],
                                  i["tipo"]])

    def action_up(self, widget):
        self.old_path.append(self.path)
        self.path = funcoes.ir_acima()
        self.update_view(self.oculto)

    def action_back(self, widget):
        try:
            self.path = self.old_path.pop()
            funcoes.ir_para(self.path)
            self.update_view(self.oculto)
        except ValueError:
            pass

    def action_go(self, widget):
        self.old_path.append(self.path)
        self.path = self.path_bar.get_text()
        funcoes.ir_para(self.path)
        self.update_view(self.oculto)

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

    def get_selected(self):
        try:
            selec = self.selected.get_selected()
            selecionado = self.list.get_value(selec[1], 0)
        except ValueError:
            selecionado = None
        return selecionado

    def action_copy(self, widget):
        self.copy_uri = funcoes.get_local_path() + "/" + self.get_selected()

    def action_crop(self, widget):
        self.crop = True
        self.copy_uri = funcoes.get_local_path() + "/" + self.get_selected()

    def action_paste(self, widget):
        funcoes.colar(self.copy_uri)
        if self.crop:
            funcoes.excluir(self.copy_uri)
            self.crop = False
        self.update_view(self.oculto)
        return 0

    def action_delete(self, widget):
        funcoes.excluir(funcoes.get_local_path() + "/" + self.get_selected())
        self.update_view(self.oculto)

    def action_properties(self, widget):
        selecionado = self.get_selected()
        info = funcoes.get_info(funcoes.get_local_path()+"/"+selecionado)
        if selecionado is None:
            pass
        else:
            win = gtk.Dialog()
            win.set_title("Propriedades")
            win.set_size_request(350, 400)
            win.set_resizable(False)

            fix = gtk.Fixed()
            tnome = gtk.TextBuffer()
            tnome.set_text("Nome: ")
            ttamanho = gtk.TextBuffer()
            ttamanho.set_text("Tamanho: ")
            tuserid = gtk.TextBuffer()
            tuserid.set_text("UID: ")
            tgroupid = gtk.TextBuffer()
            tgroupid.set_text("GID: ")
            tpermissoes = gtk.TextBuffer()
            tpermissoes.set_text("Permissoes: ")
            tdtcriacao = gtk.TextBuffer()
            tdtcriacao.set_text("Data de Criacao: ")
            tdtacesso = gtk.TextBuffer()
            tdtacesso.set_text("Data de Acesso: ")
            tdtmod = gtk.TextBuffer()
            tdtmod.set_text("Data de Modificacao: ")

            vnome = gtk.TextView(tnome)
            vnome.set_editable(False)
            vtamanho = gtk.TextView(ttamanho)
            vtamanho.set_editable(False)
            vuserid = gtk.TextView(tuserid)
            vuserid.set_editable(False)
            vgroupid = gtk.TextView(tgroupid)
            vgroupid.set_editable(False)
            vpermissoes = gtk.TextView(tpermissoes)
            vpermissoes.set_editable(False)
            vdtcriacao = gtk.TextView(tdtcriacao)
            vdtcriacao.set_editable(False)
            vdtacesso = gtk.TextView(tdtacesso)
            vdtacesso.set_editable(False)
            vdtmod = gtk.TextView(tdtmod)
            vdtmod.set_editable(False)

            cnome = gtk.TextBuffer()
            cnome.set_text(info["nome"])
            ctamanho = gtk.TextBuffer()
            ctamanho.set_text(info["tamanho"])
            cuserid = gtk.TextBuffer()
            cuserid.set_text(str(info["uid"]))
            cgroupid = gtk.TextBuffer()
            cgroupid.set_text(str(info["gid"]))
            cpermissoes = gtk.TextBuffer()
            cpermissoes.set_text(info["user_p"]+info["group_p"]+info["other_p"])
            cdtcriacao = gtk.TextBuffer()
            cdtcriacao.set_text(info["data_cr"]+"  "+info["hora_cr"])
            cdtacesso = gtk.TextBuffer()
            cdtacesso.set_text(info["data_ac"]+"  "+info["hora_ac"])
            cdtmod = gtk.TextBuffer()
            cdtmod.set_text(info["data_mo"]+"  "+info["hora_mo"])

            vcnome = gtk.TextView(cnome)
            vcnome.set_editable(False)
            vctamanho = gtk.TextView(ctamanho)
            vctamanho.set_editable(False)
            vcuserid = gtk.TextView(cuserid)
            vcuserid.set_editable(False)
            vcgroupid = gtk.TextView(cgroupid)
            vcgroupid.set_editable(False)
            vcpermissoes = gtk.TextView(cpermissoes)
            vcpermissoes.set_editable(False)
            vcdtcriacao = gtk.TextView(cdtcriacao)
            vcdtcriacao.set_editable(False)
            vcdtacesso = gtk.TextView(cdtacesso)
            vcdtacesso.set_editable(False)
            vcdtmod = gtk.TextView(cdtmod)
            vcdtmod.set_editable(False)

            fix.put(vnome, 30, 20)
            fix.put(vtamanho, 30, 50)
            fix.put(vuserid, 30, 80)
            fix.put(vgroupid, 30, 110)
            fix.put(vpermissoes, 30, 140)
            fix.put(vdtcriacao, 30, 170)
            fix.put(vdtmod, 30, 200)
            fix.put(vdtacesso, 30, 230)
            fix.put(vcnome, 180, 20)
            fix.put(vctamanho, 180, 50)
            fix.put(vcuserid, 180, 80)
            fix.put(vcgroupid, 180, 110)
            fix.put(vcpermissoes, 180, 140)
            fix.put(vcdtcriacao, 180, 170)
            fix.put(vcdtmod, 180, 200)
            fix.put(vcdtacesso, 180, 230)
            win.vbox.pack_start(fix)
            win.show_all()


    @staticmethod
    def destroy(self):
        gtk.main_quit(self)

    @staticmethod
    def main():
        gtk.main()


if __name__ == "__main__":
    main = MainWindow()
    main.main()
