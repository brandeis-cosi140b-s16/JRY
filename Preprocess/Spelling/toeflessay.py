# Reader class for a Toefl essay file
class ToeflEssay:

    def __init__(self, fName):
        with open(fName) as f:
            self.text = f.read()
            self.pos = 0
            self.size = len(self.text)

    def resetPos(self):
        self.pos = 0

    def _isEOF(self):
        return self.pos >= self.size

    def nextChar(self):
        if not self._isEOF():
            self.pos += 1
            return self.text[self.pos - 1]
        else:
            return None

    def nextWord(self):
        word = ""
        start = self.pos
        while not self._isEOF():
            c = self.nextChar()
            if not (c.isspace() or c == "-"):
                word += c
            else:
                return ToeflWord(word, (start, self.pos - 1))
        return None

    def getText(self):
        return self.text

# An object that represents a word in the essay
class ToeflWord:
        def __init__(self, text, span):
            self.text = text
            self.span = span

        def getText(self):
            return self.text

        # returns the spans of the word
        def getSpan(self):
            return self.span


