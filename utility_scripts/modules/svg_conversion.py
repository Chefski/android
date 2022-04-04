from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def main(svg_folder, output_folder, drawables):
	for drawable in drawables:
		vector = svg2rlg(svg_folder + '/' + drawable + '.svg')
		renderPM(vector, output_folder + "/" + drawable + ".png")