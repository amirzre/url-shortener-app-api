<h1 align="center"> URL Shortener APP API </h1> <br>

<h3 align="center">
  An Url Shortener Backend to Short Links. Built with Python/Django Rest Framework.
</h3>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation Process](#installation-process)

## Introduction

DRF Url Shortener API provides API endpoints to short links. Built with Python/Django.

## Features

A few of the futher on this app:

* Custom User Athentication
* JWT Token Autentication
* Authorized User Can Edit And Delete Own Links
* Unauthoriz User Just Can Create Shortener Links
* TDD Tests
* Dockerizd Project

## Installation Process

**Installation Process (Linux)**

1. Install docker engine `https://docs.docker.com/engine/install/`
2. Install docker compose `https://docs.docker.com/compose/install/`
3. Clone This Project `git clone git@github.com:zanull/url-shortener-app-api.git`
4. Go To Project Directory `cd url-shortener-app-api`
5. Build docker images `sudo docker compose build`
6. Do make migrations `sudo docker compose run --rm app sh -c "python3 manage.py makemigrations"`
7. Run the project `sudo docker compose run`
