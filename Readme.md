TO RUN THE CURRENT CODE

1) cd SmartFactoryProject
2) py -m venv .venv  (Run this locall, becasue it will not pushed)
3) venv\Scripts\activate (Then activate it locally)
4) create .env file and this  
  * SHELLSMITH_BASYX_ENV_HOST=http://92.205.177.115:8080
  * GROQ_API_KEY= add_your_groq_Api here
4) pip install -r requiremnts.txt (install needed package)
5) aas-mcp (run mpc Server in one terminal)
6) run the client now in other terminal. For example "python llm\agent.py" 
