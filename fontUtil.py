from PIL import Image, ImageDraw, ImageFont

def getCharImage(letter, font_size):
  font = ImageFont.truetype("CourierNew.ttf", font_size)
  image_size = font.getsize(letter)
  image = Image.new("L", image_size, 255)
  draw = ImageDraw.Draw(image)
  draw = draw.text((0,0), letter, 0, font=font)
  return image
