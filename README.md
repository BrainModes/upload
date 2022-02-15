# Upload Service
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green?style=for-the-badge)](https://www.python.org/)


This service is built for file data uploading purpose. It's built using the FastAPI python framework.

# About The Project

The upload service is one of the component for PILOT project. The main responsibility is to handle the file upload(especially large file). The main machanism for uploading is to chunk up the large file(>2MB). It has three main api for pre-uploading, uploading chunks and combining the chunks. After combining the chunks, the api will upload the file to [Minio](https://min.io/) as the Object Storage.

## Built With

 - [Minio](https://min.io/): The Object Storage to save the data

 - [Fastapi](https://fastapi.tiangolo.com): The async api framework for backend

 - [poetry](https://python-poetry.org/): python package management

# Getting Started


## Prerequisites

The project is using poetry to handle the package. **Note here the poetry must install globally not in the anaconda virtual environment**

```
pip install poetry
```

## Installation

 1. git clone the project
 ```
git clone 
 ```

 2. install the package
 ```
poetry install
 ```
 
 3. create and config the `.env` file

## Docker











