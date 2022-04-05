from email import charset
from encodings import utf_8
import re
from bs4 import Tag, BeautifulSoup as bs
from iteration_utilities import unique_everseen


def createTag(entry, soup):
	attrs = {
		"drawable": entry["drawable"],
	}
	if "name" in entry:
		attrs["name"] = entry["name"]
	tag = soup.new_tag("item", attrs=attrs)
	return tag


def main(drawable_file, new_drawables):
	with open(drawable_file, 'r+') as file:
		grouped = {
			"google": [],
			"folder": [],
			"calendar": [],
			"#": [],
			"other": [],
		}

		xml = bs(file, 'xml', from_encoding="utf_8")
		existing_drawables = [x.attrs for x in xml.resources.find_all('item')]
		drawables = existing_drawables + new_drawables
		drawables = list(unique_everseen(
			drawables, key=lambda x: frozenset(x.items())))

		drawables.sort(key=lambda x: x["drawable"])

		# split into groups
		for drawable in drawables:
			if drawable["drawable"].startswith("google_"):
				grouped["google"].append(drawable)
			elif drawable["drawable"].startswith("folder_"):
				grouped["folder"].append(drawable)
			elif "calendar" in drawable["drawable"] and (drawable["drawable"][-1].isdigit() or len([x for x in drawables if x["drawable"] == drawable["drawable"] + "_1"]) > 0):
				grouped["calendar"].append(drawable)
			elif drawable["name"][0].isdigit() if "name" in drawable else drawable["drawable"][0].isdigit():
				grouped["#"].append(drawable)
			elif "name" in drawable and not ord(drawable["name"][0]) < 128 or not drawable["name"][0].isalnum() if "name" in drawable else not drawable["drawable"][0].isalnum():
				grouped["other"].append(drawable)
			else:
				initial = drawable["name"][0].upper(
				) if "name" in drawable else drawable["drawable"][0].upper()
				if initial not in grouped:
					grouped[initial] = []
				grouped[initial].append(drawable)

		# sort groups internally
		for group in grouped.keys():
			grouped[group].sort(
				key=lambda x: x["name"] if "name" in x else x["drawable"])

		output = bs(features="xml")
		resources = output.new_tag("resources")
		version = output.new_tag("version")
		version.string = "1"
		resources.append(version)

		resources.append(output.new_tag("category", attrs={"title": "New"}))
		for entry in new_drawables:
			tag = createTag(entry, output)
			resources.append(tag)

		resources.append(output.new_tag(
			"category", attrs={"title": "Google"}))
		for entry in grouped["google"]:
			tag = createTag(entry, output)
			resources.append(tag)
		del grouped["google"]

		resources.append(output.new_tag(
			"category", attrs={"title": "Folder"}))
		for entry in grouped["folder"]:
			tag = createTag(entry, output)
			resources.append(tag)
		del grouped["folder"]

		resources.append(output.new_tag(
			"category", attrs={"title": "Calendar"}))
		for entry in grouped["calendar"]:
			tag = createTag(entry, output)
			resources.append(tag)
		del grouped["calendar"]

		# sort grouped by key for rest of the groups
		grouped = sorted(grouped.items(), key=lambda x: x[0])

		for group in grouped:
			resources.append(output.new_tag(
				"category", attrs={"title": group[0]}))
			for entry in group[1]:
				tag = createTag(entry, output)
				resources.append(tag)

		output.append(resources)
		file.seek(0)
		file.write(str(output.prettify()))
		file.truncate()
		file.close()
