import os, StringIO
from fontUtil import fontImageSize, getCharImage, squareDist
from PIL import Image

"""
Most Primitive Data Mining Method for Generating Ascii Image. Most Inneficient, so
better use it only on small images.
"""
class GenAsciiKNN(object):
  def __init__(self):
    #just an arbiturary number, need to analyze to see what would be the best possible 
    #infinity value
    self.INF = 10000000000000000000000000000000000000000000000000000000000000000

  def searchFontSize(self, target_image):
    """
    Approximate the best font size for the the ascii image. We aim to keep number
    of Ascii characters for the image to be within 50 characters per row.
    We use binary search between font size 8 to 100 to find the best fit.
    """
    minimum = 8
    maximum = 100
    aim = 50
    image_y = target_image.size[0]
    def binarySearch(minimum, maximum):
      if minimum == maximum:
        return minimum
      mid = (maximum + minimum) / 2
      small = (max(mid - 1,minimum) + minimum) / 2
      large = (min(mid + 1,maximum) + maximum) / 2
      test = abs(image_y / fontImageSize(mid)[1] - aim)
      test_small = abs(image_y / fontImageSize(small)[0] - aim)
      test_large = abs(image_y / fontImageSize(large)[0] - aim)
      best = min(test, test_small, test_large)
      if best == test_small:
        return binarySearch(minimum, max(minimum,mid -1))
      elif best == test_large:
        return binarySearch(min(mid+1, maximum), maximum)
      else: #we might not be at the optimal
        return binarySearch(small, large)
    return binarySearch(minimum, maximum)

  def fontSymbols(self, font_size):
    """
    Memorize all the character symbols we're going to use for KNN calculation
    """
    symbols = [(unichr(x), getCharImage(unichr(x), font_size)) for x in range(ord('A'), ord('Z') + 1)]
    symbols.extend([(unichr(x), getCharImage(unichr(x), font_size)) for x in range(ord('a'), ord('z') + 1)])
    symbols.extend([(unichr(x), getCharImage(unichr(x), font_size)) for x in range(ord('0'), ord('9') + 1)])
    symbols.append(('@', getCharImage("@", font_size)))
    symbols.append(('$', getCharImage("$", font_size)))
    symbols.append(('%', getCharImage("%", font_size)))
    symbols.append(('|', getCharImage("|", font_size)))
    symbols.append(('-', getCharImage("-", font_size)))
    symbols.append(('+', getCharImage("+", font_size)))
    symbols.append(('"', getCharImage('"', font_size)))
    symbols.append(('*', getCharImage("*", font_size)))
    symbols.append(("'", getCharImage("'", font_size)))
    symbols.append(('!', getCharImage("!", font_size)))
    symbols.append((' ', getCharImage(" ", font_size)))
    return symbols

  def KNN(self, image, symbol_memo):
    """
    KNN - k nearest neighbor search for the symbol font image closest resembling the image.
    very time consuming function
    """
    best = self.INF
    besti = ''
    for (symbol, img) in symbol_memo:
      dist = squareDist(image, img)
      if dist < best:
        best = dist
        besti = symbol
    assert besti != '' #just in case our infinity fails
    return besti

  #TODO: possible improvement: use line filtering to reduce the picture complexity before
  #      doing KNN
  def genart(self, raw_image):
    """
    Interface function
    """
    image = Image.open(StringIO.StringIO(raw_image)).convert('L')
    font_size = self.searchFontSize(image)
    font_image_size = fontImageSize(font_size)
    symbol_memo = self.fontSymbols(font_size)
    #we'll ignore the parts that don't fit a full size font for now
    maxGrid = [x / y for (x, y) in zip(image.size, font_image_size)] 
    if (len([True for x in maxGrid if x == 0]) > 0):
      return "This image is too small" #temporary way of handling small images
    #we distribute unused region to all sides
    startpos = [ (x - y * z) / 2 for (x, y, z) in zip(image.size, font_image_size, maxGrid)]
    ascii_map = ""
    #i is height, j is width
    for i in range(maxGrid[1]):
      row = "" 
      for j in range(maxGrid[0]):
        upper_left = (j * font_image_size[0] + startpos[0], i * font_image_size[1] + startpos[1])
        b = image.crop((upper_left[0], upper_left[1], upper_left[0] + font_image_size[0], upper_left[1] + font_image_size[1]))
        row = row + self.KNN(b, symbol_memo)
      ascii_map = ascii_map + row + '\n'
    return ascii_map
