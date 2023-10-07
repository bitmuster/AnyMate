#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 21:47:33 2023

@author: micha
"""
import json

file = "template.json"
fileo = "template2.json"
with open(file) as fi:
    with open(fileo, "w+") as fo:
        j = json.loads(fi.read())
        #fo.write("{\n")
        #for r in j:
        #    fo.write(    "{\n")
        #    fo.write(f"    \"name\" : \"{r[0]}\"\n")
        #    fo.write(f"    \"nick\" : \"{r[1]}\"\n")
        #    fo.write(f"    \"color\" : \"{r[2]}\"\n")
        #    fo.write(f"    \"cmd\" : \"{r[3]}\"\n")
        #    fo.write(    "},\n")
        #fo.write("}\n")
        c = []
        for r in j:
            d = {"name":r[0], "nick":r[1], "color":r[2], "cmd":r[3]}
            c.append(d)
       
        z = json.dumps(c, indent="   ")
        fo.write(z)
        