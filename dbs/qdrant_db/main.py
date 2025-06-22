


from dbs.qdrant_db.db import db

qdrant_db = db("http://52.188.193.108:6333/",'ottawa_ca_db')
qdrant_db.connect()

doc = qdrant_db.search_element_by_(term="document_id",value="b2f373f2-5cbc-453f-bd50-1c3f92458e17")

ids = [element.payload['id'] for element in doc[0]]
print(ids)
# qdrant_db.add_element_to_payload("id",4)
# qdrant_db.add_element_to_payload("url","http://www.uottawa.ca")
# qdrant_db.add_element_to_payload("language","English")
# qdrant_db.add_vector([0.05 for i in range(1000)])  

# qdrant_db.push_to_db()

# # print(qdrant_db.find_nearest_neighbours([0.05 for i in range(1000)]))
# print(qdrant_db.find_nearest_neighbours(limit=10))

# elements = (qdrant_db.find_nearest_neighbours_within_ids([0.05 for i in range(1000)],ids=[2]))
# for element in elements:
#     print(element.payload['url'])
