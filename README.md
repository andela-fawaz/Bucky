# Bucky
Bucky is a RESTful bucket list API built with `Flask`. A bucket list is a list of things, experiences or achievements that a person hopes to have or accomplish during their lifetime.
This API allows a user to create and manage his/her bucket lists and their respective items. The APi implements token-based Authentication.

## Installation & Set Up.
Clone this repo:
```
$ git clone https://github.com/andela-fawaz/bucky.git
```

Navigate to the `bucky` directory:
```
$ cd bucky
```

Create a vitual environment:
> Use [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Install the required packages:
```
$ pip install -r requirements.txt
```
Set the required environment configuration key e.g. :
```
export FLASK_CONFIG = 'development'
```
 *OR*

For production :

```
export FLASK_CONFIG = 'production'
```

Set the required environment secret key e.g. :
```
export SECRET_KEY ='your-own-secret-key'
```
>Create the database by running migrations as follows :

1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

>Now the project is fully set up with the database in place


## Usage

Run  
```
python manage.py runserver
```

To test the API, use an API Client such as [Postman](https://www.getpostman.com/) to test the endpoints.

### API Endpoints 


| Actions        | Description           | Requires Authentication |
| ------------- |:-------------:| -------------:|
| POST auth/login    | Logs in a user | False |
| POST auth/register     | Register a new user | False |
| POST api/v1.0/bucketlists | Create a new bucket list   | True |
| GET api/v1.0/bucketlists      | List all created bucket lists | True |
| GET api/v1.0/bucketlists?q=`<query_string>`      | Search for a bucket list by name | True |
| GET api/v1.0/bucketlists?limit=`<limit>`      | Paginates bucket list results. | True |
| GET api/v1.0/bucketlists/`<bucketlist_id>`     | get single bucket list | True |
| PUT api/v1.0/bucketlists/`<bucketlist_id>` | update single bucket list | True |
| DELETE api/v1.0/bucketlists/`<bucketlist_id>`      | Delete a single bucket list | True |
| POST api/v1.0/bucketlists/`<bucketlist_id>`/items      | Create a new item in a bucket list | True |
| PUT api/v1.0/bucketlists/`<bucketlist_id>`/items/`<item_id>` | Update an item in a bucket list | True |
| DELETE api/v1.0/bucketlists/`<bucketlist_id>`/items/`<item_id>`      | Delete an item in a bucket list | True |

- **User Registeration**

append **api/v1.0/register**  to the tail end of the link. i.e:
**http://127.0.0.1:5000/api/v1.0/register**

- Ensure the dropdown to the left of the URL bar is a POST request

- In the body tab on Postman, enter a username and password in JSON format i.e:

```
{
    "username" : "tester",
    "email" : "test@gmail",
    "password" : "test123"
}
```

***Set it by checking on the raw checkbox and clicking on application/json on the text drop down***

![Demo Image](/docs/img/register.png?raw=true)

A successful registeration should return the new user's username, i.e.

```
{"username":"tester"}
```

- **User Login**

This time the link changes to:
**http://127.0.0.1:5000/api/v1.0/login**

- Ensure that the method is a POST request also and log in with the same credentials used to sign up.

```
{"email":"test@gmail.com", "password":"test123"}
```

![Demo Image](/docs/img/login.png?raw=true)

A successful login should return a token and time it takes to expires, e.g :

```
{
    "expiration" : 3600,
    "token" : "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4NjM4NTM2MiwiaWF0IjoxNDg2MzgxNzYyfQ.eyJpZCI6MX0.OOnheGKkPzVB3ounLZiOIhUbT6l3DVSlxkcPBk3E_Dc",
}
```
Copy only the token to be used for Authentication.

- **Create a bucketlist**

This project utilizes **Token Based Authentication** to restrict access to certain resources. Absence
of this token with the methods from here will result in a **401: Unauthorized Access** error.

To create a bucketlist, make a **POST** request to the following URI:
**http://127.0.0.1:5000/api/v1.0/bucketlists**.

In the Authorization tab in the "type" dropdown, select Basic Auth and add your token in the username field.

Give your Bucketlist a title and description and hit send, e.g:

```
{
"title": "Food & Restaurants",
"description":"Food I'd like to try out and restaurants i'd like to visit."
}
```

A successful request should be as follows:

![Demo Image](/docs/img/new_bucketlist.png?raw=true)

To view it you can make a **GET** request to the URI for bucketlists plus the ID of the bucketlists appended:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1**.


- **Update or Delete a bucketlist**

To **UPDATE** a bucketlist, navigate to the full link as stated above i.e:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1** with the method for the URL as **PUT.**

In the body tab, provide your information as follows:

```
{
    "title": "Food Only"
    "description":"Food I'd like to try out."
}
```
A successful update should be as follows:

![Demo Image](/docs/img/update_bucketlist.png?raw=true)

- **Creating a bucket list item**

To create a bucketlist item, make sure you have a bucketlist and navigate to the following url:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items** as a **POST** request.

>1 here represents the ID of the bucketlist you want to add items to.

Add your content:

```
{
    "title": "Chinese Dishes",
    "description":"Would like to try out Sushi",
    "status" : "not done"
}
```
A successful POST request should return the following:

![Demo Image](/docs/img/new_bucketlist_item.png?raw=true)

Make a **GET** request to view the item at the following URI:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1**

- **Updating a bucket list item**

The format takes the same approach as the bucketlist update with the only difference being the URI:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1**

To **DELETE** a bucketlist item, navigate to the full link as stated above i.e:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1** with the method for the URL as **DELETE**.

A successful request should return a HTTP 204 status code as follows:

![Demo Image](/docs/img/delete_bucketlist_item.png?raw=true)

- **Paginantion and searching bucket lists**

Blister also allows you to paginate bucketlists by adding the **limit** parameter to the URI as follows:

**http://127.0.0.1:5000/api/v1.0/bucketlists?limit=1**

![Demo Image](/docs/img/limit_results.png?raw=true)

Searching is also possible using the **q** parameter as follows:

**http://127.0.0.1:5000/api/v1.0/bucketlists?q=food**

![Demo Image](/docs/img/search_bucketlist.png?raw=true)


# TESTS.

Bucky is configured using **Nosetests**. Thus use the command:

```
nosetests --with-coverage --cover-inclusive --cover-package=bucky
```
will successfully run the tests.

### Special Thanks to :

1. [Oluwafemi Sule.](https://github.com/andela-osule)

2. [Shem Ogumbe](https://github.com/andela-sogumbe)



