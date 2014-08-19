require 'rubygems'
require 'twitter'

# TwitterStats
begin

# Configuration
  client = Twitter::Streaming::Client.new do |config|
    config.consumer_key = "TWPsNBca4joN3o3bF5GP8X52J"
    config.consumer_secret = "k1O9YO267OsDedaErkhR1MTIxJS9FjgIPCnhtcsM0o4IVEnQk0"
    config.access_token = "2199777559-0cnOjV5oBtGl57FIWrtpNI5THdrRjyS9f9O9pQV"
    config.access_token_secret = "hSs76D1kxjepVUuXoy0WinWisUyYdXifEbqNkd7IKCJZ2"
  end
  
  puts "Scanning..."

  client.filter(:track => "guardiancrime statme") do |tweet|
    puts "@#{tweet.user.screen_name}: #{tweet.text}"
    client = Twitter::REST::Client.new do |config|
      config.consumer_key = "TWPsNBca4joN3o3bF5GP8X52J"
      config.consumer_secret = "k1O9YO267OsDedaErkhR1MTIxJS9FjgIPCnhtcsM0o4IVEnQk0"
      config.access_token = "2199777559-0cnOjV5oBtGl57FIWrtpNI5THdrRjyS9f9O9pQV"
      config.access_token_secret = "hSs76D1kxjepVUuXoy0WinWisUyYdXifEbqNkd7IKCJZ2"
    end 
    client.update("@#{tweet.user.screen_name} hello!")
    puts "Threat neutralized."
    puts "Scanning..."
  end
end