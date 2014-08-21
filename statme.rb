Dir.chdir("/path/to/directory")

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
          File.open("new.jpg", 'w+')
    end
    client = Twitter::REST::Client.new do |config|
      config.consumer_key = ""
      config.consumer_secret = ""
      config.access_token = ""
      config.access_token_secret = ""
    end 
    if tweet.place.full_name?
      puts "Waiting for image generation."
      while File.file?("ready.jpg") == false
        sleep(1)
      end
      puts "Image generated successfully."
      client.update_with_media("@#{tweet.user.screen_name}", File.new("/path/to/directory/location.jpg"), :place_id => "7b93be1d864cedbb")
      File.delete("location.jpg", "ready.jpg")
      puts "Threat neutralized."
      puts "Scanning..."
    else
      puts "No location provided by user."
      puts "Scanning..."
    end
  end
end