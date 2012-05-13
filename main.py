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

#ASCIIGEN Prototype

asciigen_template = Template("""
<html>
<head>
<link type="text/css" rel="stylesheet" href="{{ cssfile }}">
<title>{{ page_title }}</title>
</head>
<body>
<a href="{{ selfpage }}"><h2>/ASCIIGEN/</h2></a>
<div>
<form method="post">
  <label>
    <div>Image File</div>
    <input type="file" name="image">
  </label>
  <input type="submit" value="Upload">
</form>
</div>
</body>
</html>
""")

asciigen_title = "ASCII"
asciigen_page = "/asciigen"

class AsciiImageGenerator():
  def imageToAscii():
    pass

class GeneralHandler(webapp2.RequestHandler):
  def write(self, template, **args):
    self.response.out.write(template.render(args))

class AsciiGenHandler(GeneralHandler):
  def get(self):
    cssfile = "stylesheet/asciigen.css"
    self.write(asciigen_template, cssfile = cssfile, page_title = asciigen_title, selfpage = asciigen_page)

  def post(self):
    pass

class MainHandler(webapp2.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write("ASCIIGEN")

app = webapp2.WSGIApplication([('/', MainHandler),
                               (asciigen_page, AsciiGenHandler)],
                              debug=True)
