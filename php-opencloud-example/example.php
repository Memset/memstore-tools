<?php
// This is example.php

require '/path/to/lib/php-opencloud.php';

$conn = new \OpenCloud\OpenStack(
    'https://auth.storage.memset.com/v2.0',
    array(
        'username' => 'admin',
        'password' => 'PASSWORD',
        'tenantName' => 'YOUR-MEMSTORE' // ie. mstestaa1
    ));


$ostore = $conn->ObjectStore("memstore", "reading", "publicURL");

$containerlist = $ostore->ContainerList();
while($container = $containerlist->Next()) {
    # listing the containers
    printf("Container %s has %u bytes\n", $container->name,
$container->bytes);
}

?>
