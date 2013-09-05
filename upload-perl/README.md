
This is an example script on how to use OpenStack Object Storage API to
upload a file using Perl and LWP.

Notes:

 - The auth URL is setup for Memstore
 - The file chunk size is 64 KB
 - Files will be overwritten
 - First level directory is a CONTAINER
 - Any other directory in the path will be "created" automatically

The "special" part of this script is the chunked transfer encoding to allow 
the upload of large files.

Juan J. Martinez <juan@memset.com>
http://www.memset.com/

