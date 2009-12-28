import os

class ParserError(Exception): pass
class BadFilenameError(ParserError): pass

def get_file_contents(file):
    """Pulls each line out of a text file

    Returns a string.
    """

    if file[0] == '/':
        raise BadFilenameError

    sourceFile = open(file, 'r')
    result = sourceFile.read()
    sourceFile.close()

    return result
