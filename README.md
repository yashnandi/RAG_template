# Genie-Agentic-RAG
A minimal GPT-RAG chatbot repo. For example, if developing a chatbot that answers questions on PySpark, all related material can be added
to knowledge base and the app can be developed. 

# Sections that need to be edited.
![.env file - 1. Add OPENAI API KEY 2. Model such as gpt-4o-mini 3. GENIE_BUILD_INDEX = 0 if chunking already done, GENIE_BUILD_INDEX = 1 if chunking needs to be done (online).](./images/env.png)

![knowledge base - Add your pdfs, industry expert notes and code files here](./images/kb.png)

![Embedding model for RAG - Chunking and retrieval](./images/config.png)

![Your Prompt template](./images/prompt.png)

![Edit index.html in frontend. Add location of images of your organisation and language.](./images/index.png)

# List of supplementary folders/codes not used for the minimal app development and launch. (Useful for app upgrade)
./src/genie/cli
./src/genie/frontend/routes/batch
./src/genie/frontend/routes/eval
# RAG_template
