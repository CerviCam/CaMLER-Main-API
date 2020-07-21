# CerviCam - Main API
This repository is the source code of main api of CerviCam app. The core is built by RESTful API and Django framework.

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Code structure](#structure)
- [Setup](#setup)
- [Activate Local Environment](#activate-local-environment)
- [Add and Install Packages](#add-and-install-packages)
- [Usage](#usage)
- [Troubleshootings](#troubleshootings)
- [Acknowledgments](#acknowledgments)

## **Code structure**
```
CerviCam
├── apps
│   ├── v1                          <- API version 1                                 
│   │   ├── app1                    <- App 1 on version 1
│   │   │   ├── models.py           <- Where database models for app1 will be defined
│   │   │   ├── admin.py            <- How you control and define your database model on admin page
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
├── .env                            <- Local variables
├── env                             <- Local environment, where all installed packages will be stored
├── requirements.txt                <- All required packages are defined in here

```
## **Prerequisites**
Install the following packages/tools:
- **Git** - You need this tool for managing the repository codes.
- **Python v3.7.7** - Since django uses python to run.

For DBMS you could choose one of these following options:
- **Sqlite3** - You will not install anything if you choose this option, by default django will provide it for you.
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
    DBMS=
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=
    DATABASE_PORT=
    ```
    
    e.g:
    ```bash
    DEBUG=True
    DBMS=POSTGRESQL
    DATABASE_NAME=cervicam
    DATABASE_USER=cervicam_user
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```

    Full documentation of **.env** file:

    | Variable          | Optional | Value                                                                             |
    |-------------------|-------------|-----------------------------------------------------------------------------------|
    | DEBUG             | No          | Either **True** or **False**                                                              |
    | DBMS              | No          | Either **SQLITE3** or **POSTGRESQL**                                                      |
    | DATABASE_NAME     | Yes         | Create database on POSTGRESQL with any name you want and set it to this variable  |
    | DATABASE_USER     | Yes         | User's name to access the database on POSTGRESQL                                  |
    | DATABASE_PASSWORD | Yes         | User's password to access the database on POSTGRESQL                              |
    | DATABASE_HOST     | Yes         | The host of POSGRESQL server                                                      |
    | DATABASE_PORT     | Yes         | The port that used by the host                                                    |
After you done, activate your local environment by following instructions that defined in [here](#activate-local-environment) and also you need to install all required packages by calling commands that defined in [here](#add-and-install-environment)

## **Activate Local Environment**
Before you jump to use all available commands on [usage](#usage), you need to activate a local environment first by calling this command in the root of repository:
- Windows:
    ```bash
    env\Scripts\activate
    ```
- Unix:
    ```bash
    source env/bin/activate
    ```

## **Add and Install Packages**
Activate your local environment from [this section](#activate-local-environment) before add or install packages.
- Install all required packages from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```
- Add new package
    1. Add new package and the version of it on the requirements.txt. e.g:
        ```bash
        Django==3.0.8
        ```
    2. Finally, install all packages from requirements.txt
       ```bash
       pip install -r requirements.txt
       ```
    

## **Usage**
Ensure you already activated the local environment from [this section](#activate-local-environment) before use all these useful commands:
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
    The collection can be seen on this [site](https://documenter.getpostman.com/view/7487357/T1DmDyKV). If you use Postman, you can import the collection from that link. I recommend you to import it from Postman for better use and understanding rather than test it directly from your mobile application or web application. To use the environment variables on your local, take a look the example that exists on that site.

- ### **Authentication and Authorization**
    In order to use all services, you need to have **Token for authentication** and **API Key for authorization**.
    - ### **Token**
        To get your token, you must exchange it by sending your account (username and password) to server, use *Get token request* on Postman to request that. Once you get the response with status code 200, you will see your token on response body. Take your token and put it on header as the following format:
        ```
        Authorization: Token [YOUR_TOKEN]
        ```
        In general type of request that needs token are:
        **POST**, **UPDATE**, **DELETE**. But for POST requests, some of them are exceptional, e.g Token Request or Create user request that needs body request (POST type), but doesn't need token since you could use those requests anonymously.

        **Need to be noted**, if you use our Postman collections, you only need to provide username and password to send a token request, there is no need to set the token to header after have a OK response from server because our collections already setted it automatically for you after you get token.
    - ### **API Key**
        For API key, you could generate it only once on admin page, and you must note the API key because you will have no chance to see it again after you refresh the page. Of course you can delete and create new one as you like, please use it wisely. Once you have your own API key, put it on your request header as the following format:
        ```
        Api-Key: [YOUR_API_KEY]
        ```

        **Need to be noted**, you definitely must provide API Key on your request header for any services you want to use.


## **Troubleshootings**

## **Acknowledgements**
- CerviCam
- IMERI



