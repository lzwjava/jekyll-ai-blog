source "https://rubygems.org"

# Specify the Jekyll version
gem 'jekyll', '>= 4.4.1'

# Default theme for new Jekyll sites
gem 'minima'

# Windows and JRuby do not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :install_if => Gem.win_platform?

# Additional plugins
gem 'jekyll-sitemap'
gem 'jekyll-seo-tag'

gem 'jekyll-toc'

# gem 'webrick', '~> 1.7'

# Ensure compatibility with the logger gem
gem 'logger'

# Ensure compatibility with the rubyzip gem
gem 'rubyzip'

# Add csv and bigdecimal to avoid warnings
gem 'csv'
gem 'bigdecimal'

gem "jekyll-include-cache"

gem 'jekyll-theme-cayman'
