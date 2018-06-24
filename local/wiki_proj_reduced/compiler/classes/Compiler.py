#!/usr/bin/env python
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import json
from .Node import *
from .Utils import *

def render_content_with_text(key, value):
    if FILL_WITH_RANDOM_TEXT:
        if key.find("btn") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text())
        elif key.find("title") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, Utils.get_random_text(length_text=5, space_number=0))
        elif key.find("text") != -1:
            value = value.replace(TEXT_PLACE_HOLDER,
                                  Utils.get_random_text(length_text=56, space_number=7, with_upper_case=False))
    return value

def sanitize_data(record, singular_token_path):       
        singular_token_data = read_file(singular_token_path)
        record = record.replace('\n',' ')
        record = ' '.join(record.split(' '))
        singular_token_data = ' '.join(singular_token_data.split(' '))
        tokens = record.split(' ')
        singular_tokens = singular_token_data.split(' ')
        sanitized_string = ''
        for token in tokens:
            #print("token> " + token)
            token = token.replace(' ', '').replace('\n','')
            if any(singular_token in token for singular_token in singular_tokens):
                #print('inside')
                sanitized_string = sanitized_string + ' ' + token + ' {}'
            else:
                sanitized_string = sanitized_string + ' ' + token
        sanitized_string = '{ body { header {} ' + sanitized_string + '}}'     
        print(sanitized_string)   
        return sanitized_string

def read_file(file_path):
    file2 = open(file_path, 'r')
    content = file2.read();
    file2.close()
    return content

class Compiler:
    def __init__(self, dsl_mapping_file_path):
        with open(dsl_mapping_file_path) as data_file:
            self.dsl_mapping = json.load(data_file)

        self.opening_tag = self.dsl_mapping["opening-tag"]
        self.closing_tag = self.dsl_mapping["closing-tag"]
        self.content_holder = self.opening_tag + self.closing_tag

        self.root = Node("body", None, self.content_holder)

    def compile(self, tokens, output_file_path, dsl_singular_tag_file_path):
        dsl_file = sanitize_data(tokens, dsl_singular_tag_file_path)
        tokens
        
        #Parse fix
        dsl_file = dsl_file[1:-1]
        dsl_file = ' '.join(dsl_file)
        dsl_file = dsl_file.replace('{', '{8').replace('}', '8}8')
        dsl_file = dsl_file.replace(' ', '')
        dsl_file = dsl_file.split('8')
        dsl_file = list(filter(None, dsl_file))
        #End Parse fix
        
        current_parent = self.root
        
        for token in dsl_file:
            token = token.replace(" ", "").replace("\n", "")
           
            if token.find(self.opening_tag) != -1:
                token = token.replace(self.opening_tag, "")

                element = Node(token, current_parent, self.content_holder)
                current_parent.add_child(element)
                current_parent = element
            elif token.find(self.closing_tag) != -1:
                current_parent = current_parent.parent
            else:
                tokens = token.split(",")
                for t in tokens:
                    element = Node(t, current_parent, self.content_holder)
                    current_parent.add_child(element)

        output_html = self.root.render(self.dsl_mapping, rendering_function=render_content_with_text)
        if output_html is None:
            return "Parsing Error"
        
        with open(output_file_path, 'w') as output_file:
           output_file.write(output_html)
        return output_html
    
    
FILL_WITH_RANDOM_TEXT = True
TEXT_PLACE_HOLDER = "[]"