# -*- coding:utf-8 -*-

import os

from cleaner import StoryParser
from syllabic import SyllableStatistics
from syllabicator import Silabicador
from ngram import BiGram
from ceele import CeeleGenerator


source_dir = "../corpus/raw/"
source_dir_ceele = "../corpus/ceele"
res_dir = "../corpus/clean/"
res_dir_ceele = "../corpus/ceele_clean/"
generate_corpus = False
generate_ceele = False

if generate_corpus: # Generate corpus of children stories
    story_parser = StoryParser() # Get the corpus parser 
    for root, _, files in os.walk(source_dir): # Read all raw files
        for fl in files:
            with open(root + "/" + fl, "r") as f:
                try:
                    content = f.read()
                except:
                    continue
            
            # Parse the content of the current file
            story_parser.feed(content)
            
            # Save results in a "clean" folder
            res_path = root.replace("raw", "clean")
            if "." in fl: # no es folder
                temp_fname = "".join(fl.split(".")[0:-1]) + ".txt"
                res_path += temp_fname
            elif "." in root:
                res_path = "./" + "".join(res_path.split(".")[0:-1]
                                          ) + "-" + fl + ".txt"
            
            with open(res_path, "w") as f:
                f.write(story_parser.title)
                for line in story_parser.result:
                    f.write(" ")
                    f.write(line)
                f.flush()
                
            # Reset the parser before continuing
            story_parser.reset()

if generate_ceele:
    celegent = CeeleGenerator(source_dir_ceele,
                              res_dir_ceele)

syl = Silabicador()
result = syl("querida")
print("%s" % result)
result = syl("alquimista")
print("%s" % result)
result = syl("guey")
print("%s" % result)
result = syl("cayn")
print("%s" % result)
result = syl("adherir")
print("%s" % result)
result = syl("hembra")
print("%s" % result)
result = syl("perro")
print("%s" % result)
result = syl("llevar")
print("%s" % result)
result = syl("carretera")
print("%s" % result)
result = syl("chicharrón")
print("%s" % result)
result = syl("transgredir")
print("%s" % result)
result = syl("instrucción")
print("%s" % result)
result = syl("extrañamiento")
print("%s" % result)
result = syl("entrega")
print("%s" % result)
result = syl("espronceda")
print("%s" % result)
result = syl("institución")
print("%s" % result)
result = syl("constitución")
print("%s" % result)
result = syl("premiación")
print("%s" % result)
result = syl("transgresión")
print("%s" % result)
result = syl("playas")
print("%s" % result)
result = syl("playa")
print("%s" % result)
result = syl("padres")
print("%s" % result)
result = syl("calcificación")
print("%s" % result)
result = syl("gimnasio")
print("%s" % result)
result = syl("acróstico")
print("%s" % result)
result = syl("atraen")
print("%s" % result)
result = syl("seca")
print("%s" % result)
result = syl("salón")
print("%s" % result)
result = syl("mano")
print("%s" % result)
result = syl("pena")
print("%s" % result)
result = syl("supercalifragilisticoespiralidoso")
print("%s" % result)

# Send the complete corpus to analysis
#stats = SyllableStatistics(res_dir)
stats2 = SyllableStatistics(res_dir_ceele)
ngram = BiGram(res_dir, with_white_space=True)
ngram2 = BiGram(res_dir_ceele, with_white_space=True)
import ipdb;ipdb.set_trace()