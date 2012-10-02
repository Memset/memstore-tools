#!/usr/bin/env python
"""
This is a simple tool for uploading files to Memstore(tm) using Rackspace
Cloud Files(tm) compatible API.

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

"""
import time
from optparse import OptionParser
import logging
import os
import sys

try:
    import cloudfiles
except:
    print """
This script requires python-cloudfiles installed.

We recommend you install it using your distributor package manager.
"""
    sys.exit(1)

__version__ = '0.2'

MEMSTORE_AUTH = "https://auth.storage.memset.com/v1.0"

class main(object):
    def __init__(self):
        parser = OptionParser(usage = "usage: %prog [options] file [file ...]",
                              version="%prog " + __version__,
                              description="This is a simple tool for uploading files to Memstore(tm) using Rackspace Cloud Files(tm) compatible API.",
                              epilog="For further info please visit: http://www.memset.com/cloud/storage/")
        parser.add_option("-A", "--auth-url", dest="authurl",
                          default=MEMSTORE_AUTH,
                          help="Authentication URL (default: Memstore)")
        parser.add_option("-C", "--container", dest="container",
                          default=None,
                          help="Container to upload the files")
        parser.add_option("-d", "--directory", dest="directory",
                          default=None,
                          help="Destination directory, it's created if doesn't exist (default: root of the container)")
        parser.add_option("-u", "--user", dest="user",
                          default=None,
                          help="Username for API Login")
        parser.add_option("-p", "--password", dest="passw",
                          default=None,
                          help="Password for API login")
        parser.add_option("--long-help", dest="long_help",
                          action="store_true",
                          default=False,
                          help="Show long help")
        parser.add_option("-v", "--verbose", dest="verbose",
                          action="store_true",
                          default=False,
                          help="Show detailed information")

        (self.options, self.args) = parser.parse_args()

        if self.options.long_help:
            print __doc__
            sys.exit(1)

        if not all([self.options.container, self.options.user, self.options.passw]):
            parser.error("required parameters missing, try -h")

        if not self.args:
            parser.error("no files provided as argument")

    def run(self):
        if self.options.verbose:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("verbose logging enabled")

        logging.debug("opening connection")
        try:
            cf = cloudfiles.get_connection(self.options.user, self.options.passw,
                                           authurl=self.options.authurl, timeout=30)
        except Exception as e:
            logging.error("auth failed: %s" % e)
            return

        try:
            container = cf.get_container(self.options.container)
        except Exception as e:
            logging.error("get_container failed: %s" % e)
            return

        ok = 0
        fail = 0
        total_time = 0
        for filename in self.args:
            filename_dst = os.path.basename(filename)
            logging.debug("%s: starting" % filename_dst)

            start = time.time()

            if self.options.directory:
                directory = self.options.directory.strip('/')
                try:
                    # if the directory already exists, we get an instance
                    obj = container.create_object(directory)
                    obj.content_type = 'application/directory'
                    obj.write('0')
                except Exception as e:
                    logging.warning("%s: create_object failed: %s" % (directory, e))
                else:
                    filename_dst = '%s/%s' % (directory, filename_dst)

            try:

                obj = container.create_object(filename_dst)
                obj.load_from_filename(filename)
            except Exception as e:
                logging.warning("%s: create_object failed: %s" % (filename_dst, e))
                fail += 1
            else:
                ok += 1
            finally:
                delay = time.time()-start
                total_time += delay
                logging.debug("%s: done, %s secs" % (filename_dst, delay))

        try:
            cf.connection.close()
        except:
            pass

        logging.debug("done: %s file(s) OK, %s files(s) failed, %s secs" % (ok, fail, total_time))

        if fail:
            # we had errors
            sys.exit(1)
        else:
            sys.exit(0)

if __name__=="__main__":
    main = main()
    main.run()

