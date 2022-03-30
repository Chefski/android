import sys
import re


def main(drawable_file, new_drawables, renamed_drawables):
    with open(drawable_file) as file:
        lines = file.readlines()
        drawables = []
        google = []
        folder = []
        drawable_regex = re.compile(r'drawable="([\w_]+)"')

        # collect existing drawables
        for line in lines:
            drawable = re.search(drawable_regex, line)
            if drawable:
                if drawable.groups(0)[0].startswith('google'):
                    google.append(drawable.groups(0)[0])
                elif drawable.groups(0)[0].startswith('folder'):
                    folder.append(drawable.groups(0)[0])
                else:
                    drawables.append(drawable.groups(0)[0])

        # remove duplicates and sort
        drawables = list(set(drawables + new_drawables + renamed_drawables))
        drawables.sort()
        google = list(set(google))
        google.sort()
        folder = list(set(folder))
        folder.sort()

        # build
        output = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n<version>1</version>\n\n\t<category title="New" />\n\t'
        for entry in new_drawables:
            output += '<item drawable="%s" />\n\t' % entry

        output += '\n\t<category title="Google" />\n\t'
        for entry in google:
            output += '<item drawable="%s" />\n\t' % entry

        output += '\n\t<category title="Folders" />\n\t'
        for entry in folder:
            output += '<item drawable="%s" />\n\t' % entry

        output += '\n\t<category title="A" />\n\t'
        letter = "a"

        # iterate alphabet
        for entry in drawables:
            if not entry.startswith(letter):
                letter = chr(ord(letter) + 1)
                output += '\n\t<category title="%s" />\n\t' % letter.upper()
            output += '<item drawable="%s" />\n\t' % entry

        output += "\n</resources>"

        file.write(output)
