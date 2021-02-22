# ITALIAN WINE API // FNSD CAPSTONE PROJECT
README for my custom Wine API.

HEROKU LINK: https://italianwineapi.herokuapp.com/

## ABOUT

The italian wine API is currently a live hosted database containing the wines in my wine collection,
and is a passion project combining my wine interest and technology.

They are sorted both by grape, producer and key area characteristics as well as a rating system.

## MOTIVATION

The project was developed as part of an assignment to finnish Udacity's Full Stack Developer Program.
The idea was to both bolster my abilities to create API's and work with databases in my future job, 
as well as an idea for a future tool for cataloging wine.

## Installing dependencies

#### Python 3.9.1 

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Pip Dependencies

Once you have your virtual environment setup and running, install dependencies by running

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages I have used within the `requirements.txt` file.

#### Key Dependencies 

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the postgres database. 

- [POSTGRESSQL](https://www.postgresql.org/download/) is the database provider used for the project.

### ENVIROMENT SETUP
There is a supplied .env file used for development on windows systems, but it has also provided the author with some trouble. It is recommended to use either the setup.sh or run.sh files to setup enviroment files.

## Database Setup
Heroku recommends working with a local database while in a local enviroment. A backup database that can be used for development and testing has been provided.

Edit the "POSTGRESQL_USER" parameter in the files setup.sh and run.sh to correspond your own postgres user.
By default a superuser installed on the system is "postgres".

With Postgres running, restore a database using the italianwine.psql file provided. 
First create a database named italianwine, then run populate database using the following commands.




```bash
createdb italianwine
psql italianwine < italianwine.psql
```
If the above command does not work correctly, the following command can be used.

If you create a database with a different name, please update corresponding enviroment files.

```
psql -d italianwine -U postgres -a -f italianwine.psql

```

## Running the application localy:

To run the server:
```
bash run.sh

```

This will load .env variables and run the app on localhost in developer mode.

Command below can be run if you wish to load the enviroment var for running tests.
```
source setup.sh

```

## GETTING STARTED:

BASE URL: https://italianwineapi.herokuapp.com/

This application can also be run locally. By default the app runs at http://127.0.0.1:5000/

## AUTHENTIFICATION:

The application uses RBAC provided by AuthO.

There are two different types of roles. 

#  Subscriber 
A subscriber to the wine list is able to request lists of the wines including all the information about the wine,
as well as request the geographical. 

Permissions: `get:wines, get:districts`

# EDITOR

An editor has all rights, and can in addition to retrieving info, also create and delete instances of both 
wines and districts, as well as edit them.

Permissions `get:wines, get:districts, post:wines, post:districts, delete:wines, delete:districts, patch:wines, patch:districts`

## ERRORS 

Error responses are returned as JSON objects.
This API will return either 400, 401 404, 405 or 422 error codes if the requests fail.

Example return: 
```
{
  "error": 422, 
  "message": "Incomplete body", 
  "success": false
}
```

# TESTS
To run tests, populate a test database, test_wine_api with provided backup, setup enviroment and run
test_api:

```
dropdb test_wine_api
createdb test_wine_api
psql test_wine_api < italianwine.psql
source setup.sh
python test_api.py
```



# POSTMAN
A folder of POSTMAN request collections used while developing has also been provided for reviewers convenience.
They are organized with both a local and a live version, containing tests and active JWT_tokens
 - WINE API TEST EDITOR HEROKU.postman_collection
    - Tests for live server, containing all access.
    
 - WINE API TEST EDITOR LOCAL.postman_collection
    - Tests for local server, containing all access.

 - WINE API TEST SUBSCRIBER HEROKU LIVE.postman_collection
    - Tests for live server, containing limited subscriber access.

 - WINE API TEST SUBSCRIBER LOCAL.postman_collection
    - Tests for local server, containing limited subscriber access.


# ENDPOINTS 

# ENDPOINT GET /
What:
    - public endpoint. Will return a "I'm alive" message referring you to the docs.

### How:
Request parameters: None

### Example
```
LOCAL: curl http://127.0.0.1:5000
LIVE: curl https://italianwineapi.herokuapp.com/
```

# ENDPOINT: GET /wines

What: 
    - Will return a list of wines in the database, paginated by 8.

### How:

Request parameters: None
Requirements authorization: `get:wines`

### Example 

curl https://italianwineapi.herokuapp.com/wines -H "Authorization: Bearer {INSERT_TOKEN_HERE}"



<details>
<summary>Example Response:</summary>

```
{
    {
    "success": true,
    "wines": [
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 1,
            "producer": "Proddutori del Barbaresco",
            "rating": 96,
            "vintage": 2016,
            "vinyard": "Rabaja"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 2,
            "producer": "Proddutori del Barbaresco",
            "rating": 98,
            "vintage": 2010,
            "vinyard": "Asili"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 3,
            "producer": "Proddutori del Barbaresco",
            "rating": 92,
            "vintage": 2007,
            "vinyard": "Paje"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 4,
            "producer": "Proddutori del Barbaresco",
            "rating": 92,
            "vintage": 2007,
            "vinyard": "Pora"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 5,
            "producer": "Bruno Giacosa",
            "rating": 100,
            "vintage": 2007,
            "vinyard": "Barbaresco Red Label Asili"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 6,
            "producer": "Bruno Giacosa",
            "rating": 96,
            "vintage": 2001,
            "vinyard": "Barbaresco Red Label Asili"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 7,
            "producer": "Giovanni Rosso Barolo",
            "rating": 100,
            "vintage": 2016,
            "vinyard": "Ester Canale Rosso"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 8,
            "producer": "Giovanni Rosso Barolo",
            "rating": 100,
            "vintage": 2007,
            "vinyard": "Ester Canale Rosso"
        }
    ]
}
}
```

</details>

#

# ENDPOINT: GET /wines?page=<int:page_number>

### What:
Will return a list of wines, sorted by page number.

### How:

Request parameters: page:<page_number:int> (optional)
Requires authorization: `get:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines?page=2 -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```
#

<details>
<summary>Example Response</summary>

```

"success": true,
    "wines": [
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 9,
            "producer": "Giovanni Rosso Barolo",
            "rating": 89,
            "vintage": 2016,
            "vinyard": "Serralunga d'Alba"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 10,
            "producer": "Bruno Giacosa Barolo",
            "rating": 96,
            "vintage": 2016,
            "vinyard": "Cannubi"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 11,
            "producer": "Bruno Giacosa Barolo",
            "rating": 98,
            "vintage": 2010,
            "vinyard": "Serralunga"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 12,
            "producer": "Luciano Sandrone",
            "rating": 98,
            "vintage": 2010,
            "vinyard": "Le Vigne"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 13,
            "producer": "Luciano Sandrone",
            "rating": 95,
            "vintage": 2011,
            "vinyard": "Le Vigne"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 14,
            "producer": "Gaja",
            "rating": 93,
            "vintage": 2001,
            "vinyard": "Sperrs"
        },
        {
            "district_id": 8,
            "grape": "Sangiovese",
            "id": 15,
            "producer": "Poliziano",
            "rating": 100,
            "vintage": 2016,
            "vinyard": "Asinone"
        },
        {
            "district_id": 8,
            "grape": "Sangiovese",
            "id": 16,
            "producer": "Poliziano",
            "rating": 100,
            "vintage": 2017,
            "vinyard": "Asinone"
        }
    ]
}

```

</details>

#

# ENDPOINT GET /wines/<int:wine_id>

### What:
Will return an instance of a wine given by ID.

### How:

Request parameters: id: int
Requires authorization: `get:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines/1 -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```

<details>
<summary>Example Response</summary>

```

{
    "success": true,
    "wine": {
        "district_id": 1,
        "grape": "Nebbiolo",
        "id": 1,
        "producer": "Proddutori del Barbaresco",
        "rating": 96,
        "vintage": 2016,
        "vinyard": "Rabaja"
    }
}

```

</details>


#
# ENDPOINT GET /districts

### What:
Will return a paginated list of districts in the database

### How:

Request parameters: None
Requires authorization: `get:districts`

Example curl:
```
curl https://italianwineapi.herokuapp.com/districts -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```

<details>
<summary>Example Response</summary>

```

{
    "districts": [
        {
            "id": 1,
            "name": "Barbaresco",
            "province": "Piemonte"
        },
        {
            "id": 2,
            "name": "Barolo",
            "province": "Piemonte"
        },
        {
            "id": 3,
            "name": "Barbera d'Alba",
            "province": "Piemonte"
        },
        {
            "id": 4,
            "name": "Chianti Classico",
            "province": "Toscany"
        },
        {
            "id": 5,
            "name": "Montalcino",
            "province": "Toscany"
        },
        {
            "id": 6,
            "name": "Chianti Rufina",
            "province": "Toscany"
        },
        {
            "id": 7,
            "name": "Montepulciano",
            "province": "Toscana"
        },
        {
            "id": 8,
            "name": "Etna Rosso",
            "province": "Sicilia"
        }
    ],
    "success": true
}

```

</details>


#
# ENDPOINT GET /districts/id

### What:
Will return a paginated list of wines available in given district_id, as well as district name.

### How:

Request parameters: district_id: int
Requires authorization: `get:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/districts/2 -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```

<details>
<summary>Example Response</summary>

```

{
    "district": "Barolo",
    "success": true,
    "wine": [
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 1,
            "producer": "Proddutori del Barbaresco",
            "rating": 96,
            "vintage": 2016,
            "vinyard": "Rabaja"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 2,
            "producer": "Proddutori del Barbaresco",
            "rating": 98,
            "vintage": 2010,
            "vinyard": "Asili"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 3,
            "producer": "Proddutori del Barbaresco",
            "rating": 92,
            "vintage": 2007,
            "vinyard": "Paje"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 4,
            "producer": "Proddutori del Barbaresco",
            "rating": 92,
            "vintage": 2007,
            "vinyard": "Pora"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 5,
            "producer": "Bruno Giacosa",
            "rating": 100,
            "vintage": 2007,
            "vinyard": "Barbaresco Red Label Asili"
        },
        {
            "district_id": 1,
            "grape": "Nebbiolo",
            "id": 6,
            "producer": "Bruno Giacosa",
            "rating": 96,
            "vintage": 2001,
            "vinyard": "Barbaresco Red Label Asili"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 7,
            "producer": "Giovanni Rosso Barolo",
            "rating": 100,
            "vintage": 2016,
            "vinyard": "Ester Canale Rosso"
        },
        {
            "district_id": 2,
            "grape": "Nebbiolo",
            "id": 8,
            "producer": "Giovanni Rosso Barolo",
            "rating": 100,
            "vintage": 2007,
            "vinyard": "Ester Canale Rosso"
        }
    ]
}

```
</details>

#

# ENDPOINT POST /wines

### What:
Will create new instance of a wine object.

### How:
Request body: 
{producer:string, vintage:int, grape:string, vinyard:string, rating:int, district_id:int}

The parameters producer, vintage, grape and district_id are required.

Requires authorization: `post:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
 -d '{
	"producer": "Proddutori del Barbaresco",
	"vintage": "2016",
    "grape": "Nebbiolo",
    "vinyard": "Rabaja",
    "rating": "96",
    "district_id": "1"
    }'

```

<details>
<summary>Example Response</summary>

```

{
    "success": true,
    "wine": {
        "district_id": 2,
        "grape": "Nerello Mescalese",
        "id": 29,
        "producer": "Eduardo Torres",
        "rating": 95,
        "vintage": 2016,
        "vinyard": "Pirra"
    }
}

```

</details>

#

# ENDPOINT POST /districts

### What:
Will create an instance of the district object.

### How:

Request body: {name:string, province:string}
Requires authorization: `post:districts`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
 -d '{
    "name": "Etna Rosso",
    "province": "Sicilia
    }'

