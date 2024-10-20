from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon(output_path, size=(50, 50), bg_color=(255, 105, 180), text_color=(255, 255, 255)):
    # Create a new image with a pink background
    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)

    # Add text to the image
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    text = "PDF"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_position = ((size[0] - text_bbox[2]) / 2, (size[1] - text_bbox[3]) / 2)
    draw.text(text_position, text, font=font, fill=text_color)

    # Save the image
    image.save(output_path)
    print(f"Icon created successfully: {output_path}")

if __name__ == "__main__":
    output_path = os.path.join('assets', 'app_icon.png')
    create_simple_icon(output_path)
