---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Opinions on PHP
translated: false
type: note
---

Question: What are some unpopular or unconventional opinions or ideas about PHP?

Answer:

Here are several genuinely unpopular or contrarian takes on PHP that you’ll rarely see praised in mainstream developer discourse:

- **PHP never really needed a type system**
  Strict types (added in PHP 7) and especially scalar type hints are often over-applied and make the language feel like a worse TypeScript. PHP’s original dynamic, duck-typed nature was perfect for the kind of quick-and-dirty web glue it was designed for. Adding types mostly benefits IDEs and large teams, but for the majority of small-to-medium sites and scripts, it’s ceremonial overhead that slows prototyping without delivering proportional safety.

- **Composer and the PSR standards ruined PHP’s “batteries-included” spirit**
  Before Composer, almost everything you needed was either in core or a single-file include you could drop in. Now the ecosystem demands a package manager, autoloading, and adherence to half a dozen PSRs just to `echo "Hello World"` in a modern framework. The language became more “professional” at the cost of the effortless hackability that made it dominate the web in the first place.

- **PHP 8+ is objectively worse for the average small-site developer than PHP 5.6**
  PHP 5.6 (with security backports) was the peak of stability, performance, and simplicity. Modern PHP versions keep adding syntax sugar (attributes, match expressions, readonly classes, etc.) that mostly benefits framework authors and enterprise codebases, while the upgrade path breaks countless legacy apps and hosting environments still stuck on older versions.

- **Laravel is holding PHP back more than helping it**
  Laravel’s dominance has created a monoculture where “modern PHP” essentially means “Laravel + Vue/Inertia/Livewire.” It discourages people from learning the language itself and encourages enormous abstraction layers that hide PHP’s strengths (simplicity, direct access to $_GET/$_POST, raw SQL when you need it). Most Laravel apps could be 10× smaller and faster if written in vanilla PHP or a micro-framework.

- **The hate PHP got in the 2000s–2010s was largely justified and healthy**
  The language deserved the ridicule. Terrible built-in function naming, inconsistent argument order, magic quotes, register_globals, and a core library that looked like it was designed by committee on a weekend. The scorn forced the community to clean house (PHP 7 performance jump, namespace adoption, etc.). Today’s revisionist “PHP is actually good now” narrative forgets that it took a decade of public shaming to get here.

- **WordPress is the best thing that ever happened to PHP (and also the worst)**
  Unpopular two-sided take: WordPress kept PHP relevant and paid the bills for millions of developers and hosting companies, preventing the language from fading into obscurity like Perl. At the same time, it locked the ecosystem into ancient patterns and gave PHP a permanent reputation for sloppy code that modern PHP developers are still fighting.

- **Global functions and the superglobals are elegant, not ugly**
  `strlen()`, `json_encode()`, `$_SESSION`, `$_POST` being globally available is a feature, not a bug. Namespacing everything “properly” just adds noise when you’re writing a 200-line script. PHP was designed for embedding in HTML templates; pretending it should look like Java just fights the language.

- **PHP should have stayed single-threaded and share-nothing forever**
  Attempts to make PHP async (ReactPHP, Swoole, RoadRunner) miss the point. The beauty of PHP has always been the simple request–response lifecycle that maps perfectly to cheap Apache/Nginx + PHP-FPM hosting. Trying to turn it into Node.js or Go just creates a worse version of those tools while abandoning what PHP does best.

These opinions tend to trigger strong reactions in PHP circles, especially among the “modern PHP” crowd, but they’re held quietly by a surprising number of long-time PHP developers who lived through the 4 → 5 → 7 → 8 transitions.
