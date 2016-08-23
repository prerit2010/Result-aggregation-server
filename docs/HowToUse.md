### How to use the website

### Contents

1. Introduction
2. API endpoints
3. Side menu

## Introduction

Result-aggregation-server is a server and API for collecting and viewing the results produced by Installation scripts. The aim of building this project was to analyse the failures of packages that students face during workshops of Software Carpentry and Data Carpentry.

## API endpoints

* `/` : [POST] This endpoint is used by the installation test scripts to submit the results produced by them on the server. Currently following information is being collected from the installation test scripts:
  * Operating system of the user ()