```

<details>
<summary>Example Response</summary>

```

{
    "created": {
        "id": 8,
        "name": "Etna Rosso",
        "province": "Sicilia"
    },
    "success": true
}

```

</details>

#

# ENDPOINT DELETE /wines/<int:wine_id>

### What:
Will delete a wine with the given id.
Returns a JSON response with a success message, as well as a formatted version of the deleted wine.

### How:

Request parameters: wine_id:int
Requires authorization: `delete:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines/9 -X DELETE -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```

<details>
<summary>Example Response</summary>

```

{
    "deleted": {
        "district_id": 2,
        "grape": "Nerello Mescalese",
        "id": 29,
        "producer": "Eduardo Torres",
        "rating": 95,
        "vintage": 2016,
        "vinyard": "Pirra"
    },
    "success": true
}


```

</details>

#

# ENDPOINT DELETE /districts/<int:district_id>

### What:
Will delete an instance of a district with the given ID.
Returns a JSON response with a success message, as well as a formatted version of the deleted district.

### How:

Request parameters: district_id: int
Requires authorization: `delete:disticts`

Example curl:
```
curl https://italianwineapi.herokuapp.com/districts/9 -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```

<details>
<summary>Example Response</summary>

```

{
    "deleted": {
        "id": 9,
        "name": "Etna Rosso",
        "province": "Sicilia"
    },
    "success": true
}


```

