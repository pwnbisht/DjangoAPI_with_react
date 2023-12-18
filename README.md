# Django API with React Frontend

Welcome to the Django API project! This repository contains the source code for our backend(Django/DRF) and frontend(react.js).

## Table of Contents

- [About](#about)
  - [Authentication Flow](#authentication-flow)
      - [signup](#signup)
      - [login](#login)
      - [fileupload](#fileupload)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configurations](#configurations)
  - [.env file](#.env-file)
- [Contributing](#contributing)

  ## About
  This project utilizes Django (or Django REST Framework) for the backend and React.js for the frontend. The system incorporates token-based authentication, ensuring that only authenticated users can access private routes. Upon successful signup, users receive both a "refresh token" and an "access token." These tokens must be included in the header of every frontend request.

  After a successful login, users are redirected to the home page, which features three file input boxes. The system only accepts Excel (.xls, .xlsx) and CSV files. Each file may have different column names and data types, requiring validation based on these columns. To achieve this, users must upload 'csv1.csv' to input box 1, 'csv2.csv' to input box 2, and 'file.excel' to input box 3.

  File validation is crucial, and errors will be displayed if the uploaded files contain missing values or are empty. This ensures that only correctly validated files are successfully uploaded.

  Token management is facilitated through HTTP-only cookies, providing a secure storage mechanism on the frontend. In the event of token expiration, React.js automatically refreshes the token if the corresponding cookie is available. If the cookie is missing, the user is redirected to the login page.

  ### Authentication Flow
  #### signup
  - User signs up, triggering the generation of "refresh token" and "access token."
  - Tokens are stored in HTTP-only cookies for secure frontend authentication.

  #### login
  - Authenticated users are redirected to the home page upon successful login.

  #### fileupload
    - Uploaded files undergo validation based on their column names and data types.
    - Error messages are displayed if the file:
      - is empty
      - Contains missing values
      - invalid format etc.


## Getting Started

### Prerequisites

List any prerequisites or dependencies that users need to install to get your project up and running. For example:

- [Node js](https://nodejs.org/en/download/): You need to have Node js installed.
- [Python](https://www.python.org/downloads/) (3.12)

### Installation

### Step 1: Clone the Repository

You can get the source code by cloning this repository to your local machine. Open your terminal and run the following command:
```bash
https://github.com/pwnbisht/DjangoAPI_with_react.git
```
Change your working directory to the newly cloned repository:
```bash
cd DjangoAPI_with_react
```

### Step 2: Configure Backend
  - ### Step 2.1: change the directory to DjangoAPI
    ```bash
    cd DjangoAPI
    ```
 - ### Step2.2: Create Virtual env
    ```bash
    pip install virtualenv
    ```
    ```bash
    python -m venv .venv
    ```
  - ### step 2.3 : Activate the virtual env
    for windows:
    ```bash
    .venv/Scripts/activate
    ```
    for linux:
    ```bash
    .venv/bin/activate
    ```
  - ### setp 2.4: Install the python packages and libraries
    To install the required Python packages and libraries, use the pip package manager with the requirements.txt file:
    
    ```bash
    pip install -r requirements.txt
    ```
  - ### step 2.5: apply migrations
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```
  - ### Step 2.6: Run Django Server
        ```bash
        python manage.py runserver
        ```
### Step 3: Configure Frontend

- ### Step 3.1: Open new Terminal and chage the directory to react_ui
    ```bash
    cd react_ui
    ```
- ### Step 3.2 : Install Node modules
  ```bash
  npm install
  ```
- ### Step 3.3 : Run Node server
  ```bash
  npm start
  ```

## Configurations

### .env file
  - create .env file in the root folder (DjangoAPI/DjangoAPI/)
  - add your environments variables into .env file and update settings.py file accordingly.

## Contributing
[Pawan Bisht](https://github.com/pwnbisht)
