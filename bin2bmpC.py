from PIL import Image

binary_file_path = 'test.bin'
output_bmp_file = 'test.bmp'
width = 480
height = 272
pixel_format = 'RGB565'  # Pixel Format - 'RGB565' or  'RGB888'

if pixel_format == 'RGB565':
    mode = 'RGB'
    pixel_bytes_per_pixel = 2
elif pixel_format == 'RGB888':
    mode = 'RGB'
    pixel_bytes_per_pixel = 3
elif pixel_format == 'GrayScale' or pixel_format == 'L':
    mode = 'L'
    pixel_bytes_per_pixel = 1
else:
    raise ValueError("Please Select Valid pixel Format, RGB565، RGB888 or GrayScale .")

try:
    with open(binary_file_path, 'rb') as f:
        binary_data = f.read()

    #calculate Needed Byte to convert
    expected_bytes = width * height * pixel_bytes_per_pixel
    if len(binary_data) != expected_bytes:
        raise ValueError(f"‌Lenght of Binary File comparable to the output Pic size ({expected_bytes} Byte)  did not Match File Size: {len(binary_data)} byte.")


    if pixel_format == 'RGB565':
        # Convert RGB565 to RGB888
        pixels_rgb888 = bytearray()
        for i in range(0, len(binary_data), 2):
            pixel_data = int.from_bytes(binary_data[i:i+2], byteorder='little') # Default byteorder='little'
            r = (pixel_data >> 11) & 0x1F  # 5 bits for red
            g = (pixel_data >> 5) & 0x3F   # 6 bits for green
            b = pixel_data & 0x1F          # 5 bits for blue

            r = (r << 3) | (r >> 2)
            g = (g << 2) | (g >> 4)
            b = (b << 3) | (b >> 2)

            pixels_rgb888.extend(bytes([r, g, b]))

        image = Image.frombytes(mode, (width, height), bytes(pixels_rgb888))

    else: # RGB888 or GrayScale
        image = Image.frombytes(mode, (width, height), binary_data)


    image.save(output_bmp_file, 'BMP')
    print(f"'{output_bmp_file}' Completely Created.")

except FileNotFoundError:
    print(f"Err: File '{binary_file_path}' Not Found.")
except ValueError as e:
    print(f"Err: {e}")
except Exception as e:
    print(f"Unexpected Err: {e}")
