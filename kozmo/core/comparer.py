import difflib

def green(inp):
    return ('\033[92m%s\033[0m' % inp)

def comparer(original, new, inp):
    differences = []
    for text in difflib.unified_diff(original.split('\n'), new.split('\n')):
        if text[:3] not in ('+++', '---', '@@ '):
            if text.startswith('+'):
                differences.append((text[1:].replace(inp, green(inp))))
    if differences:
        return differences
    else:
        return False