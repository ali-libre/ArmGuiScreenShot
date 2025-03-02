to capture screenShot:
take a memory dump of FrameBuffer memory to File,
in Stm32CubeIDE memory-Window->Export
set Configuration of captured picture in python Script 
convert binary to BPM.


برای اسکرین شات گرفتن از TouchGFX میتوان به روش زیر عمل کرد:

ابتدا با دیباگر برنامه را دیباگ میکنیم.

در مرحله دوم memory Window را انتخاب کرده و ادرس بافر Touchgfx را وارد میکنیم.

در مرحله بعد با دانستن اندازه تصویر، و سایز هر پیکس ، با lenght مناسب اکسپورت میگیریم.

در مرحله با تنظیم نام و اندازه تصویر در فایل اسکریپت تصویر مورد نظر را بدست می آوریم.
