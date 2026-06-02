---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: HTTPS Test Certificates in Form Data
translated: false
type: note
---

Question: What are key.pem and cert.pem used for in the test/fixture directory of the form-data GitHub npm package?

Answer:

In the `form-data` npm package's GitHub repository (https://github.com/form-data/form-data), the `test/fixture` directory contains test fixture files used in integration tests. Specifically:

- **key.pem**: This is the private key file for a self-signed SSL certificate. It is loaded and used to configure a local HTTPS server in the integration tests.

- **cert.pem**: This is the self-signed SSL certificate file (public key). It is used both for the HTTPS server configuration and as a Certificate Authority (CA) in the client-side request options to trust the self-signed certificate during testing.

### Purpose and Usage
These files were introduced in 2015 to enable local HTTPS testing without relying on external servers. The key changes from the relevant commits (afe1959 and 4d5ec50) include:

- **Local HTTPS Server Setup**: In helper files like `static.js` and `common.js`, the HTTPS server is created using Node.js's `https` module with options like:
  ```js
  const httpsServer = https.createServer({
    key: common.httpsServerKey,  // Loaded from 'test/fixture/key.pem'
    cert: common.httpsServerCert // Loaded from 'test/fixture/cert.pem'
  });
  ```
  The server listens on a port (e.g., 9443) and responds to requests for testing purposes.

- **Loading the Files**: In `test/common.js`, the files are read using:
  ```js
  const fs = require('fs');
  const path = require('path');
  common.httpsServerKey = fs.readFileSync(path.join(__dirname, '..', 'fixture', 'key.pem'));
  common.httpsServerCert = fs.readFileSync(path.join(__dirname, '..', 'fixture', 'cert.pem'));
  ```

- **Integration Test**: In `test/integration/test-submit-https.js`, the `FormData` instance is submitted to the local HTTPS server (e.g., `localhost:9443`). The request options include `ca: common.httpsServerCert` to handle self-signed certificate validation, avoiding rejection errors.

This setup allows testing the submission of multipart/form-data over HTTPS in a controlled, local environment. The certificate was updated in 2019 (commit e90a76a) likely due to expiration or other maintenance.

Note that the `form-data` library itself does not handle HTTP/HTTPS requests or TLS configuration—it only builds the form-data streams. These fixtures are purely for the repository's integration tests to simulate real-world usage with an HTTPS endpoint.

References:

- [https://github.com/form-data/form-data/commit/afe1959ec711f23e57038ab5cb20fedd86271f29](https://github.com/form-data/form-data/commit/afe1959ec711f23e57038ab5cb20fedd86271f29)
- [https://github.com/form-data/form-data/commit/4d5ec50e81109ad2addf3dbb56dc7c134df5ff87](https://github.com/form-data/form-data/commit/4d5ec50e81109ad2addf3dbb56dc7c134df5ff87)
