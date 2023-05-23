import os
from PIL import Image

# Desired size
WIDTH, HEIGHT = 2560, 1440
ASPECT_RATIO = WIDTH / HEIGHT

def add_transparency(img):
    width, height = img.size
    new_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

    if width / height > ASPECT_RATIO:
        scale = WIDTH / width
        new_height = int(height * scale)
        resized_img = img.resize((WIDTH, new_height), Image.ANTIALIAS)
        upper = (HEIGHT - new_height) // 2
        new_img.paste(resized_img, (0, upper))

    else:
        scale = HEIGHT / height
        new_width = int(width * scale)
        resized_img = img.resize((new_width, HEIGHT), Image.ANTIALIAS)
        left = (WIDTH - new_width) // 2
        new_img.paste(resized_img, (left, 0))

    return new_img

for filename in os.listdir('.'):
    if filename.endswith(('.png', '.gif', '.jpg', '.jpeg')):
        img = Image.open(filename)
        if img.size != (WIDTH, HEIGHT):
            new_img = add_transparency(img)

            # Save in the appropriate format
            base_name, extension = os.path.splitext(filename)
            if filename.endswith('.gif'):
                new_img.save(base_name + '_resized.gif', 'GIF', save_all=True)
            else:
                new_img.save(base_name + '_resized.png', 'PNG')
