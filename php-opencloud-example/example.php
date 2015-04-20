<?php
// This is example.php

require 'vendor/autoload.php';

use OpenCloud\OpenStack;

$client = new OpenStack(
    'https://auth-host.local/v2.0',
    array(
        'username' => 'admin',
		'password' => 'YOUR-PASSWORD',
        'tenantName' => 'YOUR-MEMSTORE' // ie. mstestaa1
    ));

$service = $client->objectStoreService("memstore", "reading");

$containers = $service->listContainers();
foreach ($containers as $container) {
    printf("Container name: %s\n", $container->getName());
}

?>
