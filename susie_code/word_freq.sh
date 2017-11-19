twitter-log $1 > "$1.txt"
python bag-of-words.py "$1.txt" common_words.txt
mv "$1_BOW.txt" results
rm "$1.txt"