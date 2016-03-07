from lxml import etree
from Spelling.spellcheck import SpellChecker

#generate an xml with incorrect words tagged
class SpellXMLGen:
    def __init__(self, dtd, essay):
        self.rootname = dtd
        self.checker = SpellChecker(essay)
        self.errors = self.checker.getErrors()
        self._createStruct()
        self._createTags()

    def _createStruct(self):
        self.root = etree.Element(self.rootname)
        self.textNode = etree.SubElement(self.root, "TEXT")
        self.textNode.text = etree.CDATA(self.checker.getEssay())
        self.tagsNode = etree.SubElement(self.root, "TAGS")

    #generates a Misspelling tag
    def _createTag(self, word, n):
        spanstr = "{}~{}".format(word.getSpan()[0], word.getSpan()[1])
        etree.SubElement(self.tagsNode, "Misspelling", text=word.getText(),\
                         spans=spanstr, id="M"+str(n))

    def _createTags(self):
        i = 0
        for w in self.errors:
            self._createTag(w,i)
            i += 1

    def write(self, directory):
        tree = etree.ElementTree(self.root)
        tree.write(directory)


