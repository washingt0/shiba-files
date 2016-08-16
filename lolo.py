#!/usr/bin/env python
import os
path = os.getcwd()
path = path + "/"
a = os.listdir(path)
a.sort()
for i in a:
	b = os.stat(path+i)
	print("Nome: " + i)
	print("ID do Proprietario: " + str(b.st_uid) )
	print("ID do Grupop: " + str(b.st_gid) )
	if os.path.isfile(path+i):
		print "Arquivo"
		print("Tamanho: " + str(b.st_size/1024.0) + "kb")
	else:
		print "Pasta"
		print("Tamanho: " + str(b.st_size/1024.0) + "kb")
	print