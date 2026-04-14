PROJETO DJANGO - COMPRAS MENSAIS

PASSOS RÁPIDOS:

1) Criar e ativar ambiente virtual
Windows:
py -m venv .venv
.venv\Scripts\activate

2) Instalar Django
pip install "Django>=5.2,<5.3"

3) Entrar na pasta do projeto
cd output\projeto_mercado_rapido

4) Criar tabelas
python manage.py makemigrations
python manage.py migrate

5) Rodar servidor
python manage.py runserver

6) Abrir no navegador
http://127.0.0.1:8000/

OBSERVAÇÕES:
- Sem login, para uso pessoal rápido.
- Banco SQLite incluso pela configuração.
- Pode cadastrar listas mensais, adicionar itens, marcar/desmarcar comprado e excluir item.
