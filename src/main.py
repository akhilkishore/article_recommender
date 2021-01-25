from nlp_engine import NlpEngine 
import logging
import logging.config

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)


if __name__ == "__main__" :

    query = "Machine Learning"
    
    
    print("Processing... ")
    obj = NlpEngine(query)


    result = obj.get_result()

    print("##########################################")
    print("search query is : ", query)
    for count,item in enumerate(result.keys()):
        if count == 5:
            break
        print("________________________________________")
        print("Link to the article: ", item)
        print("________________________________________")
        print("Related keywords : ",result[item])
        print("\n \n")

    print("##########################################")