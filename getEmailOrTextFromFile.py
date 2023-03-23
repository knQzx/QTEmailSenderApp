from docx_parser import DocumentParser


class DataParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    @staticmethod
    def parse(file_path: str) -> str:
        if 'txt' in file_path:
            with open(file_path) as f:
                contents = f.read()
                return contents
        elif 'docx' in file_path:
            doc = DocumentParser(file_path)
            list_text = [item['text'] for _type, item in doc.parse()]
            return '\n'.join(list_text)

    def parsing_data(self):
        return self.parse(self.file_path)
