* https://rvm.io/rvm/install

Ubuntu
```shell
apt-get install software-properties-common
apt-add-repository -y ppa:rael-gc/rvm
apt-get update
apt-get install rvm
# also as root
. /etc/profile.d/rvm.sh
rvm install ruby

# back as regular user run this or re-login
. /etc/profile.d/rvm.sh

# Run interactive Ruby shell
irb
```

```ruby
# The load method includes the named Ruby source file every time the method is executed
load 'filename.rb'  

# The more commonly used require method loads any given file only once
require 'filename'

# Ruby 1.9 introduced a simplified syntax for hash with symbols keys. Note the difference
puts ({"string_key" => "value"})
puts ({"symbol_key": "value"})
# {"string_key"=>"value"}
# {:symbol_key=>"value"}
```
