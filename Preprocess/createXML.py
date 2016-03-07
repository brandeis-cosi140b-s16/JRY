from Spelling.generateXML import SpellXMLGen
import os, re

#edit PART to change which part of the corpus this script runs on
PART = "dev"
FILE_PATTERN = r"^\d+\.txt$"
#name of the DTD file
DTD_NAME = "L1ML_v1.0"
file_matcher = re.compile(FILE_PATTERN)

def getFolders(part):
   return os.listdir(part)

# creates a <lang>_annoation folder in each <lang> folder
def createDirectory(part, lang):
    p = os.path.join(".", part, lang, lang+"_annotation")
    if not os.path.exists(p):
        os.makedirs(p)
#returns a list of essay filenames within lang of part
def getEssays(part, lang):
    p = os.path.join(".", part, lang)
    fileList = os.listdir(p)
    fileList = [f for f in fileList if file_matcher.match(f)]
    return fileList

# writes the xml to the folder
def createAnnotation(part, lang, dtd, filename):
    fpath = os.path.join(part, lang, filename)
    g = SpellXMLGen(dtd, fpath)
    p = os.path.join(".", part, lang, lang+"_annotation")
    assert os.path.exists(p)
    f = os.path.join(p, filename+".xml")
    g.write(f)



if __name__ == "__main__":
    os.chdir("..")
    langs = getFolders(PART)
    for lang in langs:
        createDirectory(PART, lang)
        for f in getEssays(PART, lang):
            createAnnotation(PART,lang,DTD_NAME, f)
