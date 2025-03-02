from PIL import Image

# تنظیمات مورد نیاز - حتماً این مقادیر را با تنظیمات پروژه خودتان جایگزین کنید
binary_file_path = 'test.bin'  # مسیر فایل باینری خام
output_bmp_file = 'test.bmp'  # نام فایل BMP خروجی
width = 480  # عرض تصویر (پیکسل) - مقدار واقعی را وارد کنید
height = 272  # ارتفاع تصویر (پیکسل) - مقدار واقعی را وارد کنید
pixel_format = 'RGB565'  # فرمت پیکسل - 'RGB565' یا 'RGB888' یا 'L' (برای GrayScale) - مقدار واقعی را وارد کنید

# پردازش فرمت پیکسل برای Pillow
if pixel_format == 'RGB565':
    mode = 'RGB' # Pillow مستقیماً RGB565 را پشتیبانی نمی‌کند، به RGB تبدیل می‌کنیم
    pixel_bytes_per_pixel = 2
elif pixel_format == 'RGB888':
    mode = 'RGB'
    pixel_bytes_per_pixel = 3
elif pixel_format == 'GrayScale' or pixel_format == 'L': # 'L' برای GrayScale در Pillow
    mode = 'L'
    pixel_bytes_per_pixel = 1
else:
    raise ValueError("فرمت پیکسل نامعتبر. فرمت‌های RGB565، RGB888 یا GrayScale را انتخاب کنید.")

try:
    with open(binary_file_path, 'rb') as f:
        binary_data = f.read()

    # محاسبه تعداد بایت‌های مورد انتظار
    expected_bytes = width * height * pixel_bytes_per_pixel
    if len(binary_data) != expected_bytes:
        raise ValueError(f"اندازه فایل باینری با اندازه تصویر مورد انتظار ({expected_bytes} بایت) مطابقت ندارد. اندازه فایل: {len(binary_data)} بایت.")


    if pixel_format == 'RGB565':
        # تبدیل RGB565 به RGB888 (نیاز به پردازش دستی)
        pixels_rgb888 = bytearray()
        for i in range(0, len(binary_data), 2):
            pixel_data = int.from_bytes(binary_data[i:i+2], byteorder='little') # فرض byteorder='little' - بسته به معماری CPU ممکن است متفاوت باشد
            r = (pixel_data >> 11) & 0x1F  # 5 bits for red
            g = (pixel_data >> 5) & 0x3F   # 6 bits for green
            b = pixel_data & 0x1F          # 5 bits for blue

            # گسترش به 8 بیت برای هر کانال (تقریب)
            r = (r << 3) | (r >> 2)
            g = (g << 2) | (g >> 4)
            b = (b << 3) | (b >> 2)

            pixels_rgb888.extend(bytes([r, g, b]))

        image = Image.frombytes(mode, (width, height), bytes(pixels_rgb888)) # از بافر RGB888 استفاده می‌کنیم

    else: # RGB888 یا GrayScale
        image = Image.frombytes(mode, (width, height), binary_data)


    image.save(output_bmp_file, 'BMP')
    print(f"فایل BMP با نام '{output_bmp_file}' با موفقیت ایجاد شد.")

except FileNotFoundError:
    print(f"خطا: فایل '{binary_file_path}' یافت نشد.")
except ValueError as e:
    print(f"خطا: {e}")
except Exception as e:
    print(f"خطای غیرمنتظره: {e}")
