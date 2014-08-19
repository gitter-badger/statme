require 'rubygems'
require 'twitter'

# Guardian StatMe
begin
  client = Twitter::Streaming::Client.new do |config|
    config.consumer_key = "TWPsNBca4joN3o3bF5GP8X52J"
    config.consumer_secret = "k1O9YO267OsDedaErkhR1MTIxJS9FjgIPCnhtcsM0o4IVEnQk0"
    config.access_token = "2199777559-0cnOjV5oBtGl57FIWrtpNI5THdrRjyS9f9O9pQV"
    config.access_token_secret = "hSs76D1kxjepVUuXoy0WinWisUyYdXifEbqNkd7IKCJZ2"
  end
  puts "Scanning..."
  client.filter(:track => "guardiancrime statme") do |tweet|
    if tweet.geo
      long = tweet.geo.coordinates[0]
      lat = tweet.geo.coordinates[0]
      puts "@#{tweet.user.screen_name} #{lat}, #{long}: #{tweet.text}"
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
end