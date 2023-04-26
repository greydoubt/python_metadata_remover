import os
import sys
from PIL import Image

def create_output_folder(func):
    def wrapper(*args, **kwargs):
        output_folder = kwargs.get("output_folder", None)
        if output_folder is None:
            input_folder = args[0]
            output_folder = input_folder + "_cleaned"
            os.makedirs(output_folder, exist_ok=True)
            kwargs["output_folder"] = output_folder
        return func(*args, **kwargs)
    return wrapper

@create_output_folder
def clean_image_metadata(image_path, output_folder):
    with Image.open(image_path) as img:
        # Remove EXIF data
        data = list(img.getdata())
        img_without_exif = Image.new(img.mode, img.size)
        img_without_exif.putdata(data)
        # Save cleaned image to output folder
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, filename)
        img_without_exif.save(output_path)
        print(f"Cleaned metadata from {image_path} and saved cleaned image to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # Clean a single image file
        image_path = sys.argv[1]
        clean_image_metadata(image_path)
    elif len(sys.argv) == 3:
        # Clean all image files in a folder
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        for filename in os.listdir(input_folder):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                image_path = os.path.join(input_folder, filename)
                clean_image_metadata(image_path, output_folder=output_folder)
    else:
        print("Usage: python clean_image_metadata.py <input_folder or image_file> [output_folder]")
