def indent(elem, level=0, tabs=False):
    """ https://stackoverflow.com/a/33956544/4796605 """
    if tabs:
        spacer = "\t"
    else:
        spacer = "  "
    i = "\n" + level * spacer
    if len(elem):
        if not elem.text or not elem.text.strip():
            if level == 0:
                elem.text = '\n' + i + spacer
            else:
                elem.text = i + spacer
        if not elem.tail or not elem.tail.strip():
            if level <= 1:
                elem.tail = i + i
            else:
                elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def clean_and_indent(root, level=0, tabs=False):
    """ Extensible clean function """
    indent(root, level, tabs)
