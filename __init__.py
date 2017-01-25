
import os

from cleaner import StoryParser
from syllabic import SyllableStatistics


source_dir = "./corpus/raw/"
res_dir = "./corpus/clean/"
generate_corpus = False

if generate_corpus: # Corpus of children stories
    story_parser = StoryParser()
    for root, _, files in os.walk(source_dir):
        for fl in files:
            with open(root + "/" + fl, "r") as f:
                try:
                    content = f.read()
                except:
                    continue
            
            story_parser.feed(content)
            
            res_path = root.replace("raw", "clean")
            if "." in fl: # no es folder
                temp_fname = "".join(fl.split(".")[0:-1]) + ".txt"
                res_path += temp_fname
            elif "." in root:
                res_path = "./" + "".join(res_path.split(".")[0:-1]
                                          ) + "-" + fl + ".txt"
            
            with open(res_path, "w") as f:
                f.write(story_parser.title)
                f.write("\n\n")
                for line in story_parser.result:
                    f.write("\n\n")
                    f.write(line)
                f.flush()
                
            story_parser.reset()

stats = SyllableStatistics(res_dir)