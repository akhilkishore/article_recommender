import web_scrapper as WebScrapper
import nlp_components as NlpComponents
import operator


class NlpEngine():
    """
        This NLP Engine takes a user input/query and return Documnets based on ranking.
        It's making use of distilRoBERTa embedding to catch the semantic similarity 
    """

    def __init__(self, input_query):
        self.input_query = input_query

        self.validate_query()

        self.processed_data_without_ranking = self.process_text_data()

         
        self.rank_dict, self.keyphrase_dict =  self.rank_documents()


    def validate_query(self):
        """
            Simply validate the user query 
        """
        if self.input_query == None or len(self.input_query) == 0:
            exit("invalid user query")
        else :
            pass

    def get_search_result_from_search_engines(self):
        """
            Search the web using a SE and fetch seed urls for scrapping the initial articles
            #Note : we can perform a recursive scrapping to collected more related articles related to the user query
        """
        links = WebScrapper.search_web_for_links(self.input_query)
        # add log here 
        return links


    def get_text_from_webpage(self,links):
        print("Following URL are being scrapped ")
        return [ {"link":link,"text":WebScrapper.scrap_web_page(link)} for link in links]

    def process_text_data(self):
        links = self.get_search_result_from_search_engines()

        link_text_dictionary_list = self.get_text_from_webpage(links)
        del links 
        complete_processed_data = self.get_document_and_candidate_embeddings(link_text_dictionary_list)
        del link_text_dictionary_list
        return complete_processed_data

         
    def get_document_and_candidate_embeddings(self, data):
        """
            For Each Webpage :
                A Document Embedding is created
                Noun phrases extracted from the text.
                Embeddings for noun phrases generated 
                Similariy of noun phrases against the doument is fetch to get top related keywords
        """

        complete_processed_data = []

        for count, item in enumerate(data) :
            print("processing text for document : ",count)
            if item['text'] == None or len(item['text'])==0:
                continue
            document_embeddings = NlpComponents.get_bert_embedings_for_text(item['text'])
            noun_phrases = NlpComponents.get_noun_phrases(item['text'])
            keyword_embeddings_dictionary = {}
            for keyword in noun_phrases:
                keyword_embeddings_dictionary[keyword] = NlpComponents.get_bert_embedings_for_text(keyword)
            
            keyword_embeddings_dictionary = self.select_top_keywords_relevant_to_document(document_embeddings, keyword_embeddings_dictionary)
            complete_processed_data.append({'link':item['link'],'document_embeddings':document_embeddings,"keyphrases":keyword_embeddings_dictionary})
            del document_embeddings
            del noun_phrases
            del keyword_embeddings_dictionary 
        return complete_processed_data
         

    def select_top_keywords_relevant_to_document(self, document_embedding ,keyword_embeddings_dictionary ) :
        """
            Compute the similarity btw each keyword/keyphrase with
            its corresponing document to find out how similar it is.
        """
        temp_dictionary = {}

        for key in keyword_embeddings_dictionary.keys():
            score = NlpComponents.get_similarity_score(document_embedding, keyword_embeddings_dictionary[key])
            temp_dictionary[key] = score


        temp = [ temp_dictionary[x] for x in temp_dictionary.keys()]
        f_mean = (max(temp)+ (sum(temp)/len(temp)))/2 
        del temp

        temp_dictionary_temp = {}

        for x in temp_dictionary.keys():
            if temp_dictionary[x] >= f_mean:
                temp_dictionary_temp[x]=temp_dictionary[x]  
    

        
        return temp_dictionary_temp



    def rank_documents(self):
        """
            All top keyphrases fetched for input query is combined into a sentence with coma separation
            Documnet Embeddings for this sentence is generated 
            This Sentence Embeddings is compared agains each and every web page's document embeddings
            Each webpage is sorted based on semantic similarity ( cosine similarity for now )
            
            Returns Ranked article links with related keywords

        """


        sentence = self.combine_keyphrases_into_sentence(self.processed_data_without_ranking)

        sentece_emb = NlpComponents.get_bert_embedings_for_text(sentence)

        rank_dict = {}
        final_dict = {}

        for item in self.processed_data_without_ranking:

            rank_dict[item['link']] = NlpComponents.get_similarity_score(item['document_embeddings'],sentece_emb)
            keywords = [ x for x in  item['keyphrases'].keys()]
            final_dict[item['link']] = keywords

        rank_dict = dict( sorted(rank_dict.items(), key=operator.itemgetter(1),reverse=True))

        # add this into log
        return rank_dict, final_dict
        

    def combine_keyphrases_into_sentence(self, data):
        """
            Combines all top keyphrases into a sentence 
        """
        sentence = []

        for item in data :
            for key in item['keyphrases'].keys():
                sentence.append(key)
        sentence = " ".join(sentence)

        return sentence+" "+self.input_query
        

    def get_result(self):

        result = {}
        for key in self.rank_dict.keys():
            result[key] = self.keyphrase_dict[key]
        return result


