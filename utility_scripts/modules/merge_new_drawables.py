import re
from bs4 import BeautifulSoup as bs
from iteration_utilities import unique_everseen


def createTag(entry):
    tag = bs.new_tag("item")
    tag.attrs['drawable'] = entry["drawable"]
    tag.attrs['name'] = entry["name"]
    return tag


def main(drawable_file, new_drawables):
    with open(drawable_file) as file:
        lines = file.read()
        drawables = {
            "google": {},
            "folder": {},
            "calendar": {},
            "#": {},
        }

        xml = bs(lines, 'xml')
        existing_drawables = xml.find_all('item')

        drawables = {**existing_drawables, **new_drawables}
        drawables = unique_everseen(
            drawables, key=lambda x: frozenset(x.items()))

        # split into groups
        for drawable in drawables:
            if drawable["drawable"].startswith("google_"):
                drawables["google"][drawable["drawable"]] = drawable
                drawables.remove(drawable)
            elif drawable["drawable"].startswith("folder_"):
                drawables["folder"][drawable["drawable"]] = drawable
                drawables.remove(drawable)
            elif (drawable["drawable"].contains("calendar") and drawables.find(drawable["drawable"] + "_1")) or (drawable["drawable"].contains("calendar") and drawable["drawable"][-1].isdigit()):
                drawables["calendar"][drawable["drawable"]] = drawable
                drawables.remove(drawable)
            elif drawable["drawable"][0].isnumeric():
                drawables["#"][drawable["drawable"]] = drawable
                drawables.remove(drawable)
            else:
                drawables[drawable["name"][0].upper()][drawable
                                                       ["drawable"]] = drawable

        # sort groups internally
        for group in drawables:
            drawables[group] = sorted(
                drawables[group].items(), key=lambda x: x[1]["name"])

        output = bs(features="xml")
        resources = bs.new_tag("resources")

        resources.append(bs.new_tag("category", name="New"))
        for entry in new_drawables:
            tag = createTag(entry)
            resources.append(tag)

        resources.append(bs.new_tag("category", name="Google"))
        for entry in drawables["google"]:
            tag = createTag(entry)
            resources.append(tag)
        drawables.remove("google")

        resources.append(bs.new_tag("category", name="Folder"))
        for entry in drawables["folder"]:
            tag = createTag(entry)
            resources.append(tag)
        drawables.remove("folder")

        # sort drawables by key for rest of the groups
        drawables = sorted(drawables.items(), key=lambda x: x[0])

        for group in drawables:
            resources.append(bs.new_tag("category", name=group[0]))
            for entry in group[1]:
                tag = createTag(entry)
                resources.append(tag)

        output.append(resources)
        print(output.prettify())
        file.write(str(output))
