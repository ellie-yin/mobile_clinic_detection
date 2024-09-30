from gensim.models import Word2Vec

# if you have a saved model: 
model_path = 'Org Name_model.model' # CHANGE MODEL BASED ON THE ONE YOU WANT TO LOOK AT
model = Word2Vec.load(model_path)
print(f"Model loaded from {model_path}")

# word you're looking to find similar words for
word = 'Jessie'

def get_most_similar_words(model, word, topn=10):
    if word in model.wv.key_to_index:
        similar_words = model.wv.most_similar(word, topn=topn)
        return similar_words
    else:
        return f"Word '{word}' not found in the vocabulary."

similar_words = get_most_similar_words(model, word)
print(f"Most similar words to '{word}':")
if isinstance(similar_words, str): 
    print(similar_words) # prints the 'not found' error
else: 
    for similar_word, score in similar_words: # prints tuple of the (word, score) for top 10 similar words
        print(f"{similar_word}: {score}")

# example results: 

# Model loaded from Org Name_model.model
# Most similar words to 'clinic':
# medical: 0.9981817603111267
# of: 0.9981126189231873
# mobile: 0.997978687286377
# hospital: 0.9978981614112854
# health: 0.9978715777397156
# inc: 0.997845470905304
# and: 0.9977644085884094
# the: 0.9976486563682556
# center: 0.9975115060806274
# for: 0.9970736503601074

# Model loaded from Org Name_model.model
# Most similar words to 'health':
# and: 0.9989345073699951
# of: 0.9987446069717407
# center: 0.9987345933914185
# hospital: 0.9986206889152527
# inc: 0.9985927939414978
# for: 0.9985376000404358
# mobile: 0.9984998106956482
# the: 0.9984503388404846
# medical: 0.9983956813812256
# clinic: 0.997871458530426

# Model loaded from Org Name_model.model
# Most similar words to 'john':
# incorporated: 0.9456533193588257
# vincent: 0.94172203540802
# louis: 0.9406461715698242
# the: 0.9387851357460022
# association: 0.9384685158729553
# central: 0.9379059076309204
# cancer: 0.9378566145896912
# mary: 0.9378319978713989
# council: 0.9377762079238892
# at: 0.9375839829444885

# Model loaded from Org Name_model.model
# Most similar words to 'family':
# the: 0.9964994192123413
# of: 0.9960427284240723
# health: 0.996017336845398
# medical: 0.995678186416626
# center: 0.9956667423248291
# and: 0.9955787062644958
# clinic: 0.9952282309532166
# inc: 0.995173454284668
# hospital: 0.9949252009391785
# mobile: 0.9948486089706421

# Model loaded from Org Name_model.model
# Most similar words to 'and':
# health: 0.9989343881607056
# center: 0.998591423034668
# inc: 0.9985821843147278
# hospital: 0.9983585476875305
# of: 0.9983322024345398
# medical: 0.9980987310409546
# for: 0.9980496168136597
# mobile: 0.9979113340377808
# the: 0.997882604598999
# clinic: 0.9977644085884094

# Model loaded from Org Name_model.model
# Most similar words to 'alameda':
# augusta: 0.5123097896575928
# rutgers: 0.4431731104850769
# bsa: 0.4357595145702362
# edmond: 0.41141003370285034
# saline: 0.40620729327201843
# guy: 0.38505783677101135
# coffey: 0.3615211248397827
# widowed: 0.3603391945362091
# sterling: 0.35357534885406494
# diley: 0.3477223217487335

# Model loaded from Org Name_model.model
# Most similar words to 'Jessie':
# Word 'Jessie' not found in the vocabulary.