from CairoSVG import svg2png

def convert_svg_to_png(svg_folder, output_folder, drawables):
	for drawable in drawables:
		svg2png(svg_folder + "/" + drawable + ".svg", output_folder + "/" + drawable + ".png")