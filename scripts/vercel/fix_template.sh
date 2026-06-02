#!/bin/bash
sed -i 's/<%= Time.now.strftime("%Y-%m-%d %H:%M:%S %z") %>/2024-12-12 00:00:00 +0000/' vendor/bundle/ruby/3.3.0/gems/jekyll-3.10.0/lib/site_template/_posts/0000-00-00-welcome-to-jekyll.markdown.erb
