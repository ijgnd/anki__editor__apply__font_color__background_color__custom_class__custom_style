import re

def get_base_top(editor, match):
    matches = []
    query = re.escape(match.string[:match.start()]) + r'(\d+)' + re.escape(match.string[match.end():])

    for name, item in editor.note.items():
        matches.extend(re.findall(query, item))

    values = [0]
    values.extend([int(x) for x in matches])

    top = max(values)
    return top

def get_top_index(editor, match):
    base_top = get_base_top(editor, match)
    top = base_top + 1 if base_top == 0 else base_top

    return str(top)

def incremented_index(editor, match):
    base_top = get_base_top(editor, match)
    top = base_top + 1

    return str(top)

escape_seqs = {
    '%': lambda _editor, _match: '%',
    't': get_top_index,
    'i': incremented_index,
}
