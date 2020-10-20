# schema-collaboration
## Introduction
schema-collaboration is a tool in the form of web platform to help data managers and researchers to collaborate to create Frictionless datapackages.

In order to use this application some familiarity with Frictionless Datapackages is required. You can find information on the [Frictionless website](Frictionless website) or the [Data Package specification](https://specs.frictionlessdata.io/data-package/)

schema-collaboration uses [datacreator-ui](https://github.com/frictionlessdata/datapackage-ui): see the [datacreator-ui demo](https://create.frictionlessdata.io/)

It was founded by Frictionless Data Tool Fund. There is a [blog with the initial description.](https://frictionlessdata.io/blog/2020/07/16/tool-fund-polar-institute/#meet-carles-pina-estany)

## Quick guide to use schema-collaboration
The documentation tries to do a tour on the different parts of the application. If anyone would like to explore this by themselves a quick guide:
 * Install the application
 * Login as a data manager
 * Create a Datapackage and add the known information (title, authors, etc.)
 * Create a Person
 * Edit the Datapackage and assign a person to the datapackage
 * Send the link to the Datapackage to the collaborator so they can work on it
 * At any time add comments to the datapackage to be seen either by you only or by the collaborators as well

## Installation
schema-collaboration needs to be installed into a server in order to be used by the data manager and researchers. It is done in Python and Django and there are different ways to set it up:
 * Using a Python virtual environment (see the documentation in the main README file)
 * Using Docker and a sqlite3 database
 * Using Docker and a MariaDB database server (not included)

A data manager with certain familiarity to the command line tools with Docker installed or Python3 installed should be able to install schema-collaboration in their computer.

In order to install it on a server to be used in production a system administrator will need to help to integrate with existing infrastructure (DNS, existing servers, virtual hosts, etc.).

We have tried to make schema-collaboration easier to deploy and please let us know if anything could be done to make it easier for your institution.

schema-collaboration will not hold any research data. This is to keep the installation and administration of the application as easy as possible.

## User account types
 * *Data manager users:* they have access to the "management" area with individual login and password. All the data manager users have access to the same data sets. Find the login in the main page.
 * *Admin user:* this user, using the Django admin web section, can personalise status of the data packages and do actions that are not exposed to the data managers (for example delete or modify comments, delete data packages, etc.)
 * *Researchers:* they do not need any login/password. The data managers will send unique links to them in order to access their datasets. The system is designed this way to avoid creating users, making them keep/recover password, etc.

## Data manager login into schema-collaboration
After the installation of the schema-collaboration in the main page there is a link to the management area. The URL of the schema-collaboration will vary depending on the installation methods but it will like:
 * http://localhost:8000 if it was installed in the local computer
 * https://schema-collaboration.your_institution.org (or similar) if it was installed in one of your servers

In the main page there is a link to the "management area":

![management_area_link](images/homepage_link_to_management_area.png)

After this please login using your credentials:
![login](images/login.png)

The username and password for the datamanager where created during the installation. Please refer to the installation steps to find them.

## Navigation
There is a left-hand side bar to navigate between "Datapackages" and "People". It also shows the user that is logged-in and allows to "Logout". See the options:
![navigation_bar](images/navigation_bar.png)

## Create the first datapackage
The first time that a data manager logins in the system there will be no packages created. The datamanager needs to create a new data package to fill-in with the basic information.

Create the button "Create a Datapackage" in order to create one:
![list_of_datapackages_empty](images/list_of_packages_empty.png)

It will create a new, empty, data package and it will open the Data Package Creator:
![data_creator_empty](images/datacreator_ui_empty.png)

As a data manager fill in all the information that you might know of the data set.

At any time or when finished click on "Save to server".

Then click on "List of datapackages" (TODO 2020-10-20: button to be added!) 

The list of datapackages will contain a new datapackage:
![list_of_packages_one_package](images/list_of_packages_empty_one_package.png)

## Create the first Person
In order to give access to the researchers it is needed to create "People" (TODO 2020-10-20 rename to collaborators?)

Click on the "People" option on the left hand side bar:
![list_of_people_empty](images/list_of_people_empty.png)

Click on "Create a Person" and enter the person's name:
![create_person](images/create_person.png)

schema-collaboration will show the "Person detail" page:
![person_detail](images/person_detail.png)

There are three buttons on above screenshot:
 * "Edit": to edit the person (change the name)
 * "List Datapackages": takes you to the list of datapackages assigned to this user
 * "Copy List Datapackages": copies the link to the datapackages to your clipboard.
 
 If we observe the "List Datapackages" at the moment it is empty:
![list_of_datapackages_for_user_empty](images/list_of_datapackages_for_user_empty.png)

Note that this page doesn't have the left hand side bar. This is an indication that this page is accessible by anyone just having the link: it can be sent to the researcher and will be able to see their datapackages.

## Assign a datapackage to a researcher
Let's click a the "Datapackages" on the left hand side and click on "Options -> Manage Datapackage":
![manage_datapackage](images/manage_datapackage.png)

There is a brief information on the datapackage detail. Here is where you could add Comments for the researchers of for yourself (click on "Private" if the comment is only for you).

Click on "Edit Manage" in order to Manage the Datapackage:
![datapackage_manage_edit](images/datapackage_manage_edit.png)

In this page you are able to Edit this datapackage: change its status and add collaborators. In this case we are adding the "Jane Doe" collaborator and clicking "Save".

Clicking then on "Datapackages" again you can see the "List of Datapackages" and the "Collaborators" column has "Jane Doe":
![list_of_datapackages_with_collaborator](images/list_of_datapackages_with_collaborator.png)

## Options in a Datapackage
Each Datapackage has a different set of options:
![options_for_a_datapackage](images/options_for_datapackage.png)

 * Edit Datapackage: takes you to the "Datapackage creator" in order to make changes to the data package
 * Manage Datapackage: place to add comments and also to edit the datapackage collaborators and status of the datapackage
 * Collaborator View: takes to the accessible without login/password page: this is to be sent to the collaborators. Collaborators can read and write comments, datapackage information, Edit it and Download it

## Download button
The "Download" button appears in different pages with always the same options:
![download](images/download.png)

 * Schema: downloads the JSON schema file
 * Markdown: generates a documentation file formatted on Markdown based on the Schema
 * PDF: generates a PDF file from the Markdown
 
 All the Markdown and PDF information comes from the Schema.
 
An example of the PDF output:
![pdf_output](images/pdf_output.png)

## Collaborator access
The collaborators can have access to the datapackages via two type of links:
 * Datapackage link: give access to one datapackage
 * Collaborator link: give access to all the datapackage that this collaborator is assigned to

The public link to a datapackage can be found in the "Options" in the List of Datapackages.

The public link to all the datapackages for a given users can be found in the "List of People" and the name is "List Datapackages".

Collaborators don not need a username/password: only the unique links.
