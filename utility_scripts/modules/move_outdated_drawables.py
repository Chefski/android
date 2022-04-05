from glob import glob
import os
from bs4 import BeautifulSoup as bs

num2words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
			 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
			 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
			 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
			 19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
			 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty',
			 90: 'ninety'}


def n2w(n):
	try:
		return num2words[n]
	except KeyError:
		try:
			return num2words[n-n % 10] + num2words[n % 10]
		except KeyError:
			return 'Number out of range'


def main(drawable_file, drawables_to_update, drawable_folder):
	renamed_drawables = []

	with open(drawable_file) as file:
		soup = bs(file.read(), 'xml')
		for drawable in drawables_to_update:
			drawable_path = os.path.join(
				drawable_folder, drawable["update_drawable"] + ".png")
			if os.path.exists(drawable_path):
				count = len(
					glob(
						drawable_path + "/" +
						drawable["update_drawable"] + '.png') +
					glob(
						drawable_path + "/" +
						drawable["update_drawable"] + '_alt*.png'))
				suffix = "_alt"
				if count > 1:
					suffix += "_" + n2w(count)
				renamed_drawables.append({
					"drawable": drawable["update_drawable"] + suffix,
					"name": soup.find(
						"item", attrs={"drawable": drawable
									   ["update_drawable"]})["name"] +
					" Alt " + str(count + 1), })
				os.rename(drawable_path, drawable_path.replace(".png", suffix + ".png"))

			return renamed_drawables
