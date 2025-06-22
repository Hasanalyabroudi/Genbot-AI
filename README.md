# Genbot AI – Chatbot Builder
  
## Project Description  
This project aims to develop a system that can build custom AI chatbots based on the content of a given website. It comprises of four major components: a web scraper/crawler, a database, a search engine, and language model (LLM) integration.  
  
## Goals  
The primary goal of this project is to design a system that automates the process of creating an AI chatbot by utilizing the available information on a website. This will reduce the need for manual input and coding, making it easier to create a chatbot for any website.  
  
## Project Components  
  
### Web Scraper/Crawler  
The first part of the algorithm is the web scraper/crawler. Given a base URL, for example, uottawa.ca, this component will navigate through the website and find all the pages. It will then scrape the content for further use.  
  
### Database  
The second part of the project is the database, where all the scraped data gets organized. The data is stored in a tree-based database and arranged appropriately to facilitate easy access and search.  
  
### Search Engine  
The third component is the search engine. This is the core of the system, responsible for searching the database to find the parts that answer a user's query. For instance, if the question is "how many years in software engineering", the search engine will scan the database and return the content from the software engineering page.  
  
### LLM Integration  
The fourth and final part is the LLM integration. Once a user asks a question and the search engine finds the part that has the answer, a language model is prompted with both the query and answer. It is then asked to answer the question based on the search engine result.  
  
## Objectives  
The project's objectives are to:  
- Automate the process of creating AI chatbots for customers, reducing the need for manual input and coding.  
- Deliver a system that can navigate a given website, extract information, and generate a database.  
- Create a search engine that can scan this database and find relevant answers to user queries.  
- Integrate a language model that can formulate responses to these queries.  
The success of the project will be measured by the efficiency and accuracy of the chatbot in understanding and responding to user queries.  
  
## Anticipated Risks  
Some of the engineering challenges anticipated include:  
- Efficient and comprehensive web scraping: The system needs to navigate and extract information from complex and diverse website structures.  
- Database organization: Efficiently organizing and storing a large amount of data.  
- Search accuracy: The search engine must be able to accurately and quickly locate relevant information in response to a query.  
- Language model integration: The language model must be able to understand the context and formulate an accurate and relevant response.  
  
## Legal and Social Issues  
The project will adhere to all legal requirements regarding data privacy and web scraping. Any information scraped from a website will be used solely for the purpose of creating the chatbot and will not be shared or used for any other purpose. Socially, this project aims to improve user interaction with websites, making information retrieval more interactive and efficient.  
 
This innovative project combines various aspects of AI, web scraping, and database management. The end goal is to create a system that can generate a customized AI chatbot for any given website.
