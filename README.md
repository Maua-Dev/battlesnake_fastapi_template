# battlesnake_fastapi_template 🐍

This is a [Battlesnake](http://play.battlesnake.com) template written in Python using the [FastAPI](https://fastapi.tiangolo.com/) framework and deployed in AWS Lambda using [Mangum](https://mangum.io).

## Introduction and Objectives ⁉
The main purpose of this project is to create a template for Battlesnake using FastAPI and Mangum. The biggest challenge is to understand how an API works and how to deploy it in AWS Lambda.

![Example](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/58080c12-6d91-4366-b4e0-f7cd9f20f98d)

## How to use 🤔
First of all, you need to create a repo using issues from [Devmaua setup](https://github.com/Maua-Dev/devmaua_setup/), set the **project_name** as "**battlesnake_{your name}**" and project template as **battlesnake_fastapi_template** and make sure it's **public** . Hit create issue and wait for the setup to finish.

After that you need to clone your new repo, create a virtual environment and install the requirements.

## Installation 👩‍💻

### Create virtual ambient in python (only first time)

###### Windows

    python -m venv venv

###### Linux / macOS

    python3.13 -m venv venv

#### Activate the venv

###### Windows:

    venv\Scripts\activate

###### Linux / macOS:

    source venv/bin/activate

#### Install the requirements

    pip install -r requirements-dev.txt
    pip install -r requirements.txt

#### Run the tests

    pytest

#### Run the server local

    uvicorn src.app.main:app --reload

## The Challenge 🐍
The challenge is to create a Battlesnake using FastAPI and Mangum. The Battlesnake must be deployed in AWS Lambda.
You can find the documentation for Battlesnake [here](https://docs.battlesnake.com/).

### The files 📁
The project is divided in 2 folders: **src** and **tests**.
In src you can find the main.py file, which is the file that contains the FastAPI app and the routes. From there you can create your own routes and functions.
The tests folder contains the tests for the project. You can create your own tests and run them using pytest.

### The routes 🛣
The routes are created in **main.py** file. You can create your own routes and functions. The routes are created using FastAPI decorators, you can find the documentation [here](https://fastapi.tiangolo.com/tutorial/first-steps/). Follow the rules from Battlesnake documentation to create your routes, they should look like [this](https://docs.battlesnake.com/api).

### Atention 🚨
In order to deploy your Battlesnake in AWS Lambda, you need to follow some rules:
- The routes must be created using FastAPI decorators;
- Don't use complete import, only relative ones. (eg: from .move_function import move);
- ALWAYS test your code before pushing it to the repo. You can use pytest to test your code;
- Don't forget to create your own tests;
- Make sure there is a \_\_init\_\_.py file each directory, otherwise it's not a Python package;
- Every file should be inside the app folder;

### Deploy 🚀

![FastApi AWS drawio](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/68026cf1-14de-4ca9-bd50-61688556b581)


After pushing your code to the repo, it will trigger an action to deploy your code in AWS Lambda. You can find the action in the **.github/workflows/aws_cd.yml** file.

In the first time you push your code, the action will create a new stack in AWS CloudFormation. After that, every time you push your code, the action will update the stack with the new code.

The deploy runs only on the **dev** branch and targets the Dev Community AWS account in **sa-east-1**, using OIDC (`GithubActionsRole`) via the `AWS_ACCOUNT_ID_DEV` secret. The Lambda runs on **Python 3.13**.

In the [Actions](https://github.com/Maua-Dev/battlesnake_fastapi_template/actions) tab you can see the status of the deploy, and if it was successful or not. If it was successful, you can find the URL of your API in the outputs tab of the action (in the final part of the "Deploy with CDK" step).


![Action Tab](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/ca447b23-e4f3-423c-8ba2-3f7c891849c9)
![CD](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/1340c269-f182-46eb-ae12-1d0bdd6059a2)
![STEP](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/6129f465-a54d-46fc-b45a-c8b219a6823b)

There you can find your API URL. You can use this URL to create your Battlesnake in the Battlesnake website. You can find the documentation [here](https://docs.battlesnake.com/guides/getting-started#step-2-create-a-battlesnake).

The stack outputs also include a link to the Lambda console (monitoring tab) so you can inspect CloudWatch logs when debugging.

![Outputs](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/e06bf1dd-18cc-4057-91ea-3ccd8074848f)

![Lambda Console](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/8a584df8-9efe-432d-9083-6f3523b7f58c)
![Cloudwatch Logs](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/94483cd1-ae3c-46c0-86df-d8fff0b0490e)

After finishing your project, you can delete it from our backend using our CD.

![AwsDestroy](https://github.com/Maua-Dev/battlesnake_fastapi_template/assets/81604963/68a73993-c55e-4ba8-8bf9-2becbc9decf6)

## Useful tools 🛠

- [Postman](https://www.postman.com/) - API development environment
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Python 3.13](https://docs.python.org/3.13/) - Python Documentation
- [Battlesnake](https://docs.battlesnake.com/) - Battlesnake Documentation

## Thanks 👢🍿

We hope you like and enjoy it! Thanks!

## Contributors 💰🤝💰

This project was developed to use inside Dev. Community Mauá, but feel free to help!.

- Bruno Vilardi - [Brvilardi](https://github.com/Brvilardi) 👷‍♂️
- Hector Guerrini - [hectorguerrini](https://github.com/hectorguerrini) 🧙‍♂️
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) 😎
- Luigi Trevisan - [LuigiTrevisan](https://github.com/LuigiTrevisan) 🔙 
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio) 🌞

## Contact us 📞
If you have any questions, feel free to contact us! You can find us in our [Discord](https://discord.gg/Yr2VPgAmcb) server.
