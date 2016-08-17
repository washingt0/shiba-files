#!/usr/bin/env python
import os
import datetime


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


def get_info(diretorio, arquivo):
    path = diretorio + "/" + str(arquivo)
    info = os.stat(path)
    ac = get_time(info.st_atime)
    mo = get_time(info.st_mtime)
    cr = get_time(info.st_ctime)
    tamanho = format_size(info.st_size)
    permissions = get_permissions(oct(info.st_mode)[-3:])
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
        "tamanho": tamanho
    }
    return retorno

# a = os.getcwd()
# b = os.listdir(a)
# for i in b:
#     infos = get_info(a, i)
#     print infos["nome"]
#     print infos["uid"]
#     print infos["gid"]
#     print infos["data_ac"]
#     print infos["hora_ac"]
#     print infos["data_mo"]
#     print infos["hora_mo"]
#     print infos["data_cr"]
#     print infos["hora_cr"]
#     print infos["user_p"]
#     print infos["group_p"]
#     print infos["other_p"]
#     print infos["tamanho"]
#     print
