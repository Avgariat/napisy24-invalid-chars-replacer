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

if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    _, _, filenames = next(walk("."))
    filenames.remove(script_name)

    changed_count = 0

    for filename in filenames:
        has_changed = False
        with open(filename, "r", encoding="utf-8") as in_file:
            if not os.path.isdir(out_dir):
                os.mkdir(out_dir)

            with open(os.path.join(out_dir, filename), "w", encoding=out_encoding) as out_file:
                for line in in_file:
                    valid_line = line
                    for invalid_char, valid_char in char_map.items():
                        valid_line = valid_line.replace(invalid_char, valid_char)
                    out_file.write(valid_line)
                    if line != valid_line:
                        has_changed = True
        if has_changed is True:
            changed_count += 1

    print("processed files: %s" % len(filenames))
    print("affected files: %s" % changed_count)
