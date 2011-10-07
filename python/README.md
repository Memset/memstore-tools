cf-upload.py
============

This is a simple tool for uploading files to Memstore(tm) using Rackspace
Cloud Files(tm) compatible API.

Requires python-cloudfiles (python-rackspace-cloudfiles on Debian/Ubuntu).

Please check -h option for help.

Examples:

    cf-upload.py -u msproduct.user -p passwd -C blog -d /images image.jpg

Using 'msproduct.user' access username with 'passwd' password, uploads into
'/images' directory of 'blog' container the 'image.jpg' file. The directory is
created if it doesn't exist.

    cf-upload.py -u msproduct.user -p passwd -C music files/*.mp3

Using 'msproduct.user' access username with 'passwd' password, uploads into
root directory of 'music' container all the mp3 files found in 'files' local
directory.

License
-------

Copyright (C) 2011 by Memset Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

http://www.memset.com/


