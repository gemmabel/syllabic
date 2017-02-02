
import os

from cleaner import StoryParser
from syllabic import SyllableStatistics
from syllabificator import Silabicador


source_dir = "./corpus/raw/"
res_dir = "./corpus/clean/"
generate_corpus = False

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

syl = Silabicador()
result = syl("património")
print(result)
import ipdb;ipdb.set_trace()
# Send the complete corpus to analysis
#stats = SyllableStatistics(res_dir)