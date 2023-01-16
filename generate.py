import os
import sys
import tweepy

consumer_key = os.environ.get("TWITTER_API_KEY", "")
consumer_secret = os.environ.get("TWITTER_API_SECRET_KEY", "")
oauth_token = os.environ.get("TWITTER_ACCESS_TOKEN", "")
oauth_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")


logstash_conf_input = '''input { 
    twitter {
        consumer_key => "%s"
        consumer_secret => "%s"
        oauth_token => "%s"
        oauth_token_secret => "%s"
        follows => ["%s"]
        type => stream
    }
} 
'''
logstash_conf_filter = '''filter {
    if [type] == "stream" {

        if ([hashtags]) {
            ruby {
                code => '    
                i = 0
                event.get("[hashtags]").each {|hash|
                    if event.get("hashtags_text")
                        event.set("[hashtags_text]", event.get("hashtags_text") + [event.get("[hashtags][#{i}][text]").downcase])
                    else
                        event.set("[hashtags_text]", [event.get("[hashtags][#{i}][text]").downcase])
                    end
                    i += 1
                }'
            }
        }
        mutate{
            remove_field => ["doc", hashtags]
        }
        mutate{
            rename => { "hashtags_text" => "hashtags" }
        }
    }
}'''

logstash_conf_output = '''
output {
    if [type] == "stream" {
        elasticsearch {
            hosts => ["elasticsearch:9200"]
            index => "twitter-%{+YYYY-MM}"
            document_type => "stream"
        }
    }
}
'''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

follower_ids = list(map(str, tweepy.Cursor(api.get_friend_ids, cursor=-1).items()))

print(logstash_conf_input % (consumer_key, consumer_secret, oauth_token, oauth_token_secret, '","'.join(follower_ids)))
print(logstash_conf_filter)
print(logstash_conf_output)
