twitter-log $1 > "$1.txt"
python parse_tweet.py "$1.txt"
mv "$1_parsed.txt" sample_userdata
rm "$1.txt"