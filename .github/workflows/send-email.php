<?php
require 'vendor/autoload.php'; // Load AWS SDK for PHP

use Aws\Ses\SesClient;
use Aws\Ses\Exception\SesException;

$client = new SesClient([
    'version' => 'latest',
    'region' => 'us-north-1', // Change to your desired AWS region
    'credentials' => [
        'key' => $_ENV['AKIAQ5OENXUUTLYD4Z5K'],
        'secret' => $_ENV['yQpxkeHicwUbKIY/ZFEyNUAKZVtfxU+7iV/xwqLh'],
    ],
]);

$params = [
    'Destination' => [
        'ToAddresses' => [$_ENV['TO_EMAIL']],
    ],
    'Message' => [
        'Body' => [
            'Text' => [
                'Charset' => 'UTF-8',
                'Data' => 'This is the email body.',
            ],
        ],
        'Subject' => [
            'Charset' => 'UTF-8',
            'Data' => 'Email Subject',
        ],
    ],
    'Source' => $_ENV['FROM_EMAIL'],
];

try {
    $result = $client->sendEmail($params);
    echo "Email sent successfully.\n";
} catch (SesException $e) {
    echo "Error sending email: " . $e->getMessage() . "\n";
}
