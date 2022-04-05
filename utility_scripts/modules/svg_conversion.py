import pyvips
import os


def main(svg_folder, output_folder, drawables):
    for drawable in drawables:
        input = os.path.join(svg_folder, drawable + '.svg')
        output = os.path.join(output_folder, drawable + ".png")
        image = pyvips.Image.thumbnail(input, 192, height=192)
        image.write_to_file(output)
