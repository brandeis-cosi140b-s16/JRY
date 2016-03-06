Put the Preprocess folder in the toefl11_part folder, then run createXML.
It generates a XML file for each essay, and stores it in the <lang>_annotation folder.

The PART variable in createXML.py specifies which part of the corpus this program works on.
e.g. if PART = "dev", then the program checks the spelling of all the files in the dev folder