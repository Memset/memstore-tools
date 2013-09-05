=begin

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

=cut
use strict;
use warnings;

use HTTP::Request;
use LWP::UserAgent;

# configuration
my $chunk_size = 64*1024;
my $auth_url = "https://auth.storage.memset.com/v1.0";

# Authenticate (get a token)
sub authenticate {
	my ($username, $password) = @_;
	my $token;
	my $storage_url;

	my $ua = LWP::UserAgent->new;

	my $req = HTTP::Request->new(GET => $auth_url);

	$req->header("X-Auth-User" => $username);
	$req->header("X-Auth-Key" => $password);

	my $res = $ua->request($req);

	die("Failed to auth: ". $res->message ."\n") unless $res->is_success;

	$token = $res->header("X-Auth-Token");
	$storage_url = $res->header("X-Storage-URL");
	# see Expires header to know how long will the token last

	die("Failed to get a token\n") unless $token && $storage_url;

	return ($token, $storage_url);
}

# Read a file in chunks using chunked transfer encoding
sub file_into_chunks {
	my $fd = shift;
	my $chunk;

	if(!fileno($fd)) {
		return "";
	}

	read($fd, $chunk, $chunk_size);

	if($chunk) {
		return sprintf("%x\r\n%s\r\n", length($chunk), $chunk);
	}

	close($fd);
	return "0\r\n\r\n";
}


# Main #######################################

# your Memstore credentials
my $username = "YOUR-USER";  # ie. msmymemstore1.admin
my $password = "PASSWORD";

my ($token, $storage_url) = authenticate($username, $password);

my $filename = "bigfile.bin";          # local filename
my $destination = "/TEST/" .$filename; # /CONTAINER/path/name

# we're going to build an URL that is https://STORAGE_URL/CONTAINER/path/name

my $ua = LWP::UserAgent->new;
my $req = HTTP::Request->new(PUT => $storage_url .$destination);

# optional, you can specify the type of file
# $req->header("Content-Type" => "");

# the auth token is required
$req->header("X-Auth-Token" => $token);

# sending the file in chunks
$req->header("Transfer-Encoding" => "chunked");
$req->header("Content-Length" => -s $filename);

# set the content of the request
open(FD, "<", $filename);

$req->content(sub {
	return file_into_chunks(\*FD);
});

my $res = $ua->request($req);

die("Failed to upload the file: " .$res->message ."\n") unless $res->is_success;

# the MD5 of the upload file is in $res->headers->{"etag"}
print "OK, MD5 ". $res->headers->{"etag"} ."\n";

# EOF

