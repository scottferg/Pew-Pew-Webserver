import sys
import unittest

sys.path.append('..')
import fileParser

class basicParsing(unittest.TestCase):
    knownResult = """<html>
    <body>
        LOL INTERNET
    </body>
</html>
"""

    def testCorrectParsing(self):
        result = fileParser.getFileContents('DUMMY.html')

        self.assertEquals(self.knownResult, result)

class badParserInput(unittest.TestCase):

    def testBadInput(self):
        self.assertRaises(fileParser.BadFilenameError, fileParser.getFileContents, '/DUMMY.html')

if __name__ == '__main__':
    unittest.main()
