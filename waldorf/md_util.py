CSS_HEAD = """<head>
<link rel="stylesheet" type="text/css" href="{}">
</head>
"""

import markdown


class Element(object):
    def render(self):
        pass


class Text(Element):
    def __init__(self, text):
        self.text = text

    def render(self):
        return self.text + '\n'


class Head(Element):
    def __init__(self, lvl: int, msg: str):
        self.lvl = lvl
        self.msg = msg

    def render(self):
        return '#' * self.lvl + ' ' + self.msg + '\n'


class Table(Element):
    def __init__(self):
        self.objects = {}

    def set_head(self, head: list):
        self.head = head

    def update_object(self, key: str, properties: dict):
        self.objects.update({key: properties})

    def remove_object(self, key):
        if key in self.objects:
            self.objects.pop(key)

    def to_dict(self):
        return {
            'head': self.head,
            'objects': self.objects
        }

    def render(self):
        md = 'Index|' + '|'.join(self.head) + '\n'
        md += '|'.join(['-'] * (len(self.head) + 1)) + '\n'
        for idx, obj in enumerate(self.objects.values()):
            attr = []
            for h in self.head:
                attr.append(str(obj[h]))
            md += str(idx + 1) + '|' + '|'.join(attr) + '\n'
        return md


class MarkdownGenerator(object):
    def __init__(self):
        self.elements = []

    def add_element(self, elem):
        self.elements.append(elem)

    def del_element(self, elem):
        self.elements.remove(elem)

    def source(self):
        md = ''
        for elem in self.elements:
            md += elem.render() + '\n'
        return md

    def render(self, css=None):
        if css:
            head = CSS_HEAD.format(css)
        else:
            head = ''
        html = head + markdown.markdown(
            self.source(), extensions=['markdown.extensions.extra'])
        return html
