# -*- coding:utf.8 -*-
from html.parser import HTMLParser
import pyphen


class StoryParser(HTMLParser):
    
    def __init__(self):
        self.reset_memory()
        super(StoryParser, self).__init__()
    
    def reset_memory(self):
        self.is_article = False
        self.result = []
    
    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.is_article = True
        elif tag == "p":
            if self.is_article:
                import ipdb;ipdb.set_trace()
        HTMLParser.handle_starttag(self, tag, attrs)
        
    def handle_endtag(self, tag):
        if tag == "article":
            self.is_article = False


source = ""

story_parser()
lang = pyphen.language_fallback('es_MX')
dic = pyphen.Pyphen(lang=lang)
dic.inserted