</details>

#

# ENDPOINT PATCH /wines/<int:wine_id>

### What:
Edit information about a wine with the given ID.
Returns a JSON success response as well as formatted version of the edited wine.

### How:

Request body: {producer:string, vintage:int, grape:string, vinyard:string, rating:int, district_id:int}
Requires authorization: `patch:wines`

Example curl:
```
curl https://italianwineapi.herokuapp.com/wines/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
 -d '{
	"producer": "Proddutori del Barbaresco",
    "rating": "75",
    }' 

```

<details>
<summary>Example Response</summary>

```

{
    "Wine": {
        "district_id": 1,
        "grape": "Nebbiolo",
        "id": 1,
        "producer": "Proddutori del Barbaresco",
        "rating": 75,
        "vintage": 2016,
        "vinyard": "Rabaja"
    },
    "success": true
}

```

</details>

#

# ENDPOINT PATCH /districts/<int:district_id>

### What:
Edit information about a district with the given ID.
Returns a JSON success response as well as a formatted version of the edited district

### How:

Request parameters: district_id: int
Requires authorization: `patch:districts`

Example curl:
```
curl https://italianwineapi.herokuapp.com/districts/8 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
 -d '{
	"name": "Montalcino"

    }' 

```

<details>
<summary>Example Response</summary>


```
{
    "district": {
        "id": 7,
        "name": "Montalcino",
        "province": "Toscana"
    },
    "success": true
}


```

</details>

