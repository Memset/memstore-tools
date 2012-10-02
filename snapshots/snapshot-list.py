#!/usr/bin/env python
"""
List Miniserver Snapshots using OpenStack Object Storage API

Copyright (C) 2012 Memset Ltd; http://www.memset.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==

This script lists all the snapshots in a Memstore(tm) instance, calculating
the used space by adding up the size of all the .part files.

It provides more detail than:

    http://www.memset.com/apidocs/methods_server.html#server.snapshot_list

The output is in JSON format.

Required:

    - Python 2.6 (or later)
    - python-swiftclient: https://github.com/openstack/python-swiftclient

"""

from optparse import OptionParser
import json

from swiftclient.client import Connection, ClientException

VERSION = "1.0"
AUTH_URL = "https://auth.storage.memset.com/v1.0"

class Main(object):
    def __init__(self):

        parser = OptionParser(usage="%prog [options] memstore_admin password",
                              version="%prog v" + VERSION,
                              description="List Miniserver snapshots stored in a Memstore(tm) instance.",
                              epilog="For further information, please visit: http://www.memset.com/cloud/storage/")

        parser.add_option("--auth_url",
                          type="str",
                          dest="auth_url",
                          default=AUTH_URL,
                          help="Auth URL (default: %s)" % AUTH_URL,
                          )

        self.options, self.args = parser.parse_args()

        if len(self.args) != 2:
            parser.error("Not enough parameters provided")

        self.conn = Connection(self.options.auth_url, self.args[0], self.args[1])

    def run(self):

        info, snapshots = self.conn.get_container('miniserver-snapshots', delimiter='/')

        for snap in snapshots:
            if 'subdir' not in snap.keys():
                continue

            _, objects = self.conn.get_container('miniserver-snapshots', prefix=snap["subdir"])
            snap["bytes-used"] = 0
            snap["parts"] = 0
            readme = False
            for obj in objects:
                snap["bytes-used"] += obj["bytes"]
                if '.part' in obj.get("name", ""):
                    snap["parts"] += 1
                elif obj.get("name", "").lower().endswith("readme.txt"):
                    readme = True
                    snap["date"] = obj["last_modified"]

            if not readme:
                snap["notes"] = "README.txt not found, it may be an incomplete snapshot"

        result = dict((key[len("x-container-"):], value) for key, value in info.items() if key.startswith("x-container-"))
        result["snapshots"] = snapshots

        print json.dumps(result, indent=1)


if __name__ == '__main__':
    main = Main()
    main.run()

