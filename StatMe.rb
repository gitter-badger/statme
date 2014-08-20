Dir.chdir("/file/location")

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
    puts "@#{tweet.user.screen_name}: #{tweet.text}"
    if tweet.place.full_name?
      puts tweet.place.full_name
        if File.file?("location.txt")
          File.delete("location.txt")
        end
          File.open("location.txt", 'w+') {|f| f.write(tweet.place.full_name.to_s) }
    end
    client = Twitter::REST::Client.new do |config|
      config.consumer_key = ""
      config.consumer_secret = ""
      config.access_token = ""
      config.access_token_secret = ""
    end 
    if tweet.place.full_name?
      client.update("@#{tweet.user.screen_name} hello!")
      puts "Threat neutralized."
      puts "Scanning..."
    else
      puts "No location provided by user."
      puts "Scanning..."
    end
  end
end