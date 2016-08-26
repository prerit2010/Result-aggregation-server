# How to use the website

## Contents

1. Introduction
2. API endpoints
3. Side menu
4. Plots

## Introduction

Result-aggregation-server is a server and API for collecting and viewing the results produced by Installation scripts. The aim of building this project was to analyze the failures of packages that students face during workshops of Software Carpentry and Data Carpentry.

## API endpoints

* `/` : [POST] This endpoint is used by the installation test scripts to submit the results produced by them on the server. Currently following system information is being collected from the installation test scripts:
  * Operating System of User (e.g. Linux, Windows).
  * Linux Distribution name and version (If OS is Linux).
  * System Version (e.g. #53-Ubuntu SMP Wed Jul 27 16:06:39 UTC 2016)
  * Machine info (e.g. x86_64)
  * System Platform (e.g. Linux-4.4.0-34-generic-x86_64-with-Ubuntu-16.04-xenial)
  * Python Version (e.g. 2.7.11)

Apart from the system information, some other information is also collected from the user, which is optional for the user to enter. e.g Workshop Id and email id.

* `/view/` : [GET] This endpoint is used to view the most failed packages for all the workshops and also for those workshops for which user didn't provide the workshop name. For these type of users, the results are aggregated in the category 'No workshop name provided'.

* `/view/<workshop id>/` : [GET] This endpoint is used to view the most failed packages filtered by the workshop name provided.

* `/view/detail/` : [GET] This endpoint is used to view the detail for a failed package selected by the user. Details like, in what type of environment did this package failed, e.g. python version used, operating system etc.

One can also compare between 2 packages.

## Side Menu

Side menu Looks like :

![image](http://imgur.com/oFQLbtW.png)

* **Filter by workshop :** From here workshop id can be selected, and thus it would lead to the endpoint '/view/<workshop id>/'. It also allows to select the 'No workshop name provided category'.

* **Filter by attempts :** As the scripts might have been run by the user many times, so each attempt of the user is tracked down in the database. By default all the visualization of data is done by 'latest attempt' of the user. One can select between **All attempts** and **latest attempt*8 from here.

* **Filter by failed package :** This drop down provides the list of most failed packages, and one can select any one of them to view the details. After selecting a failed package, user has the option to select the version of the failed package. By default 'All' is selected. Clicking on submit leads to '/view/detail/' with all information.

![image](http://imgur.com/Q1Lggat.png)

* **Also Compare with :** Instead of viewing the results for only one failed package, one can select 2 packages to compare the results of the two.

## Plots

On submitting the selected package from the side menu, plots on the '/view/detail/' will appear showing the details of the failed package.

![image](http://imgur.com/336ppgv.png)

* If results are viewed for all workshops, a time series plot will appear first which shows how much this package has been failing over the period of time.

* Several other plots like python version, Operating systems used, etc are also being shown. To view the results in tabular form, a button is provided right below each plot, clicking on which collapses down the tabular view, which can again be closed by clicking on the same button.
