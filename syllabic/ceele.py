# -*- coding:utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os

class CeeleGenerator(object):
    
    def __init__(self, corpus_path, results_path, conserve_subsegments=True):
        for root, dirs, files in os.walk(corpus_path):
            for filepath in files:
                try:
                    tree = ET.ElementTree(file=root + "/" + filepath)
                except:
                    continue
                tree_root = tree.getroot()
                text = ""
                for child in tree_root:
                    if 'cuerpo' in child.tag:
                        tokens = []
                        for grand_child in child:
                            if 'g' in grand_child.tag:
                                all = [g for g in grand_child.itertext()]
                                if conserve_subsegments:
                                    i = 0
                                    segments = []
                                    for gg_child in grand_child:
                                        if "hiposeg" in gg_child.tag or\
                                           "hiperseg" in gg_child.tag:
                                            segments.append(i)
                                        i += 1
                                    if segments != []:
                                        last_segment = 0
                                        for segment in segments:
                                            tokens.append("".join(all[last_segment:segment]))
                                            last_segment = segment
                                        tokens.append("".join(all[last_segment:]))
                                    else:
                                        tokens.append("".join(all))
                                else:
                                    tokens.append("".join(all))
                                
                        if len(tokens)>0:
                            if len(tokens) == 1:
                                text += tokens[0]
                            else:
                                text += " ".join(tokens)
                with open(results_path + filepath.replace(".xml", 
                                                          ".txt"), "w") as f:
                    f.write(text)
                