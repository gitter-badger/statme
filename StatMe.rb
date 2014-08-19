require 'rubygems'
require 'twitter'

# Guardian StatMe
begin
  client = Twitter::Streaming::Client.new do |config|
    config.consumer_key = ""
    config.consumer_secret = ""
    config.access_token = ""
    config.access_token_secret = ""
  end
  puts "Scanning..."
  client.filter(:track => "guardiancrime statme") do |tweet|
    if tweet.geo
      lat = tweet.geo.coordinates[0]
      long = tweet.geo.coordinates[1]
      puts "@#{tweet.user.screen_name} #{lat}, #{long}: #{tweet.text}"
      client = Twitter::REST::Client.new do |config|
        config.consumer_key = ""
        config.consumer_secret = ""
        config.access_token = ""
        config.access_token_secret = ""
      end 
      client.update("@#{tweet.user.screen_name} hello!")
      puts "Threat neutralized."
      puts "Scanning..."
    end
  end
end