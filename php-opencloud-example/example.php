<?php

require __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\HandlerStack;
use OpenStack\Common\Transport\Utils as TransportUtils;
use OpenStack\Identity\v2\Service;
use OpenStack\OpenStack;

$authUrl = 'https://auth-host.local/v2.0';

$httpClient = new Client([
    'base_uri' => TransportUtils::normalizeUrl($authUrl),
    'handler'  => HandlerStack::create(),
]);

$client = new OpenStack(
    [
        'authUrl' => $authUrl,
        'region' => 'reading',
        'username' => 'admin',
        'password' => 'YOUR-PASSWORD',
        'tenantName' => 'YOUR-MEMSTORE', // e.g. mstestaa1
        'identityService' => Service::factory($httpClient),
    ]
);

$service = $client->objectStoreV1(
    [
        'catalogName' => 'memstore',
    ]
);

$containers = $service->listContainers();
foreach ($containers as $container) {
    printf("Container name: %s\n", $container->getObject()->containerName);
}
