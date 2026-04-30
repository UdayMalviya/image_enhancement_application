from PIL import Image, ImageEnhance
from pathlib import Path


def read_image(image_path: Path):
    if not image_path:
        raise ValueError(f"Image path cannot be empty, given path is: {image_path}")
    img = Image.open(image_path)
    return img

def enhance_image(image, factor: float, method):
    if method.lower() == 'contrast':
        enhancer = ImageEnhance.Contrast(image).enhance(factor)
    elif method.lower() == 'brightness':
        enhancer = ImageEnhance.Brightness(image).enhance(factor)
    if method.lower() == 'sharpness':
        enhancer = ImageEnhance.Sharpness(image).enhance(factor)
    return enhancer


def save_image(image, out_path):
    image.save(out_path)
    print(f"Image saved successfully at: {out_path}")

def main():
    img = read_image(r'images\Interstellar wallpaper 4k.jpg')
    save_image(enhance_image(img, 0.3, 'sharpness'), out_path=r'images/file.png')


if __name__ == '__main__':
    main()

    


    




