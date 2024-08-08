from PIL import Image
import os

def crop_image_into_9_pieces(image_path, output_folder):
    img = Image.open(image_path)

    width, height = img.size

    piece_width = width // 3
    piece_height = height // 3

    k = 1
    for i in range(3):
        for j in range(3):
            left = j * piece_width
            upper = i * piece_height
            right = (j + 1) * piece_width
            lower = (i + 1) * piece_height

            piece = img.crop((left, upper, right, lower))

            piece.save(f"{output_folder}/{k}.png")
            k += 1

crop_image_into_9_pieces('C:\\Users\\gaura\\OneDrive\\Desktop\\Puzzle\\media\\myapp\\present\\img.png', 'C:\\Users\\gaura\\OneDrive\\Desktop\\Puzzle\\media\\myapp\\main\\')