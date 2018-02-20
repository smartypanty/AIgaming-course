# FEATURE EXTRACTION

s = "Kunt u mij dat tonen op de kaart"

ngrams = []
n = 3 # size of the ngrams

# generating character ngrams of size n
for i in range(len(s) - n + 1):
    ngram = s[i:i+n]
    ngrams.append(ngram)
print(ngrams)
# ['Kun', 'unt', 'nt ', 't u', ' u ', 'u m', ' mi', 'mij', 'ij ', 'j d', ' da', 'dat', 'at ', 't t', ' to', 'ton', 'one', 'nen', 'en ', 'n o', ' op', 'op ', 'p d', ' de', 'de ', 'e k', ' ka', 'kaa', 'aar', 'art']



# generating character ngrams of size up to n (1,2,3...n)
ngrams.clear()
for k in range(1, n+1):
    for i in range(len(s) - k + 1):
        ngram = s[i:i+k]
        ngrams.append(ngram)
print(ngrams)
# ['K', 'u', 'n', 't', ' ', 'u', ' ', 'm', 'i', 'j', ' ', 'd', 'a', 't', ' ', 't', 'o', 'n', 'e', 'n', ' ', 'o', 'p', ' ', 'd', 'e', ' ', 'k', 'a', 'a', 'r', 't', 'Ku', 'un', 'nt', 't ', ' u', 'u ', ' m', 'mi', 'ij', 'j ', ' d', 'da', 'at', 't ', ' t', 'to', 'on', 'ne', 'en', 'n ', ' o', 'op', 'p ', ' d', 'de', 'e ', ' k', 'ka', 'aa', 'ar', 'rt', 'Kun', 'unt', 'nt ', 't u', ' u ', 'u m', ' mi', 'mij', 'ij ', 'j d', ' da', 'dat', 'at ', 't t', ' to', 'ton', 'one', 'nen', 'en ', 'n o', ' op', 'op ', 'p d', ' de', 'de ', 'e k', ' ka', 'kaa', 'aar', 'art']



# generating word ngrams of size n
ngrams.clear()
words = s.split(" ") # a list of words, or "tokens"
for i in range(len(words) - n + 1):
    ngram = str1 = ' '.join(words[i:i+k])
    ngrams.append(ngram)
print(ngrams)
# ['Kunt u mij', 'u mij dat', 'mij dat tonen', 'dat tonen op', 'tonen op de', 'op de kaart']
