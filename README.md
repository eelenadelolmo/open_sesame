# Framenet annotation in English


### Installation

Clone the repo and execute the installation command:
`pip install -r requirements.txt`


### Usage

- English version: run `opensesame_en.py` and upload your files to http://0.0.0.0:5002/.
- Spanish version: run `opensesame.py` and upload your files to http://0.0.0.0:5002/.

    The only difference is the link for the next module: the annotation mapper in case for Spanish and the Thematic Progression annotator for English.

Annotator source: https://github.com/swabhs/open-sesame

- Accepted **input** files: txt files with one sentence per line and the name of the text plus an underscore and the number of sentence.

    Data format available as the output of the previous module for English (themmatic annotation module: http://0.0.0.0:5000/upload-grew-ann -- https://github.com/eelenadelolmo/TP_grammar) and Spanish (translation module: http://0.0.0.0:5001/ -- https://github.com/eelenadelolmo/neuraltrans).

- The **output** consists of one CoNLL file for every English sentence. Every file is named with the text id plus underscore plus the number of sentence.
 

____

 
This project is a part of a PhD thesis carried out at the Department of Linguistics of the Complutense University of Madrid (https://www.ucm.es/linguistica/grado-linguistica) and is supported by the ILSA (Language-Driven Software and Applications) research group (http://ilsa.fdi.ucm.es/).

The module will be publicly accessible for Spanish annotation from http://repositorios.fdi.ucm.es:5002/