import json
import time
import datetime
import calendar

# convert txt to dictionary
tweets = []
with open('../tweet_input/tweets.txt') as tweetfile:
    lines = tweetfile.readlines()
    for item in lines:
        tweet = json.loads(item)
        tweets.append(tweet)

# preparation for calculation and output 
dict = {}
result = ""
output = open('../tweet_output/output.txt','w')

# set most current time
max_time = calendar.timegm(time.strptime(tweets[0]["created_at"],"%a %b %d %H:%M:%S +0000 %Y"))

# process each tweet in input file
for tweet in tweets:
    # obtain time info
    created_at = tweet["created_at"]
    current_time = calendar.timegm(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y"))
    max_time = max(max_time, current_time)
    
    # continue if time satisfies 60 secconds window
    if max_time - current_time > 60:
        continue
    else:
        # set up edges for each hashtag
        for idx,hashtag in enumerate(tweet["entities"]["hashtags"]):
            current_hashtag = hashtag["text"]

            if current_hashtag not in dict:
                dict[current_hashtag]={}
            for i in tweet["entities"]["hashtags"][idx+1:]:
                hashtag_i = i["text"]
                if hashtag_i not in dict:
                    dict[hashtag_i]={}
                if hashtag_i not in dict[current_hashtag]:
                    dict[current_hashtag][hashtag_i] = current_time
                    dict[hashtag_i][current_hashtag] = current_time
                else:
                    old_time = dict[current_hashtag][hashtag_i]
                    dict[current_hashtag][hashtag_i] = max(old_time,current_time)
                    dict[hashtag_i][current_hashtag] = max(old_time,current_time)
    
    # degree calculation
    degree = 0
    null_dict = []
    for tag in dict:

        # clean expired edges
        null_dict_expired = []
        for sub_tag in dict[tag]:
            if max_time - dict[tag][sub_tag] >60:
                null_dict_expired.append(sub_tag)
            else:
                degree += 1
                
        for null_dict_expired_tag in null_dict_expired:
            dict[tag].pop(null_dict_expired_tag, None)
            dict[null_dict_expired_tag].pop(tag, None)
            
        if len(dict[tag]) == 0:
            null_dict.append(tag)
    
    # clean expired hashtag entries
    for null_dict_tag in null_dict:
        dict.pop(null_dict_tag, None)
    
    # result calculation        
    avg_degree = degree/len(dict)
    result = (str(round(avg_degree,2))+ "\n")
    
    # write result in output    
    output.write(result)

