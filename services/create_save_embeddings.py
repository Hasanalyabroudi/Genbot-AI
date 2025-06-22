from embeddings.CreateEmbedding import CreateEmbedding



def save_embeddings(url_id,url_corpus,mongo_db):
    mongo_db.connect()
    embeddings = CreateEmbedding(url_corpus)

    
    mongo_db.add_element("embeddings",embeddings)
    mongo_db.update_element(url_id)
    mongo_db.close_connection()

    return embeddings