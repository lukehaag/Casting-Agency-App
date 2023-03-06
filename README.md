# Casting-Agency-App
The Casting Agency App is a web-based application that allows a casting agency to manage actors and movies.

All code has been formatted using black.

This project is the final project of Udacity's Fullstack Course and it is built using the following technologies:

* Python Flask
* SQLAlchemy
* PostgreSQL
* Auth0 for authentication and authorization

## Getting Started ##
### Prerequisites ###
* Python 3.8 or later
* PostgreSQL
* Virtual Environment 
* PIP Dependencies 

PIP Dependencies can be installed by running the following command:

```bash
$ pip install -r requirements.txt
```

## Environment Variables ##

To run the application, you'll need to set the following environment variables:

* DATABASE_URL: the URL of your PostgreSQL database
* AUTH0_DOMAIN: the domain name of your Auth0 account
* API_AUDIENCE: the identifier of your Auth0 API
* ALGORITHMS: the algorithm used for JWT token verification
* AUTH0_CLIENT_ID: the Client ID of your Auth0 account
* AUTH0_CLIENT_SECRET: the Client Secret of your Auth0 account

```bash
DATABASE_URL="postgresql://user:password@localhost:5432/casting_agency"
AUTH0_DOMAIN="your-auth0-domain.auth0.com"
API_AUDIENCE="your-auth0-api-identifier"
ALGORITHMS=["RS256"]
AUTH0_CLIENT_ID="your-auth0-client-id"
AUTH0_CLIENT_SECRET="your-auth0-client-secret"
```

For the purposes of the project, environment variables have been provided as well as JWT tokens for the unit testing as well as postman tests.

## Running the Application ##

To run the application, first create a new PostgreSQL database and set the DATABASE_URL environment variable to the URL of your database.

Then run:

```bash
source setup.sh
flask run
```

To run the server in development you can run this command first:

```bash
export FLASK_ENV=development
```

## Auth0 SetUp ##

The environment variables have all been provided in the application

## API Reference ##

* Base URL: https://casting-agency-app.onrender.com

### Endpoints ###

The following endpoints have been set up. I've included a collection of postman tests for local or hosted testing.

* #### GET /actors ####

  * Request: curl -X GET http://127.0.0.1:5000/actors
  
    ```bash
    {
      "actors": [
          {
              "age": 50,
              "gender": "male",
              "id": 1,
              "name": "Tom Hanks"
          }  
      ],
      "success": true
    }
    ```

* #### POST /actors ####

  * Request: curl -X POST http://127.0.0.1:5000/actors
  
    ```bash
    {
      "actor": {
          "age": 47,
          "gender": "male",
          "id": 4,
          "name": "Leonardo DiCaprio"
      },
      "success": true
    }
  ```

* #### PATCH /actors/<int:actor_id> ####

  * Request: curl -X PATCH http://127.0.0.1:5000/actors/4

    ```bash
    {
      "actor": {
          "age": 48,
          "gender": "male",
          "id": 4,
          "name": "Leonardo DiCaprio"
      },
      "success": true
    }
    ```
  
* #### DELETE /actors/<int:actor_id> ####

  * Request: curl -X DELETE http://127.0.0.1:5000/actors/4

    ```bash
    {
      "deleted": 4,
      "success": true
    }
    ```

* #### GET /movies ####

* Request: curl -X GET http://127.0.0.1:5000/movies
  
  ```bash
  {
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 12 Jul 2002 00:00:00 GMT",
            "title": "Catch Me If You Can"
        },
        {
            "id": 2,
            "release_date": "Fri, 02 Oct 2020 00:00:00 GMT",
            "title": "Enola Holmes"
        }
    ],
    "success": true
  }
  ```
  
* #### POST /movies ####

  * Request: curl -X POST http://127.0.0.1:5000/movies

    ```bash
    {
      "movie": {
          "id": 4,
          "release_date": "Fri, 16 Jul 2010 00:00:00 GMT",
          "title": "Inception"
      },
      "success": true
    }
    ```
  
* #### PATCH /movies/<int:movie_id> ####

  * Request: curl -X PATCH http://127.0.0.1:5000/movies/4

    ```bash
    {
      "movie": {
          "id": 4,
          "release_date": "Fri, 08 Oct 2021 00:00:00 GMT",
          "title": "No Time to Die"
      },
      "success": true
    }
    ```
  
* #### DELETE /movies/<int:movie_id> ####

  * Request: curl -X DELETE http://127.0.0.1:5000/movies/4

    ```bash
    {
      "deleted": 4,
      "success": true
    }
    ```
## Unit Tests ##

To run the unit tests create a test database and run the following command:

```bash
$ Python3 test_app.py
```

