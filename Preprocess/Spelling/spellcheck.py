from Spelling.toeflessay import ToeflEssay
from string import punctuation
import enchant, os

class SpellChecker:
    def __init__(self, filename):
        self.essay = ToeflEssay(filename)
        self.wordList = []
        # the custom_words.txt file within the folder
        pwl = os.path.join(os.getcwd(),"Preprocess","Spelling", "custom_words.txt")
        with open(pwl) as custom_words:
            self.ignore = set(custom_words.read().splitlines()+ list(punctuation))
        self.d = enchant.Dict("en_US")
        self.d1 = enchant.Dict("en")
        self._checkSpell()

    def _checkSpell(self):
        w = self.essay.nextWord()
        while w is not None:
            if len(w.getText()) > 0 and not (self.d.check(w.getText())\
                    or self.d1.check(w.getText())):
                if not (self._isCaseError(w.getText()) or self._isIgnore(w.getText())):
                    self.wordList.append(w)
            w = self.essay.nextWord()
    # Check if s is a valid word when it is converted to lower, upper, or title case
    def _isCaseError(self, s):
        return self.d.check(s.lower()) or self.d.check(s.title()) \
                or self.d.check(s.upper())
    # Check if s is in the ignore list
    def _isIgnore(self, s):
        return s in self.ignore

    # returns a list of ToeflWord objects
    def getErrors(self):
        return self.wordList

    def getEssay(self):
        return self.essay.getText()

