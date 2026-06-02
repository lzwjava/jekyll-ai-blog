#!/bin/bash

# Basic GET request
echo "Basic GET request:"
curl http://example.com

# GET with custom headers
echo "\nGET request with custom headers:"
curl -H "User-Agent: MyUserAgent/1.0" http://example.com

# POST request
echo "\nPOST request:"
curl -X POST -d "key1=value1&key2=value2" http://example.com/post

# POST with JSON data
echo "\nPOST with JSON data:"
curl -X POST -H "Content-Type: application/json" -d "{\"key1\":\"value1\",\"key2\":\"value2\"}" http://example.com/post

# Using a proxy
echo "\nUsing a proxy:"
curl -x http://proxy.example.com:8080 http://example.com

# Authentication
echo "\nBasic Authentication:"
curl -u username:password http://example.com/auth

# Download a file
echo "\nDownload a file:"
curl -O http://example.com/file.zip

# Follow redirects
echo "\nFollow redirects:"
curl -L http://example.com/redirect

# Save output to a file
echo "\nSave output to a file:"
curl http://example.com -o output.txt

# Custom HTTP method
echo "\nCustom HTTP method (DELETE):"
curl -X DELETE http://example.com/delete/resource

# Verbose output
echo "\nVerbose output:"
curl -v http://example.com

# Connection timeout
echo "\nConnection timeout:"
curl --connect-timeout 5 http://example.com

echo "\nScript execution completed."
