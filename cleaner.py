# -*- coding:utf-8 -*-
from html.parser import HTMLParser


class StoryParser(HTMLParser):
    
    def reset(self):
        self.is_article = False
        self.is_p = False
        self.is_title = False
        self.title = ""
        self.result = []
        HTMLParser.reset(self)    
    
    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.is_article = True
        elif tag == "p":
            if len(attrs) == 0:
                self.is_p = True
        else:
            for attr in attrs:
                key, val = attr 
                if key == 'class' and val == 'title':
                    self.is_title = True
        
        HTMLParser.handle_starttag(self, tag, attrs)
    
    def handle_data(self, data):
        if self.is_article:
            if self.is_title:
                self.is_title = False
                self.title = data
                print(self.title)
            elif self.is_p:
                stripped_data = data.strip()
                if "adsbygoogle" in stripped_data:
                    pass
                elif "Páginas:" in stripped_data:
                    pass
                elif "1" == stripped_data \
                  or "2" == stripped_data \
                  or "3" == stripped_data \
                  or "4" == stripped_data:
                    pass
                else:
                    if stripped_data != '':
                        self.result.append(data.strip())
                    # print(stripped_data)
    
    def handle_endtag(self, tag):
        if tag == "article":
            self.is_article = False
        if tag == "p":
            self.is_p = False