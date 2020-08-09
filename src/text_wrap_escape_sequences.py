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

def fill_matching_field(indexer):
    def get_value(editor, match):
        current_index = indexer(editor, match)

        for index, (name, item) in enumerate(editor.note.items()):
            match = re.search(r'\d+$', name)

            if match and match[0] == current_index and len(item) == 0:
                js = (
                    f'pycmd("key:{index}:{editor.note.id}:active");'
                    f'document.querySelector("#f{index}").innerHTML = "active";'
                )

                editor.web.eval(js)

        return current_index

    return get_value

escape_seqs = {
    '%': lambda _editor, _match: '%',
    't': get_top_index,
    'u': fill_matching_field(get_top_index),
    'i': incremented_index,
    'j': fill_matching_field(incremented_index),
}
