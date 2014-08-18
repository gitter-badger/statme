require 'rubygems'
require 'twitter'

# TwitterStats
begin

# Configuration
client = Twitter::Streaming::Client.new do |config|
  config.consumer_key = "kao1cND8RFCHcUJeb5xONcsZQ"
  config.consumer_secret = "7L6jS0vRnqVVT9WpH7BZ3jPvrYgmd3XinK3tScVEov48wDgzeg"
  config.access_token = "2199777559-2Eetn8D3VvuLkVKPvWsUA1jNaIgMoDu9F0gBZCT"
  config.access_token_secret = "7V14U9JLsKEHvdAMpwrqDNuQsVuOnFUGgrO106b6GIOMS"
end

client.filter(:track => "@guardiancrime") do |tweet|
  puts tweet.text
end

end