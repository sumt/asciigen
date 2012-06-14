import os
import StringIO
from PIL import Image

class GenAscii(object):

  '''
  location - path of the image file to be converted.
  self.image - the image object from the PIL library
  self.pixels - list of pixels from the image object  
  '''
  def __init__(self, location="", data=""):
    if location != "":
      self.image=Image.open(location).convert('L')
      self.pixels=list(self.image.getdata())
    elif data != "":
      self.image=Image.open(StringIO.StringIO(data)).convert('L')
      self.pixels=list(self.image.getdata())
    else:
      self.image = None
      self.pixels = None

  '''
  Divides image into blocks of nxn pixels where n = combinefactor; and calculates the average of each block. 
  combinefactor - determines size of each block; suppose, n is entered, then a block would have n x n pixels
  return - list containing a list of pixel averages, and the width and height of the ascii image; this list is used as the "pixeldata" for the draw function
   '''       
  def combinepixels(self, combinefactor):
    pixels = self.pixels
    width, height = self.image.size
    averages=[]
    for y in range(height/combinefactor):
      y=y*combinefactor
      for x in range(width/combinefactor):
        ave=0
        for i in range(combinefactor):
          ave=ave+sum(pixels[width*(y+i)+x*combinefactor:width*(y+i)+x*combinefactor+combinefactor])/combinefactor
        ave=ave/combinefactor
        averages.append(ave)
    return [averages,width/combinefactor,height/combinefactor]
   
  
  '''
  Takes pixel data determined in combinepixels and maps them to characters in char to produce the ascii image; this function alls the __transformpixel function
  pixeldata - list containing list of averages generated in combinepixels and width and height of the image 
  chars - string of 10 characters used to draw image; the left most pixel will map to ranges closer to 0 while the rightmost to 255
  return - the ascii image
  '''
  def draw(self,pixeldata,chars="@$%OI|+*-' "):
    ascii=''    
    for y in range(pixeldata[2]):
      for x in range(pixeldata[1]):
        x=y*pixeldata[1]+x
        ascii=ascii+self.__transformpixel(pixeldata[0][x], chars)
      ascii=ascii+'\n'
    return ascii
                
  '''
  Private function to map image from draw function  
  '''           
  def __transformpixel(self,pixel, chars):
    chars = list([x for x in chars])
    return chars[pixel/25]
       



