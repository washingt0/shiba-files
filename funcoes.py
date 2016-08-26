#!/usr/bin/env python
import os
import datetime
import shutil

def get_time(time):
    date = datetime.datetime.fromtimestamp(time)
    d = date.day
    mo = date.month
    y = date.year
    h = date.hour
    m = date.minute
    s = date.second
    datetime_set = ["{}/{}/{}".format(str(d).zfill(2), str(mo).zfill(2), y),
                    "{}:{}:{}".format(str(h).zfill(2), str(int(m)).zfill(2), str(int(s)).zfill(2))]
    return datetime_set


def get_permissions(modo):
    permissoes = {
        "0": "---",
        "1": "--x",
        "2": "-w-",
        "3": "-wx",
        "4": "r--",
        "5": "r-x",
        "6": "rw-",
        "7": "rwx"
    }
    perm = []
    for i in modo:
        perm.append(permissoes[i])
    return perm


def format_size(tamanho):
    pb = 1125899906842624.0
    tb = 1099511627776.0
    gb = 1073741824.0
    mb = 1048576.0
    kb = 1024.0
    if tamanho > pb:
        retorno = str(round((tamanho/pb), 2)) + " PB"
    elif tamanho > tb:
        retorno = str(round((tamanho / tb), 2)) + " TB"
    elif tamanho > gb:
        retorno = str(round((tamanho / gb), 2)) + " GB"
    elif tamanho > mb:
        retorno = str(round((tamanho / mb), 2)) + " MB"
    elif tamanho > kb:
        retorno = str(round((tamanho / kb), 2)) + " KB"
    else:
        retorno = str(round(tamanho, 2)) + " B"
    return retorno


def get_info(diretorio, type):
    info = os.stat(diretorio)
    ac = get_time(info.st_atime)
    mo = get_time(info.st_mtime)
    cr = get_time(info.st_ctime)
    permissions = get_permissions(oct(info.st_mode)[-3:])
    permissions2 = oct(info.st_mode)[-3:]
    if os.path.isfile(diretorio):
        tipo = "Arquivo"
        tamanho = format_size(info.st_size)
    else:
        tipo = "Pasta"
        if type == 1:
            tamanho = format_size(get_size_folder(diretorio))
        else:
            tamanho = format_size(info.st_size)
    arquivo = ''
    url = diretorio.split('/')
    for i in url:
        arquivo = i
    retorno = {
        "nome": arquivo,
        "uid": info.st_uid,
        "gid": info.st_gid,
        "data_ac": ac[0],
        "hora_ac": ac[1],
        "data_mo": mo[0],
        "hora_mo": mo[1],
        "data_cr": cr[0],
        "hora_cr": cr[1],
        "user_p": permissions[0],
        "group_p": permissions[1],
        "other_p": permissions[2],
        "tamanho": tamanho,
        "tipo": tipo,
        "perm": permissions2
    }
    return retorno


def get_local_path():
    return os.getcwd()


def ir_acima():
    os.chdir("..")
    return get_local_path()


def ir_para(diretorio):
    if os.path.isfile(diretorio):
        pass
    else:
        os.chdir(diretorio)
    return get_local_path()


def get_list(diretorio):
    if os.path.exists(diretorio):
        lista = os.listdir(diretorio)
        return lista
    else:
        return -1


def existe(diretorio):
    return os.path.exists(diretorio)


def get_size_folder(diretorio):
    start_path = diretorio
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.stat(fp).st_size
            except Exception as e:
                print "Nao foi possivel realizar a operacao"
                print e
    return total_size


def colar(caminho):
    if caminho is None:
        return 0
    try:
        if os.path.isfile(caminho):
            shutil.copy(caminho, get_local_path()+"/")
        else:
            lnome = caminho.split("/")
            shutil.copytree(caminho, get_local_path()+"/"+lnome[-1])
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def excluir(caminho):
    try:
        if os.path.isfile(caminho):
            os.remove(caminho)
        elif os.path.islink(caminho):
            os.unlink(caminho)
        else:
            shutil.rmtree(caminho)
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def alter_uid(caminho, uid):
    try:
        os.chown(caminho, int(uid), -1)
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def alter_gid(caminho, gid):
    try:
        os.chown(caminho, -1, int(gid))
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def alter_perm(caminho, perms):
    try:
        os.chmod(caminho, int(perms))
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def create_symlink(origem, nome):
    try:
        os.symlink(origem, nome)
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0


def create_folder(caminho):
    try:
        os.mkdir(caminho)
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e


def create_file(caminho):
    try:
        arquivo = open(caminho, 'a')
        arquivo.close()
    except Exception as e:
        print "Nao foi possivel realizar a operacao"
        print e
    return 0
