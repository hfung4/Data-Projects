# Health behaviour guru webapp

## Technologies used:

Python, Streamlit, deployed on Heroku (**Link to the [app](https://behaviourial-science-guru-d2520d92ce6e.herokuapp.com/)**)

## Description

Used [LangChain](https://www.langchain.com/) to build a simple LLM chatbot for answering questions related to:

- Takeda survey data

- Very specific health/drug related questions that requires searching through academic journals in PubMed

- General questions that can be answered with search engines such as DuckDuckGo

- We use [agents](https://python.langchain.com/docs/modules/agents/) (a component of LangChain), which are modular “expert” tools that are targeted for specific task

  Several agents were used for the app, which is built in Streamlit, containerized in Docker, and Deployed with Github Action on Heroku (or AWS ECS)

- DuckDuckGo Search

- Calculator

- PubMed Search

- Takeda Survey Data

## Setup

- Fork the repository

- Set up a virtual environment on your local machine and pip install the requirements.txt

- Install the Heroku CLI (command line interface) [The Heroku CLI | Heroku Dev Center](https://devcenter.heroku.com/articles/heroku-cli)

- Go to [Heroku](https://dashboard.heroku.com/apps) (register if you haven't)

- Click `New` and then `Create New App`

- Give it a name and click `Create`

- Choose your repository

- Click `Enable Automatic Deploys`. Now, anytime you push to Github, your code will be automatically deployed to Heroku!