def format_docstring(text: str, indent: int = 4) -> str:
    if not text:
        return ""

    indent_str = " " * indent
    max_length = 88 - indent

    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_length and current_line:
            lines.append(indent_str + " ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += word_length

    if current_line:
        lines.append(indent_str + " ".join(current_line))

    result = [f'{indent_str}"""']
    result.extend(lines)
    result.append(f'{indent_str}"""')

    return "\n".join(result)
