# Checklist Deploy PythonAnywhere - Projeto Mercado Rápido

## ✅ Arquivos Essenciais Presentes
- [x] `manage.py` 
- [x] `requirements.txt` (atualizado com Django 4.2.16 e gunicorn)
- [x] `config/settings.py` (configurado para produção)
- [x] `config/wsgi.py` 
- [x] `config/urls.py`
- [x] App `compras/` completo
- [x] Templates em `templates/`
- [x] Arquivos estáticos em `static/`
- [x] Migrations em `compras/migrations/`

## ✅ Configurações de Produção
- [x] `SECRET_KEY` via variável de ambiente
- [x] `DEBUG` configurado via variável de ambiente  
- [x] `ALLOWED_HOSTS` configurado para PythonAnywhere
- [x] `STATIC_ROOT` e `MEDIA_ROOT` configurados
- [x] Configurações de segurança para produção

## ✅ Banco de Dados
- [x] SQLite configurado (funciona bem em PythonAnywhere)
- [x] Migrations aplicadas localmente
- [x] Schema atualizado com modelo Categoria

## ⚠️ Ações Necessárias ANTES do Deploy

### 1. Fazer push para GitHub
```bash
git add .
git commit -m "Preparando projeto para deploy PythonAnywhere"
git push origin main
```

### 2. Gerar SECRET_KEY para produção
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Criar script de setup para PythonAnywhere
Criar arquivo `setup_pythonanywhere.sh` com comandos automatizados

## 🚀 Passos no PythonAnywhere

### 1. Configurar Ambiente
```bash
# Clonar repositório
git clone https://github.com/SEU-USUARIO/projeto_mercado_rapido.git
cd projeto_mercado_rapido

# Criar virtual environment
mkvirtualenv --python=/usr/bin/python3.10 mercado_rapido

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
```bash
# Adicionar ao ~/.bashrc
echo 'export DJANGO_SETTINGS_MODULE="config.settings"' >> ~/.bashrc
echo 'export DEBUG="False"' >> ~/.bashrc
echo 'export SECRET_KEY="SUA-CHAVE-GERADA-AQUI"' >> ~/.bashrc
echo 'export PYTHONANYWHERE_USER="SEU-USUARIO-PA"' >> ~/.bashrc

source ~/.bashrc
```

### 3. Configurar Banco de Dados
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Configurar Web App
- Criar manual web app (Python 3.10)
- Configurar WSGI path
- Configurar static files
- Configurar virtual environment

## 🔧 Configuração WSGI Necessária

Arquivo: `/var/www/SEU-USUARIO_pythonanywhere_com_wsgi.py`

```python
import os
import sys

# Adicionar projeto ao path
path = '/home/SEU-USUARIO/projeto_mercado_rapido'
if path not in sys.path:
    sys.path.append(path)

# Ativar virtual environment
activate_this = '/home/SEU-USUARIO/.virtualenvs/mercado_rapido/bin/activate'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Importar WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 📁 Estrutura de Static Files

Na Web tab do PythonAnywhere:
- **Static URL**: `/static/`
- **Static Directory**: `/home/SEU-USUARIO/projeto_mercado_rapido/staticfiles`

## 🔄 Comandos de Atualização

```bash
cd ~/projeto_mercado_rapido
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/SEU-USUARIO_pythonanywhere_com_wsgi.py
```

## ⚠️ Pontos de Atenção

1. **ALLOWED_HOSTS**: Precisa incluir seu domínio PythonAnywhere
2. **SECRET_KEY**: Use uma chave diferente da local
3. **DEBUG=False**: Essencial para produção
4. **Static Files**: Execute collectstatic após atualizações
5. **Migrations**: Execute migrate se houver alterações no DB

## 🎯 Status Atual: PRONTO PARA DEPLOY

O projeto está 95% pronto para deploy no PythonAnywhere. 
Falta apenas:
- Push para GitHub
- Configurar variáveis de ambiente no PA
- Criar web app e configurar WSGI
