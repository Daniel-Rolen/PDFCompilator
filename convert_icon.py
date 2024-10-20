import cairosvg
import os

def convert_svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)

if __name__ == "__main__":
    svg_path = os.path.join('assets', 'app_icon.svg')
    png_path = os.path.join('assets', 'app_icon.png')
    
    if os.path.exists(svg_path):
        convert_svg_to_png(svg_path, png_path)
        print(f"Icon converted successfully: {png_path}")
    else:
        print(f"SVG icon not found: {svg_path}")
