### Flask Rest Api

#### Steps:


+ Install packages:
  * Install pipenv ```pip install pipenv```.
  * Create a virtualenv and install packages ```pipenv install```
  * Enter in virtualenv ```pipenv shell```

+ Running migrations:
  * Enter in python console.
  * Enter this commands in python terminal:
  ```
     python migrations.py db init
     python migrations.py db migrate
     python migrations.py db upgrade
  ```
  
  Obs: Just to undo last migrations:
  ```python migrations.py db downgrade```
  

+ Running application:
  * ```python app.py```


+ Todo:
  - [ ] - Implementar todos os métodos Rest para os modelos.
  - [ ] - Separar módulos pastas.
  - [ ] - Criar arquivo de configuração.

