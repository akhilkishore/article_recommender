from textblob import TextBlob
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import stopwords  
stop_words = set(stopwords.words('english'))  
from nltk.tokenize import word_tokenize  
model = SentenceTransformer('msmarco-distilroberta-base-v2')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import logging

#from gensim.summarization import keywords


def add_info_log(message):
    """
    Used to add log (info) into the log file
    
    Parameters
    ----------
        message (string):
            Content to add in the log

    Returns
    -------
        Returns nothing

    """
    logging.info(message)

def get_bert_embedings_for_text(text):
    """
        Get distilRoBERTa Embeddings for given text

        parameters
        ----------
            text (string):
                document as string
        returns
        -------
            tensor

    """
    return model.encode(text)

def get_similarity_score(embeding_one, embeding_two):
    """
        Returns the cosine similarity btw two tensors

        parameters
        ----------
            embeding_one (Tensor):
                tensor data
            embeding_two (Tensor):
                tensor data
        returns
        -------
            tensor
    """
    return util.pytorch_cos_sim(embeding_one, embeding_two).item()

def get_noun_phrases(text):
    # word_tokens = word_tokenize(text)  
    # filtered_sentence = [w for w in word_tokens if not w in stop_words]  
    # text = " ".join(filtered_sentence)
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    blob = TextBlob(text)
    return blob.noun_phrases  


def get_ngrams_list(text):
    blob = TextBlob(text)
    blob.ngrams(n=3)

