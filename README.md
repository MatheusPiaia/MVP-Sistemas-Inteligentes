# MVP-Sistemas-Inteligentes

🎲 Instalação
Recomendado iniciar ambiente virtual antes da instalação das dependência/bibliotecas.

Para iniciar ambiente virtual no padrão do python utilizar:

python -m venv env
.\env\Scripts\activate
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal e executar:

pip install -r requirements.txt
Este comando instala as dependências/bibliotecas, descritas no arquivo requirements.txt.

Para executar a API basta executar:

flask run --host 0.0.0.0 --port 5000
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

flask run --host 0.0.0.0 --port 5000 --reload
Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.