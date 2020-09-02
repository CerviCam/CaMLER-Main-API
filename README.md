# CerviCam - Main API
As main services of CerviCam app and the only gateway to accesing all services, which mean all outside-requests must be going through this API for any CerviCam services, including AI service. The core is built by Django and python as its language. The API Gateway is built by REST architecture.

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [File structure](#file-structure)
- [Setup](#setup)
- [Activate/Deactivate Local Environment](#activate/deactivate-local-environment)
- [Add and Install Packages](#add-and-install-packages)
- [Usage](#usage)
- [API Documentation](#api-documentation)
    - [Postman Collection](#postman-collection)
    - [Authentication and Authorization](#authentication-and-authorization)
        - [Token](#token)
        - [API Key](#api-key)
- [Troubleshootings](#troubleshootings)
- [Acknowledgements](#acknowledgements)

## **File structure**
```
Main-API
├── apps
│   ├── v1                          <- API version 1                                 
│   │   ├── app1                    <- App 1 on version 1
│   │   │   ├── models.py           <- Where database models for app1 will be defined
│   │   │   ├── admin.py            <- How you control/manage your database model on admin page
│   │   │   ├── serializers.py      <- Serializer and deserializer of all your model on app1
│   │   │   ├── urls.py             <- Map all endpoints to handler from views.py
│   │   │   ├── views.py            <- Handlers of all endpoints that defined on urls.py
│   │   │   └── ...                 <- For the rest files, you should go further look at Django documentation
│   │   │
│   │   ├── app2                    <- App 2 on version 1
│   │   ├── app...                  <- Rest apps on version 1
│   │   └── urls.py                 <- Map all endpoint to app urls
│   │
│   ├── v2                          <- API version 2
│   ├── v...                        <- Other versions
│   └── urls.py                     <- Define versions for all endpoints
│
├── cervicam                        <- Configuration files
│   ├── settings.py                 <- Allowed host, secret key, database, timezone, etc
│   ├── urls.py                     <- Root urls, this will connect to apps.urls.py
│   ├── ...                         <- For the rest files, you should go further look at Django documentation
│
├── .env                            <- Local variables
├── env                             <- Local environment, where all installed packages will be stored
├── requirements.txt                <- All required packages are defined in here

```
## **Prerequisites**
Install the following packages/tools:
- **Git** - You need this tool for managing the repository codes.
- **Python v3.7.7** - Since django uses python to run.

For DBMS you can choose one of these following options:
- **Sqlite3** - You will not install anything for database if you choose this option, by default django will provide it for you.
- **Postgresql v10.12** - **Recommended** for performance reason.

## **Setup**
Follow all these instructions if this is the first time you pull/fork this repository.
1. Create **env** folder in the root of project/repository for creating local environment, will use this for saving  all installed packages and will isolate the environment from global environment.
    ```bash
    python -m venv env
    ```
2. Create **.env** file in the root of project/repository and fill in these variables:
    ```bash
    DEBUG=
    ALLOWED_HOSTS=
    DBMS=
    MEDIA_PATH=
    AI_API_DOMAIN=
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=
    ```
    
    e.g:
    ```bash
    DEBUG=True
    ALLOWED_HOSTS=locahost,127.0.0.1
    DBMS=POSTGRESQL
    MEDIA_PATH=./media
    AI_API_DOMAIN=http://localhost:2020
    DATABASE_NAME=cervicam
    DATABASE_USER=cervicam_user
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```

    Full documentation of **.env** file:

    | Variable          | Optional    | Value                                                                             |
    |-------------------|-------------|-----------------------------------------------------------------------------------|
    | DEBUG             | No          | Either **1** or **0**                                                             |
    | ALLOWED_HOSTS     | Yes         | List of allowed hosts and separated by comma, the default is **'*'** means all hosts  |
    | DBMS              | Yes         | Either **SQLITE3** or **POSTGRESQL**, the default is **SQLITE3**                  |
    | MEDIA_PATH        | Yes         | The path where model files/images will be stored, the default path is **./media** |
    | AI_API_DOMAIN     | Yes         | URI of AI API, you can ignore it if you don't use the API                         |
    | DATABASE_NAME     | Yes         | Set targeted database, ensure you have created on your DBMS                       |
    | DATABASE_USER     | Yes         | User's name to access the database                                                |
    | DATABASE_PASSWORD | Yes         | User's password to access the database                                            |
    | DATABASE_HOST     | Yes         | The host of database server                                                       |
    | DATABASE_PORT     | Yes         | The port that used by the host                                                    |

After you done, activate your local environment by following instructions that defined in [here](#activate/deactivate-local-environment) and also you need to install all required packages by calling commands that defined in [here](#add-and-install-environment)

## **Activate/Deactivate Local Environment**
Before you use all available commands on [usage](#usage), you need to activate a local environment first by calling this command in the root of repository:
- Windows:
    ```bash
    env\Scripts\activate
    ```
- Unix:
    ```bash
    source env/bin/activate
    ```

And if you need to close it, then run as easy as run terminated signal:
- Windows/Unix:
    ```bash
    [CTRL + C]
    ```

or you can close it in gracefully way:
- Windows/Unix:
    ```bash
    deactivate
    ```

## **Add and Install Packages**
Activate your local environment from [this section](#activate/deactivate-local-environment) before add or install packages.
- Install all required packages from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```
- Add new package
    1. Add new package and the version of it on the requirements.txt. e.g:
        ```bash
        Django==3.0.8
        ```
    2. Finally, install all packages after you added it to requirements.txt
       ```bash
       pip install -r requirements.txt
       ```
    

## **Usage**
Ensure you already activated the local environment from [this section](#activate/deactivate-local-environment) before use all these useful commands:
- Run application and will be hosted at **localhost:8000** by default
    ```bash
    python manage.py runserver
    ```
- Make migrations after you created/changed something on models
    ```bash
    python manage.py makemigrations
    ```
- Migrate after there is a new changes of migration files
    ```bash
    python manage.py migrate
    ```
- Create superuser in order to use django admin or other stuffs that needs super user credential
    ```bash
    python manage.py createsuperuser
    ```
## **API Documentation**
- ### **Postman Collection**
    The collection can be seen on this [site](https://documenter.getpostman.com/view/7487357/T1DmDyKV). If you use Postman, you can import the collection from that link. We recommend you to import it from Postman for better use and understanding instead of test it directly from your mobile application or web application. To use the environment variables on your local, take a look the example that exists on that site.

- ### **Authentication and Authorization**
    In order to use all services, you need to have **Token** and **API Key**. Basically, token is used to identify who you are. And before accessing all services, the server needs to know whether you have a permission to access the API or not, that's why we require you to send API key as well before token to identify your authorization.
    - ### **Token**
        To get your token, you must exchange it with your **username** and **password**, you can use *Get token request* on our Postman to request that. Once you get the response with status code 200, you will see your token on response body. Take your token and put it to header as the following format:
        ```
        Authorization: Token [YOUR_TOKEN]
        ```
        In general, here are the list of requests that needs token:
        **POST**, **UPDATE**, **DELETE**. But for POST requests, some of them are exceptional, e.g *Token Request* or *Create user request* that needs body request (POST type), but doesn't need a token since you can use those requests anonymously.

        **Notable**, if you use our Postman collections, you only need to provide username and password to send a token request, there is no need to set the token to header after having a OK response from server because our collections already set it automatically for you after you get token.
    - ### **API Key**
        For API key, you can generate it only once on admin page, and you must note the API key because you will have no chance to see it again after you refresh the page or close the page. Of course you can delete and create new one as you like, but please use it wisely. Once you have your own API key, put it on your request header as the following format:
        ```
        Api-Key: [YOUR_API_KEY]
        ```

        **Notable**, you definitely must provide API Key on your request header for any services you want to use.


## **Troubleshootings**

## **Acknowledgements**
- CerviCam
- IMERI



