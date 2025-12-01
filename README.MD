Para rodar o projeto é necessario ter o python 10 instalado.
Instalar também o streamlit experta e groq com o comando: pip install streamlit experta groq python-dotenv.
Para rodar o projeto rodar no terminal o comando: streamlit run app.py
Criar o arquivo .env na raiz do projeto e colocar a chave do groq 
porta do navegador http://localhost:8501

Caso apresente o erro: AttributeError: module 'collections' has no attribute 'Mapping'  para rodar o projeto, referente ao streamlit, fazer o seguinte, rodar os comandos a baixo:

pip uninstall -y frozendict
pip install frozendict==2.3.10
pip install experta --no-deps
pip install frozendict==2.3.10
