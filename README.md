                                   _   _                   _       _     
     _ __ ___  _   _   _ __  _   _| |_| |__   ___  _ __   | | __ _| |__  
    | '_ ` _ \| | | | | '_ \| | | | __| '_ \ / _ \| '_ \  | |/ _` | '_ \ 
    | | | | | | |_| | | |_) | |_| | |_| | | | (_) | | | | | | (_| | |_) |
    |_| |_| |_|\__, | | .__/ \__, |\__|_| |_|\___/|_| |_| |_|\__,_|_.__/ 
               |___/  |_|    |___/                                       
    --------------------------------------------------------------------- 

# Configuração do Ambiente no [Cloud Nine](http://c9.io)

**Python**

Já veio instalado com python 2.7.

**SQLite**
```bash
# Instalação do console
$ sudo apt-get install sqlite3

# Console
$ sqlite [path_do_banco]

# DDL de todas as tabelas
sqlite>.dump
# DDL de uma tabela
sqlite>.dump [nome da tabela]
```

**SQL ALchemy**

* http://docs.sqlalchemy.org/en/latest/intro.html#install-via-pip
* https://github.com/fastmonkeys/stellar/issues/34


```bash
# instalar
$ sudo apt-get install python-dev
$ sudo pip install SQLAlchemy
# checar
$ python
>>> import sqlalchemy
>>> sqlalchemy.__version__
'1.0.12'
>>> exit()
```

**Criação de Banco de Dados**

Após escrever database_setup.py, execute no bash:

```bash
$ python database_setup.py
```

**Povoamento do Banco de Dados**

No [material do curso](https://classroom.udacity.com/courses/ud088/lessons/3621198668/concepts/36123887380923),
o povoamento é feito no console do python:

```python
# Importar SQLAlchemy
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker

# Importar as classes do projeto.
>>> from database_setup import Base, Restaurant, MenuItem

# Qual banco?
>>> engine = create_engine('sqlite:///restaurantmenu.db')

# Tem que ligar as classes à banco
>>> DBSession = sessionmaker(bind = engine)

# e instanciar o objeto session (responsável pelas transações)
>>> session = DBSession()

# insere um restaurant
>>> r = Restaurant(name = "Minha Pizzaria")
>>> session.add(r)
>>> session.commit()

# lista todos os restaurant criados
>>> session.query(Restaurant).all()
```

# SQL ALchemy
- Configuration
```python
import sys
from sqlalchemy import ...
Base = declarative_base()
...
```

- Class
```python
# extends Base class
class Restaurant(Base):

class Menu(Base):
```

- Tables
```python
# inform the table's name
__tablename__ = 'menu'
```

- Mapper
```python
# inform table's columns
id = Column(Integer, primary_key = True)
columnName = Column(String(80), nullable = false)
restaurant_id = Column(Integer, ForeignKey('restaurant_id'))
restaurant = relationship(Restaurant)
```

- Insert (pelo prompt)
```python
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> from database_setup import Base, Restaurant, MenuItem
>>> engine = create_engine('sqlite:///restaurantmenu.db')
>>> DBSession = sessionmaker(bind = engine)
>>> session = DBSession()

# insere um restaurant
>>> r = Restaurant(name = "Minha Pizzaria")
>>> session.add(r)
>>> session.commit()
```
  
- Select
```python
>>> restaurant = session.query(Restaurant).all()
>>> restaurant[0].name
"Pizza Palace"
# ou
>>> restaurant = session.query(Restaurant).first()
>>> restaurant.name
# ou
>>> veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
>>> for v in veggieBurgers:
...    print v.id
...    print v.name
...    print v.price
...    print v.restaurant.name
...    print '-' * 10
```

- Update
```python
>>> b = session.query(MenuItem).filter_by(id = 10).one()
>>> b.price = '$2.99'
>>> session.add(b)
>>> session.commit()
```

- Delete
```python
>>> b = session.query(Restaurant).filter_by(id = 10).one()
>>> session.delete(b)
>>> session.commit
```

# Flask

```bash
# instalar
$ sudo pip install flask
# checar
$ python
>>> import flask
>>> flask.__version__
'0.10.1'
>>> exit()
```

**Aplicação mínima em Flask:**

```python
#project.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.debug = True # Server loads itself everytime the code changes
    app.run(host='0.0.0.0', port=8080)
```

* http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/

**GET requests**
```python
#project.py
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "etc, etc, etc"
```

**Templates**
```html
<!--menu.html -->
<html>
  <body>
  <h1>{{restaurant.name}}</h1>
  {% for i in items %}
  <div>
    <p>{{i.name}}</p>
    <p>{{i.description}}</p>
    <p> {{i.price}} </p>
  </div>
  {% endfor %}
</body>
</html>
```

```python
#project.py
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)
```

**url_for**
```python
#project.py
from flask import Flask, render_template, request, url_for
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"
```

```html
<!--menu.html -->
<a href='{{url_for('editMenuItem', restaurant_id = restaurant.id, menu_id = i.id) }}'>Edit</a>
```

**POST requests**

```html
<!--newmenuitem.html-->
<html>
<body>
    <h1> New Menu Item </h1>
    <form action="{{url_for('newMenuItem', restaurant_id=restaurant_id )}}" method = 'POST'>
        <p>Name:</p>
        <input type='text' size='30' name='name'>
        <input type='submit' value='Create'>
    </form>
</body>
</html>
```

```python
#project.py 
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
```

**Message Flashing**
```python
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
```

```html
<html>
    <body>
    <h1>{{restaurant.name}}</h1>
    <!--MESSAGE FLASHING EXAMPLE -->
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    <ul>
        {% for message in messages %}
        <li><strong>{{message}}</strong></li>
        {% endfor %}
    </ul>
    {% endif %}
    {% endwith %}
    {% for i in items %}
    <div>
        <p>{{i.name}}</p>
        <p>{{i.description}}</p>
        <p> {{i.price}} </p>
    </div>
    {% endfor %}
    </body>
</html>
```

**JSON**
```python
#database_setup.py
class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }

```

```python
project.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])
    
```