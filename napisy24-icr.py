from os import walk
import os

out_encoding = "utf-8-sig"
out_dir = "icr-out"

char_map = {
    "¹": "ą",
    "æ": "ć",
    "ê": "ę",
    "³": "ł",
    "ñ": "ń",
    "œ": "ś",
    "¿": "ż",
    "Ÿ": "ź",
    "Œ": "Ś",
    "Ê": "Ę",
    "¯": "Ż",
    "£": "Ł",
    "¥": "Ą",
    "Æ": "Ć",
    "": "Ź",
    "Ñ": "Ń",
}


allowed_extensions = {
    'txt', 'srt',
}


def on_start():
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)


def get_fixed_text(text):
    for invalid_char, valid_char in char_map.items():
        text = text.replace(invalid_char, valid_char)
    return text


def has_allowed_ext(file_name: str):
    return any(file_name.endswith(f'.{ext}') for ext in allowed_extensions)


if __name__ == '__main__':
    on_start()

    _, _, filenames = next(walk("."))

    script_name = os.path.basename(__file__)
    filenames.remove(script_name)

    changed_count = 0

    for filename in filenames:
        if not has_allowed_ext(filename):
            continue

        has_changed = False
        dest_file = os.path.join(out_dir, filename)
        try:
            with open(filename, "r", encoding="utf-8") as in_file:
                with open(dest_file, "w", encoding=out_encoding) as out_file:
                    for line in in_file:
                        valid_line = get_fixed_text(line)
                        out_file.write(valid_line)
                        if line != valid_line:
                            has_changed = True
        except UnicodeDecodeError:
            print(f"Could not process file '{filename}' since it is not utf-8 encoded")
            if os.path.isfile(dest_file):
                os.remove(dest_file)
        if has_changed is True:
            changed_count += 1

    print("processed files: %s" % len(filenames))
    print("affected files: %s" % changed_count)
