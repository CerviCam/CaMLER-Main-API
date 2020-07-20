# CerviCam - Main API
This repository is the source code of main api of CerviCam app. The core built by RESTful API and Django framework. 

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Activate Local Environment](#activate-local-environment)
- [Add and Install Packages](#add-and-install-packages)
- [Usage](#usage)


## **Prerequisites**
Install the following packages/tools:
- **Git** - You need this tool for managing codes.
- **Python v3.7.7** - Since django uses python to run.

For DBMS you could choose one of these following options:
- **Sqlite3** - Means you will not install anything if you choose this option, by default django will provide it for you.
- **Postgresql v10.12** - **Recommended** for performance reason.

## **Setup**
Follow all these instructions if this is the first time you pull/fork this repository, and go to [usage](#usage) section after you done.
1. Create **env folder** in the root of project/repository for creating local environment, will use this for installing all needed packages and will isolate the environment from global environment.
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

    Full documentation to set **.env** file:

    | Variable          | Optional | Value                                                                             |
    |-------------------|-------------|-----------------------------------------------------------------------------------|
    | DEBUG             | No          | Either **True** or **False**                                                              |
    | DBMS              | No          | Either **SQLITE3** or **POSTGRESQL**                                                      |
    | DATABASE_NAME     | Yes         | Create database on POSTGRESQL with any name you want and set it to this variable  |
    | DATABASE_USER     | Yes         | User's name to access the database on POSTGRESQL                                  |
    | DATABASE_PASSWORD | Yes         | User's password to access the database on POSTGRESQL                              |
    | DATABASE_HOST     | Yes         | The host of POSGRESQL server                                                      |
    | DATABASE_PORT     | Yes         | The port that used by the host                                                    |

## **Activate Local Environment**
Before you jump to [usage](#usage), you need to activate a local environment by calling this command in the root of repository:
- Windows:
    ```bash
    env\Scripts\activate
    ```
- Linux:
    ```bash
    source env/bin/activate
    ```

## **Add and Install Packages**
Activate your local environment on [this section](#activate-local-environment) before install.
- Run this command to add new package
    ```bash
    pip install [PACKAGE]
    ```
- Install all required packages from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

## **Usage**
Ensure you already activated the local environment before use all these useful commands:
- Run application, used to run application and run on **localhost:8000** by default
    ```bash
    python manage.py runserver
    ```
- Make migrations after you changed something on models
    ```bash
    python manage.py makemigrations
    ```
- Migrate after there is a new changed of migrations file
    ```bash
    python manage.py migrate
    ```


