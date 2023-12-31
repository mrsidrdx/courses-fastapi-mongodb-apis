# FastAPI, Beanie, MongoDB REST APIs Project

This project aims to provide a RESTful API using FastAPI, Beanie, and MongoDB. It allows users to perform CRUD operations on courses stored in a MongoDB database. 

## Installation

1. Copy the `.env.example` file located in the root directory of the project and create a new file named `.env`. Update the values in the `.env` file according to your environment.

2. In the `scripts` folder, you will find scripts to parse a `courses.json` file and upload the documents to the MongoDB collection.

3. Build the Docker container by running the following command in the root directory of the project:

   ```shell
   docker-compose up --build
   ```
   
## Usage

To interact with the API, you can use any HTTP client, such as cURL or Postman. The base URL for the API is http://localhost:8000. The docs for the API is http://localhost:8000/docs. 

## Endpoints

The following endpoints are available:

- **GET /v1/courses**: Retrieves a list of available courses.
- **GET /v1/courses/{course_id}**: Get a Course by Id.
- **GET /v1/chapters/{chapter_id}**: Get a Chapter by Id.
- **POST /v1/chapters/rating**: Update rating of a chapter. Provide the chapter rating details in the request body.

## Running Tests

To run the tests, ensure that the Docker container is running, and then execute the following command:

```shell
docker-compose exec server pytest .
```

This command will run the test suite and display the results.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the project, please submit a pull request or open an issue on the project repository.

## License

This project is licensed under the **MIT License**. Feel free to use and modify it as per your needs.
