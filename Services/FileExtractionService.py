import textract
import re


class TextExtract:
    def extract(self, file):
        text = textract.process(file)
        text = text.decode('utf-8')
# Decodes text
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
# Removes \n \r \t
        text = re.sub(' +', ' ', text)
# Removes extra white spaces
        return text
