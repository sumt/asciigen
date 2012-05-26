#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi, re
from jinja2 import Template
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import images

#ASCIIGEN Prototype

asciigen_template = Template("""
<html>
<head>
<link type="text/css" rel="stylesheet" href="{{ cssfile }}">
<title>{{ page_title }}</title>
</head>
<body>
<a href="{{ selfpage }}"><h2>/GENASCII/</h2></a>
<div>
<form method="post" enctype="multipart/form-data" action="{{ imageHandlerPage }}">
  <label>
    <div>Image File</div>
    <input type="file" name="{{ vImageName }}" size="40">
  </label>
  <input type="submit" value="Upload">
</form>
</div>
</body>
</html>
""")

asciigen_title = "ASCII"

#global website addresses
asciigen_page = "/genascii"
image_debug_page = "/debug/([^/]+)?"
image_debug_page_sub = "/debug/%(blobid)s"
upload_url = "/upload"

#global webpage variable
image_name = "image"

#global css file for all sites
cssfile = "stylesheet/asciigen.css"

#database containing images that we'll save temporarily
class ImageDB(db.Model):
  mImage = blobstore.BlobReferenceProperty(required = True) #blobInfo of the raw image file

#extends this to handle image trnsformation into ASCII
class AsciiImageGenerator():
  def imageToAscii():
    #TODO: interface class
    pass

#Superclass that defines useful methods for all website handlers
class GeneralHandler(webapp2.RequestHandler):
  def write(self, template, **args):
    self.response.out.write(template.render(args))

class AsciiGenHandler(GeneralHandler):
  def get(self):
    self.write(asciigen_template, cssfile = cssfile, page_title = asciigen_title, selfpage = asciigen_page, imageHandlerPage = blobstore.create_upload_url(upload_url), vImageName = image_name)

  def post(self):
    blob_key = blobstore.parse_blob_info(self.request.POST[image_name])
    img = ImageDB(mImage = blob_key)
    img.put()
    #redirect to the debug page that shows the image
    self.redirect(image_debug_page_sub % {"blobid" : img.key().id()}) #TODO: replace 

#DEBUG Handler that shows the image being uploaded
class ShowImageHandler(webapp2.RequestHandler):
  def get(self, image_id):
    if image_id.isdigit():
      img_file = ImageDB.get_by_id(int(image_id))
      if img_file:
        blob_reader = blobstore.BlobReader(img_file.mImage)
        raw_file = blob_reader.read() #get the raw data of the image from blobInfo key
        img = images.Image(raw_file)
        img.im_feeling_lucky() #a random transformation, 1 transformation is required
        thumbnail = img.execute_transforms(output_encoding = images.JPEG)
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(thumbnail)

class MainHandler(webapp2.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write("GENASCII")

#define a list of websites our server will handle, and map them to the handler class
app = webapp2.WSGIApplication([('/', MainHandler),
                               (asciigen_page, AsciiGenHandler),
                               (upload_url, AsciiGenHandler),
                               (image_debug_page, ShowImageHandler)],
                              debug=True)

