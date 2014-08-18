require 'rubygems'
require 'twitter'

# TwitterStats
begin

# Configuration
client = Twitter::REST::Client.new do |config|
  config.consumer_key = ""
  config.consumer_secret = ""
  config.access_token = ""
  config.access_token_secret = ""
end

client.update_with_media("I'm tweeting with @gem!", File.new("/path/to/media.png"))

end

=begin
potential classes of use are Twitter:Mention and Twitter:Reply
repo for twitter gem is here https://github.com/sferik/twitter
=end