def filter_lines(file_or_path, search_words, stop_words):
    search_words = {word.lower() for word in search_words}
    stop_words = {word.lower() for word in stop_words}

    def process_lines(lines):
        for line in lines:
            words = set(line.strip().lower().split())
            if words & stop_words:
                continue
            if words & search_words:
                yield line.strip()

    if isinstance(file_or_path, str):
        with open(file_or_path, 'r', encoding='utf-8') as f:
            yield from process_lines(f)
    else:
        yield from process_lines(file_or_path)
