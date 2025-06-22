import time
import concurrent
import numpy as np
import pandas as pd
from embeddings.embedding_similarity_search import VectorSimilaritySearch
from llm.LLM_integration import generate_response




def process_and_answer(Query,qdrant,embeddings,sql_db,mongo_db,text_cleaner):

   
    
    ## connect to the databases

    context = ''

    original_query = Query

   
    # text_cleaner.set_text(Query)
    # text_cleaner.process_text()
    # Query =text_cleaner.text
    # print(Query)
    # print('text cleaned')
    ## start timer
    start_time = time.time()
    

    query_embedded = embeddings.embed_documents([original_query])[0]


    ## ids to string
    ids = [str(id) for id in ids]

    #match = qdrant.find_nearest_neighbours_within_ids(query_embedded,ids,limit=2)
    match = qdrant.find_nearest_neighbours(query_embedded,limit=6)
    print(f'match: {match}')
    ids_match = []
    urls = []
    text_content = []
    for e in match:
        ids_match.append(e.payload['document_id'])
        urls.append(e.payload['url'])
        text_content.append(e.payload['section_text'])


    ## delete duplicates
    ids_match = list(set(ids_match))

    content_match = text_content
    print(content_match)

    ## end timer
    end_time = time.time()
    print(f"Time to search: {end_time-start_time}")


    print(urls)
    response = generate_response(original_query,content_match,'')
    sources = "Sources:\n" + "\n".join(urls)



    return response + sources

def llm_agent_researcher(query,embeddings,qdrant):
    ## connect to the databases
    try:
        query_embedded = embeddings.embed_documents([query])[0]
        match = qdrant.find_nearest_neighbours(query_embedded,limit=2)
        ids_match = []
        urls = []
        text_content = []
        score = []

        df = pd.DataFrame(columns=['id','url','text','score'])

        for e in match:
            df = pd.concat([df, pd.DataFrame({'id':e.payload['document_id'],'url':e.payload['url'],'text':e.payload['section_text'],'score':e.score}, index=[0])], ignore_index=True)

            ids_match.append(e.payload['document_id'])
            urls.append(e.payload['url'])
            text_content.append(e.payload['section_text'])
            score.append(e.score)

        ## delete duplicates
        ids_match = list(set(ids_match))

        content_match = text_content

        return_string = f"Query: {query}\n\nResults found:\n\n"
        for url, content in zip(urls, content_match):
            return_string += f"URL: {url}\nContent: {content}\n\n"

        return return_string
    except Exception as e:

        print(f"Error: {e}")
        return None


def multi_llm_agent_researcher(queries:list,embeddings,qdrant):
    '''
    This function takes a list of queries and returns a list of responses
    '''
    responses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(queries)) as executor:
        future_research = {executor.submit(llm_agent_researcher, query, embeddings, qdrant): query for query in queries}
        for future in concurrent.futures.as_completed(future_research):
            query = future_research[future]
            try:
                response = future.result()
                responses.append(response)
            except Exception as exc:
                print(f'Query {query} generated an exception: {exc}')
                responses.append(None)
    return responses



def full_agent_research_response(query,embeddings,qdrant,ai_agent):
    '''
    This function takes a query and returns a response from the LLM
    '''
    start = time.time()
    print(f"Starting research for query: {query}")
    queries = ai_agent.generate_queries(query)
    print(f'lenght of queries: {(queries)}')
    print()
    if len(queries) > 0 :
        knowledge = multi_llm_agent_researcher(queries,embeddings,qdrant)
    else:
        print("No need for research")
        knowledge = []
    print(f"Knowledge: {knowledge}")

    ## generate copies of ai_agent for each query
   

    # if len(knowledge) > 0:
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=len(knowledge)) as executor:
    #         future_research = {executor.submit(generate_response, query, knowledge,''): query for query in knowledge}
    #         for future in concurrent.futures.as_completed(future_research):
    #             query = future_research[future]
    #             try:
    #                 response = future.result()
    #                 answers.append(response)
    #             except Exception as exc:
    #                 print(f'Query {query} generated an exception: {exc}')

    
    # # formatted_answers = "\n".join([f"Sub-research:\n{knowledge_item}\n\nAnswer:\n{answer}\n" for knowledge_item, answer in zip(knowledge, answers)])
    # formatted_answers = "\n".join([f"Question:\n{question}\n\nAnswer:\n{answer}\n" for answer,question in zip(answers,queries)])


    ## final response 
    final_answer = ai_agent.final_answer(query,knowledge)
    end = time.time()
   
    print(f"Time taken: {end - start}")

    return final_answer

    
        

    

 