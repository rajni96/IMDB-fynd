
# IMDB clone

IMDB clone movie APIs has 4 methods **GET**, **POST**, **PUT** and **DELETE** to perform operations on the incoming requests.


##  Get Movies 
#### Method: *GET*
#### Request URL: https://imdb-fynd-task.herokuapp.com/imdb/api/movies/list?limit= `limit`& offset=`offset`&_search=`movie_name`
#### Authentication Required: NO
#### Headers Required:
```sh
Content-Type: application/json
```
#### Description:
(__Provide a movie name or part of it in the query params [_search_] to get the list of movies from the database.__)
Return the list of movies and success status code __*200*__  . In case of exception it will return a error message and error status codes __*500*__. 

## Insert Movie
#### Method: *POST*
#### Request URL: https://imdb-fynd-task.herokuapp.com/imdb/api/movies/add
#### Authentication Required: YES
#### Headers Required:
```sh
Content-Type: application/json
Authorization: Bearer LXFFAV5o27s0mlV3508QDz104ASVJ
```
#### Request Data <Sample Data>: 
```sh
{
	"name": "Ironman",
	"director": 13,
	"genre": [2,3,5],
	"imdb_score": 5.2,
    "popularity": 50
}
```

#### Description:
(__Provide the movie data as JSON data to add the movie into the database.__)
Add the movie with the name, director, genre etc provided in request and return newly added movie with success status code as __*200*__. Same movie name and director can't be added if already exist return error message and error status code as __*400*__. In case of exception it will return a error message and error status codes __*500*__. 

## Update Movie
#### Method: *PATCH*
#### Request URL: https://imdb-fynd-task.herokuapp.com/imdb/api/movies/update
#### Authentication Required: YES
#### Headers Required:
```sh
Content-Type: application/json
Authorization: Bearer LXFFAV5o27s0mlV3508QDz104ASVJ
```
#### Request Data <Sample Data>: 
```sh
{
	"id":5,
	"name": "Ironman",
	"director": 13,
	"genre": [2,3,5],
	"imdb_score": 5.2,
    "popularity": 50
}
```
#### Description:
(__Provide the movie data as JSON data to update the movie into the database.__)
Update the movie with the JSON data provided in request and return updated movie JSON if successfully saved with success status code as __200__.If the movie and director combination already exists then return error message and error status code as __400__.If given movie id does not exist in database will return a error message and status code as  __404__.In case of exception it will return error message and error status codes as __500__.

## Delete Movie
#### Method: *DELETE*
#### Request URL: https://imdb-fynd-task.herokuapp.com/imdb/api/movies/delete?id=`movie_id`
#### Authentication Required: YES
#### Headers Required:
```sh
Content-Type: application/json
Authorization: Bearer LXFFAV5o27s0mlV3508QDz104ASVJ
```
#### Description:
(__Provide the movie in query params [id] to delete the movie into the database.__)
 Delete the movie with the id provided in request return the success message and success status code as __*200*__. If given movie id does not exist in database will return a error message and status code as  __404__.In case of exception it will return error message and error status codes as __500__.
