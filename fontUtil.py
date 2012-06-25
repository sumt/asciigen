from PIL import Image, ImageDraw, ImageFont

#return the image size of one letter based on font size
def fontImageSize(font_size):
  font = ImageFont.truetype("CourierNew.ttf", font_size)
  return font.getsize("A")

#create a PIL.Image object containing the character string in parameter letter
#return: PIL.Image of the string of letters in black with white background
def getCharImage(letter, font_size):
  font = ImageFont.truetype("CourierNew.ttf", font_size)
  image_size = font.getsize(letter)
  image = Image.new("L", image_size, 255)
  draw = ImageDraw.Draw(image)
  draw = draw.text((0,0), letter, 0, font=font)
  return image

#calculate the square distance between 2 images as if they are two vectors
#with each pixel representing a dimention
def squareDist(image1, image2):
  image1_data = list(image1.getdata())
  image2_data = list(image2.getdata())
  minlen = min(len(image1_data), len(image2_data))
  square_dist = reduce(lambda x, y: x + (y[1] - y[0])**2, zip(image1_data, image2_data), 0)
  return square_dist
