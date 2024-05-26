# Readme

## Instalação

### Criação das pastas

1-Criar uma pasta chamada "gestao_pecuaria";

2-Dentro de "gestão_pecuaria", criar uma subpasta chamada "back" e outra "front";

3-Dentro de "back", criar duas subpastas, uma chamada "venvs", outra "projetos";

4-Dentro da pasta venvs, criar um ambiente virtual chamado "gestaoPecuaria", com o comando: 

	python -m venv gestaoPecuaria
 
5-Ativar a venv com o comando:  

	gestaoPecuaria\Scripts\activate
 Se a venv estiver habilitada, aparece "gestaoPecuaria" em cor de destaque antes da linha de comando;

6-Caso ocorra o erro:

	gestaoPecuaria\Scripts\activate : O arquivo
	..\gestao_pecuaria\back\venvs\gestaoPecuaria\Scripts\Activate.ps1 não pode ser
	carregado porque a execução de scripts foi desabilitada neste sistema. Para obter 	mais informações, consulte
	about_Execution_Policies em https://go.microsoft.com/fwlink/?LinkID=135170.
	No linha:1 caractere:1
	+ gestaoPecuaria\Scripts\activate
	+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    	+ CategoryInfo          : ErrodeSegurança: (:) [], PSSecurityException
    	+ FullyQualifiedErrorId : UnauthorizedAccess

Esse erro indica que a execução de scripts PowerShell foi desabilitada no sistema.
Para habilitar a execução de scripts toda vez antes de habilitar a venv, digite o comando: 

	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
 
Depois execute o passo 5 novamente ;

### Django
1- Instalar o Django com a venv ativada, usando o comando: 

	pip install Django
 
2- Verificar se tudo ocorreu corretamente, entrando no python, com o comando: 
	
 	python
  
Agora os comandos:

  	import django
   	print(django.get_version())
  
3- Na supbasta projetos, cria um projeto django, com o comando: 

	django-admin startproject gestaoPecuaria
 
4- Dentro da primeira pasta gestaoPecuaria, criar uma subpasta "apps";

5- Dentro da pasta "apps" criar uma nova aplicação "core", sendo ela a aplicação principal do projeto, usando o comando:  

	python ../manage.py startapp core

6- Dentro da pasta "apps" criar uma nova aplicação "users", sendo ela a aplicação para o controle de usuários (produtores) do projeto, usando o comando:

	python ../manage.py startapp users

### Banco de dados

1- Baixar o PostgreSQL e criar uma database chamada de "gestaoPecuaria" com o ususario "postgres" e a senha "admin" (para alterar a senha do usuario no PgAdmin, abre-se a database, clica em "Login/Group Roles","postgres", "definition" e escreva "admin" na "password");

### Instalação das libs utilizadas no back

1- Instalar o driver para Python com o comando: 

	pip install psycopg2-binary
 
2- Instalar a biblioteca python-decouple com o comando: 

	pip install python-decouple
 
3- Instalar o django-rest-framework com o comando: 

	pip install djangorestframework
 
4- Instalar o django-cors-headers com o comando: 

	pip install django-cors-headers

5 - Instalar o rest_framework_simplejwt

	pip install djangorestframework-simplejwt

6- Instalar o Pillow com o comando:

	python -m pip install Pillow
 
### Vue.js


Em outra aba do terminal:

1- Instalar o vue.js com o comando: 

	npm install -g @vue/cli
 
2- Criar um novo projeto vue chamado "gestao-pecuaria-frontend" dentro da pasta front com o comando: 

	vue create gestao-pecuaria-frontend
 
3- Selecionar a opção: vue 3

### Instalações das libs utilizadas no front

Dentro da pasta /gestao-pecuaria-frontend:

1- Instalar o Axios com o comando:

	npm install axios

2- Instalar o bootstrap

	npm install bootstrap

3- Instalar o router

	npm install vue-router

### Pull dos arquivos do repositório remoto no gitHub

1- Excluir os arquivos do back que serão importados do github:

	-gestaoPecuaria/gestaoPecuaria/settings.py;
	-gestaoPecuaria/gestaoPecuaria/urls.py;
	-gestaoPecuaria/apps/core/models.py;
	-gestaoPecuaria/apps/core/views.py;
 	-gestaoPecuaria/apps/users/models.py;
	-gestaoPecuaria/apps/users/views.py;


2- Excluir os arquivos do front que serão importados do git:

	Excluir a pasta src da pasta gestao-pecuaria-frontend
 	Excluir o .gitignore da pasta gestao-pecuaria-frontend
 
3- Dentro da pasta inicial "gestao_pecuaria" inicie o git com o comando: 

	git init
 
4- Adicione o URL do repositório remoto do Git como um repositório remoto em seu repositório local usando o comando: 

	git remote add origin https://github.com/CopiniS/gerenciadorPecuaria.git
 
5- Puxar as alterações do repositório remoto para o seu repositório local usando o comando: 

comando para criar uma branch local pecuariaMain:

	git checkout -b main

comando para puxar os arquivos do repositório remoto:

	git pull origin main

### Fazer as migrações para o banco de dados

1- Dentro da primeira pasta gestaoPecuaria, 

Para preparar as migrações, usar o comando:

	python manage.py makemigrations

Para migrar os dados para o banco, usar o comando:

	python manage.py migrate
 	
### Fazer pushs para o repositório remoto

1- Para mandar alterações locais ao repositório remoto: 

comando para adicionar todos os arquivos alterados ao stage:

 	git add .

comando para commitar:

	git commit -m "sua mensagem"

comando para dar o push para o repositório remoto:

	git push origin main

 
