# Blog API App

Create blog api 

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)


### Prerequisites

- Python must be installed on your System.

### Installation

1. Clone the repository: `git clone https://github.com/owaisgithub/blog-app-api.git`
2. Navigate to the project directory: `cd blog-app-api`
3. Install python package `pip install virtualenv`
4. Create a virtual env for installing project related dependencies `virtualenv <env-name>`
5. Actiavte the virtual env `<env-name>\Script\activate`
6. Install dependencies: `pip install -r requirements.txt`
7. Do some migration `python manage.py makemigrations`
                     `python manage.py migrate`
                     `python manage.py createsuperuser`  for admin access
8. Start development server `python manage.py runserver`

## Usage

- After development server start. There are some endpoints you can request and get some response from it.
- Endpoints are:
- `localhost:8000/ or 127.0.0.1:8000/`
1. `api/users/create/`   Register or Create a user account to given data in json.
                        Example:- post request
                        {
                            "first_name":"user first name",
                            "last_name":"user last name",
                            "email":"user@gmail.com",
                            "password":"12345678"
                        }
2. `api/users/authenticate/`   After registration you can login with email and password
                               Example:- post request
                               {
                                    "email":"user@gmail.com",
                                    "password":"12345678"
                               }
                               It will give a jwt token as response

3. `api/users/logout/`   It invalidates the token so that the token cannot be used further

4. `api/blog/post/`      Send the data on this endpoint to create a blog post (with jwt token).
                         Example:- post request
                         {
                            "title":"Title of Post",
                            "content":"Content of Post"
                         }

5. `api/blog/post/post_id/` Update the post  (with jwt token)

6. `api/blog/all-posts/`   Get all the blog post (jwt token is not required)

7. `api/blog/comment/post_id/`  send the data on this endpoint for a specific post (with jwt token)
                                Example:- post request
                                {
                                    "content":"Comment"
                                }

8. `api/blog/post-comments/post_id/`  Get all the comments related comments with specific post (jwt token is not required)