require 'rubygems'
require 'twitter'
# require 'sinatra'
# require 'chatterbox/dsl'

# TwitterStats
begin

# Configuration
client = Twitter::REST::Client.new do |config|
  config.consumer_key = ""
  config.consumer_secret = ""
  config.access_token = ""
  config.access_token_secret = ""
end

=begin

this is what i found originally https://github.com/miguelgraz/TwitterBot

get '/update' do
  update
  puts 'updated'
end

@last = 480737441985212416
def update
  update_last = true
  CLIENT.search('" guardiancrime " -rt', since_id: @last, result_type: "recent").take(5).collect do |tweet|
    if update_last
      @last = tweet.id
      update_last = false
    end
    reply = "@#{tweet.user.screen_name} hello!"
    puts "posting #{reply}" if reply.size <= 140
    CLIENT.update(reply, in_reply_to_status: tweet) if reply.size <= 140
    sleep 120
  end
end
=end

=begin

this one uses chatterbox... a little simpler https://github.com/muffinista/chatterbot

replies do |tweet|
  reply "#USER# Thanks for contacting me!", tweet
end
=end

client.update("I'm tweeting with @gem!")

end

=begin
repo for twitter gem is here https://github.com/sferik/twitter
twitter api is dev.twitter.com
=end

