---
audio: false
generated: true
image: false
lang: en
layout: post
title: ng-bootstrap 20 and Angular 21 Compatibility
translated: false
type: note
---

Question: Does ng-bootstrap 20.0.0 support Angular version 21.2.0, and can we use them together?

Answer:

**Yes, ng-bootstrap 20.0.0 supports Angular 21.2.0**, and you can use them together.

According to the official compatibility table from ng-bootstrap:

- ng-bootstrap **20.x.x** requires **Angular ^21.0.0**
  (The caret `^` means >=21.0.0 and <22.0.0)

Since Angular 21.2.0 falls within this range (>=21.0.0 <22.0.0), it is fully compatible.

This is also confirmed in the project's npm page and getting-started documentation. ng-bootstrap 20.0.0 was specifically released to support Angular 21 (released around late 2025), with minimum version bumped to Angular 21.0.0.

**Quick summary of recent versions for reference:**

- ng-bootstrap 18.x → Angular ^19.0.0
- ng-bootstrap 19.x → Angular ^20.0.0
- ng-bootstrap 20.x → Angular ^21.0.0

So using **ng-bootstrap 20.0.0** with **Angular 21.2.0** is not only possible — it's the expected and supported combination.

References:

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0](https://github.com/ng-bootstrap/ng-bootstrap/releases/tag/20.0.0)
- [https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md](https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md)
