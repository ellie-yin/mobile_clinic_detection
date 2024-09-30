Working with Harvard Family Van team to
* collect data on (potential) mobile health clinics
* predict whether or not something is a mobile health clinic

This is duplicated from a private github for this project. Sensitive files have been removed, 

3 folders:
* feature_extraction
  * testing_similarity.py returns the most similar words to a given word. only works for words in the model already
  * cleaning_data.py: notes of things someone might want to change (file name etc) at top of script
    * takes about 4 minutes to run, 3 of this is writing the excel file.
    * uses Word2Vec vectors to handle text features
      * must delete w2v_models folder (inside feature_extraction) if someone wants to regenerate the vocabulary the Word2Vec uses 
      * can check the words embeddings it creates + their values by uncommenting out the word_embeddings code (near the end of the file)
* new_recipient_cleaning
  * the website_extractor.py file finds contact email and websites for candidate clinics via the googlesearch package
  * find_duplicates.py sees if the new list has duplicate organization names as the master spreadsheet and removes them if so 
* logistic_reg
	* logistic_reg.py trains a logistic regression model to classify entries as mobile health clinics or not 



TODO/FURTHER THINGS TO EXPLORE
* confidence threshold of 80% on the new recipients
* similar words for those not in the corpus/extend the corpus
* in cleaning_data.py, play with embedding dimension for Word2Vec (currently 50)
* add EIN back in to model input
