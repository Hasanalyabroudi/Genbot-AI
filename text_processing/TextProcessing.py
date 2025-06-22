import re
import uuid
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect  
from nltk.stem import WordNetLemmatizer   
from simplemma import lemmatize
import string
from unidecode import unidecode
import spacy
import unicodedata
import pandas as pd



nlp_fr = spacy.load('fr_core_news_md')
nlp_fr.max_length = 2000000

nlp_en = spacy.load('en_core_web_md')
nlp_en.max_length = 2000000
  
# nltk.download('wordnet')

class TextProcessing:
    def __init__(self):
        self.text = ''

    def detect_language(self):
        try:
            lang_code = detect(self.text)
            if lang_code == 'en':
                return 'english'
            elif lang_code == 'fr':
                return 'french'
            else:
                return 'english'
        except:
            return 'english'
    
    def text_lower(self):
        self.text = self.text.lower()
        return self.text.lower()
    
    
    def remove_non_words(self):
        self.text = re.sub(r'[^\w\s]', '', self.text)
        return self.text
    
    def remove_digits(self):
        self.text = re.sub(r'\d', '', self.text)
        return self.text
    
    def remove_punctuation(self):
        # self.text = re.sub(r'[^\w\s]', '', self.text)

        # self.text = "_".join([char for char in self.text if char not in string.punctuation])  
        text = ([char for char in self.text if char in string.punctuation])
        for e in text:
            text = list(set(text))
            self.text = self.text.replace(e, ' ')

        return self.text
            

    def remove_accent(self):
        self.text = "".join(
            c
            for c in unicodedata.normalize("NFD", self.text)
            if unicodedata.category(c) != "Mn"
        )

        return self.text
    
    def tokenize_text(self):
        self.text = word_tokenize(text=self.text, language=self.language)
        return self.text
    
    def remove_stopwords(self):
        
        if self.language == 'english':
            stop_words = set(stopwords.words('english'))
        elif self.language == 'french':
            stop_words = set(stopwords.words('french'))
        else:
            print('language not supported for stopwords removal')

            stop_words = set(stopwords.words('english'))
            words = word_tokenize(self.text)
            self.text = ' '.join([word for word in words if word.lower() not in stop_words])

            stop_words = set(stopwords.words('french'))
            words = word_tokenize(self.text)
            self.text = ' '.join([word for word in words if word.lower() not in stop_words])

            return self.text


        words = word_tokenize(self.text)
        self.text = ' '.join([word for word in words if word.lower() not in stop_words])
        return self.text
    
    def lemmatize_text(self):
        self.text = self.text.lower()
        if self.language == 'english':
            text = nlp_en(self.text)

        elif self.language == 'french':
            text = nlp_fr(self.text)

        else:
            print(f'language not supported for lemmatization: {self.language}')
            text = nlp_en(self.text)
            return self.text

        self.text =  ' '.join([token.lemma_ for token in text])
        return self.text
    
    def CreateWordFrequencyMatrix(self):
        words = word_tokenize(self.text)
        words = list(set(words))
        
        df = pd.DataFrame(columns=['words','frequency'])
        for word in words:
            count = self.text.count(word)
            df.loc[len(df)] = [ word, count]
            
            # df.loc[df['words'] == word, 'frequency'] = count
        return df
        
    def validate_no_punctuation(self):
        ponctuation = [char in string.punctuation for char in self.text]
        print(ponctuation)
        return any(char in string.punctuation for char in self.text)


    def process_text(self,current_try=0):
        self.text_lower()
        self.remove_punctuation()
        self.remove_stopwords()
        self.remove_accent()
        # if self.validate_no_punctuation() and current_try < 3:
        #     print('Text still contains punctuation, trying again ... ')
        #     return self.process_text(current_try+1)
        # self.remove_digits()
        self.lemmatize_text()
        # self.tokenize_text()
        return self
    
    def set_text(self, text):
        self.text = text
        self.original_text = text
        self.language = self.detect_language()
        
    
    def __str__(self):
        if isinstance(self.text, list):
            return ' '.join(self.text)
        return self.text
    








# text = TextProcessing()
# text.set_text("This is just a sample text for the purpose of cats abondonné, être")

# text = text.process_text()
# print(text.text)

