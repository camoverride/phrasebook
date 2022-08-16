"""
This module is resposible for converting yaml pages into HTML.

This needs to be run manually if you want to include changes in a commit.

TODO: automate this process during the jekyll build!

This takes yaml files from the `___pages` directory and writes html docs
in the `docs` directory. NOTE: these files need to have their front matter
manually edited to include the title and page order.

TODO: automate this process too
"""

import jinja2
import yaml 
from collections import ChainMap


# Define functions for parsing yaml file.
class Phrase:
    """
    A Phrase object has the obligatory attributes `phrase` and `ortho`
    and can also have `ipa`, `comment`, and multiple `audio` files.
    """
    def __init__(self, phrase, ortho):
        self.phrase = phrase
        self.ortho = ortho
        self.ipa = None
        self.comment = None
        self.audio_recordings = []


def parse_yaml(phrases):
    """
    Parse an incoming yaml document. Re-define each phrase
    as a Phrase object.
    """
    phrase_list = []
    title = phrases["title"]
    description = phrases["description"]
    # Remove these from phrases, because they're not actually phrases
    phrases.pop("title")
    phrases.pop("description")

    for phrase in phrases.items():
        _phrase = phrase[0]
        # convert list of dicts to dict
        _data = dict(ChainMap(*phrase[1]))
        # print(_data)

        p = Phrase(_phrase, _data["ortho"])
        if "ipa" in _data:
            p.ipa = _data["ipa"]
        if "comment" in _data:
            p.comment = _data["comment"]
        if "audio" in _data:
            p.audio = _data["audio"]
    
        phrase_list.append(p)

    return title, description, phrase_list


def render_pages(yaml_pages, template, output_dir):
    """
    Takes a list of pages (yaml format) and inserts the information into
    a given template.
    """
    # Open and parse yaml file.
    for yaml_page in yaml_pages:
        with open(yaml_page) as f: 
            phrases = yaml.safe_load(f)

        title, description, parsed_phrases = parse_yaml(phrases)


        # Load the template file (.html) that will be populated with
        # information from a .yaml file
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)

        template = templateEnv.get_template(template)

        # Pass all information to the .html document.
        templateVars = {"title" : title,
                        "page_description" : description,
                        "phrases" : parsed_phrases}

        outputText = template.render(templateVars)

        output_file_name = output_dir + "/" + yaml_page.split("/")[-1].split(".")[0] + ".html"

        with open(output_file_name, "w") as p:
            p.write(outputText)



PAGES_TO_RENDER = ["./___pages/greetings.yaml", "./___pages/colors.yaml", "./___pages/numbers.yaml"]

render_pages(PAGES_TO_RENDER, template="./___page_template.html", output_dir="docs")
