# Deploy Django no PythonAnywhere - Passo a Passo

## Pré-requisitos
- Conta no PythonAnywhere (gratuita ou paga)
- Projeto Django configurado localmente
- Repositório Git (GitHub, GitLab, etc.)

## 1. Limpeza do Ambiente PythonAnywhere

Se você já tem dados no PythonAnywhere e quer limpar tudo:

### Opção A: Limpeza Completa
```bash
# No Bash console do PythonAnywhere
rm -rf ~/*
rm -rf ~/.*
rm -rf /tmp/*
```

### Opção B: Limpeza Específica
```bash
# Deletar apenas o projeto antigo
rm -rf <nome-do-projeto>
rm -rf ~/.virtualenvs/<nome-do-env>
```

## 2. Configurar Repositório Git

### 2.1 Fazer push do projeto para GitHub
```bash
git add .
git commit -m "Preparando projeto para deploy"
git push origin main
```

### 2.2 Verificar se todos os arquivos estão no repositório:
- `requirements.txt`
- `manage.py`
- Pasta do projeto (`config/`)
- Apps (`compras/`)

## 3. Configurar PythonAnywhere

### 3.1 Fazer clone do repositório
No Bash console do PythonAnywhere:
```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

### 3.2 Criar Virtual Environment
```bash
# Criar virtual environment
mkvirtualenv --python=/usr/bin/python3.10 venv

# Ativar (se já não estiver ativo)
workon venv

# Instalar dependências
pip install -r requirements.txt
```

### 3.3 Configurar Variáveis de Ambiente
No Bash console:
```bash
# Adicionar ao ~/.bashrc
echo 'export DJANGO_SETTINGS_MODULE="config.settings"' >> ~/.bashrc
echo 'export DEBUG="False"' >> ~/.bashrc
echo 'export SECRET_KEY="sua-chave-segura-aqui"' >> ~/.bashrc
echo 'export PYTHONANYWHERE_USER="seu-usuario-pa"' >> ~/.bashrc

# Recarregar bashrc
source ~/.bashrc
```

## 4. Configurar Banco de Dados

### 4.1 Criar banco de dados
```bash
# Migrar banco de dados
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser
```

### 4.2 Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

## 5. Configurar Web App

### 5.1 Criar Web App
1. Vá para "Web" tab no PythonAnywhere
2. Clique "Add a new web app"
3. Escolha "Manual configuration"
4. Selecione Python 3.10
5. Deixe o resto como padrão

### 5.2 Configurar WSGI
No campo "WSGI configuration file", edite o arquivo para:

```python
import os
import sys

# Adicionar o projeto ao path
path = '/home/SEU-USUARIO/SEU-REPOSITORIO'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Importar WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5.3 Configurar Virtual Environment
No mesmo arquivo WSGI, adicione antes do import:
```python
# Ativar virtual environment
activate_this = '/home/SEU-USUARIO/.virtualenvs/venv/bin/activate'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))
```

### 5.4 Configurar Static Files
Na "Web" tab:
- **Static files**: `/static/` -> `/home/SEU-USUARIO/SEU-REPOSITORIO/staticfiles`
- **Media files**: `/media/` -> `/home/SEU-USUARIO/SEU-REPOSITORIO/media`

## 6. Configurar Domínio

### 6.1 Configurar ALLOWED_HOSTS
No settings.py, já está configurado para aceitar o domínio automaticamente.

### 6.2 Testar
1. Salve as configurações da Web app
2. Clique em "Reload" na Web tab
3. Acesse `https://SEU-USUARIO.pythonanywhere.com`

## 7. Configurar Cron Jobs (Opcional)

Se precisar de tarefas agendadas:
1. Vá para "Tasks" tab
2. Configure o comando e horário desejado
3. Exemplo para backup diário:
   ```bash
   cd /home/SEU-USUARIO/SEU-REPOSITORIO && python manage.py backup
   ```

## 8. Comandos Úteis

### Verificar logs
```bash
tail -f /var/log/apache2/error.log
```

### Reiniciar web app
```bash
touch /var/www/SEU-USUARIO_pythonanywhere_com_wsgi.py
```

### Atualizar projeto
```bash
cd ~/SEU-REPOSITORIO
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/SEU-USUARIO_pythonanywhere_com_wsgi.py
```

## 9. Troubleshooting

### Erro 500 - Internal Server Error
- Verifique os logs em `/var/log/apache2/error.log`
- Confirme se o virtual environment está ativado
- Verifique se as variáveis de ambiente estão configuradas

### Arquivos estáticos não carregam
- Execute `python manage.py collectstatic --noinput`
- Verifique as configurações de static files na Web tab
- Confirme se `STATIC_ROOT` está correto

### Banco de dados não funciona
- Verifique se as migrations foram aplicadas
- Confirme se o banco de dados tem permissões corretas
- Para SQLite, verifique se o arquivo `.sqlite3` existe

## 10. Segurança

### Mudar SECRET_KEY
```python
# Gerar nova chave
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Configurar DEBUG=False
```bash
export DEBUG="False"
```

### Backup regular
- Configure cron jobs para backup do banco de dados
- Mantenha cópias do código no GitHub

---

## Resumo Rápido

1. Limpar ambiente PythonAnywhere (se necessário)
2. Fazer push do projeto para GitHub
3. Clonar repositório no PythonAnywhere
4. Criar virtual environment e instalar dependências
5. Configurar variáveis de ambiente
6. Migrar banco de dados e coletar static files
7. Configurar Web app com WSGI
8. Configurar static/media files
9. Testar e fazer reload

Seu projeto estará disponível em: `https://SEU-USUARIO.pythonanywhere.com`
