
#  Inventory

this project has functionality of crud operation that add, delete, update and read the inventory records.JWT token is used as authorization 





## How to run the project

create virtual environment with below command

```bash
  python -m venv inventroy_env
```

Activate virtual environment running below command

```bash
  .\inventroy_env\scripts\activate.bat
```
Install libraries from requirements.txt with below command

```bash
  pip install -r requirements.txt
```
run below command to create migrate file

```bash
  python manage.py makemigrations
```
run below command to reflect changes to db

```bash
  python manage.py migrate
```

run main.py using below command

```bash
  python manage.py runserver
```



## API Reference

#### Get all user subscription

```http
  GET inventory/list
```

 | Description                     |
 |:--------------------------------|
| fetch all the inventory records |




#### home page to subscribe user by filling details

```http
  GET  inventory/retrieve/id
```

 | Description              |
 |:-------------------------|
| fetch inventory using id |


#### Check user subscription by providing email address

```http
  PUT inventory/update/id
```

 | Description                               |
 |:------------------------------------------|
| this endpoint will update record using id |

#### activate and deactivate user subscription

```http
  GET inventory/create
```

 | Description             |
 |:------------------------|
| to add inventory record |



#### unsubscribe subscribed user

```http
  DELETE /unsubscribe/id
```

 | Description                |
 |:---------------------------|
| to delete inventory record |

