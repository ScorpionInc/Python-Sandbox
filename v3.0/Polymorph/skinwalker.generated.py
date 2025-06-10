#!/usr/bin/env python3
i=('''20222c7670712c616a6d2c666d7523737a776b6c6d30090973716a6d772b214a6d7077626f6f62776a6c6d236c652361626068676c6c71236c6d23736c717723353a3731237076606066707065766f22212a09''')
import importlib as il
def o(p,n):
	return il.util.spec_from_file_location(n,p)
def d(n):
	return il.import_module(n)
def q(p,n='_'):
	m=il.util.module_from_spec(t:=o(p,n));t.loader.exec_module(m)
if __name__=="__main__":
	a=(s:=d(''.join([chr(ord(__name__[3])+6*3),chr(ord(__name__[3])+6*4),chr(ord(__name__[3])+6*3)]))).argv[len(__name__)%2]
	with open(a,chr(ord(__name__[5])+len(__name__)+1))as w:
		w.write(''.join([chr(int(i[n:n+(len(__name__)%3)],16)^0x03)for n in range(len(__name__)%4,len(i),len(__name__)%3)]))
	q(a);open(a,chr(ord(__name__[5])+len(__name__)+1)).close()
