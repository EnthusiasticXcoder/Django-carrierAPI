# Django-carrierAPI

Django-carrierAPI is a RESTful API designed for user authentication and sending blog and career data. Built with Django, Django Rest Framework, and Python, this API serves responses when called by clients, providing seamless integration with various applications and services.

## Features

1. **User Authentication**
   - Secure user authentication system to manage user access.
   - Supports token-based authentication for API requests.

2. **Blog and Career Data**
   - Provides endpoints to retrieve and manage blog and career-related data.
   - Allows clients to fetch information about blogs and careers for display or analysis.

3. **RESTful API**
   - Built following RESTful principles for standardized communication.
   - Utilizes HTTP methods such as GET, POST, PUT, and DELETE for CRUD operations.


## Technologies Used

- Django: High-level Python web framework for rapid development and clean design.
- Django Rest Framework: Toolkit for building Web APIs in Django.
- Python: Programming language used for backend development.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EnthusiasticXcoder/Django-carrierAPI.git
   ```

2. Change to the project directory:
   ```bash
   cd Django-carrierAPI
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Environment Variables:

   To run this project, you will need to add the following environment variables to your .env file

   - `SECRET_KEY` : SECRET_KEY of your Django Project.

   - `DEBUG` : DEBUG value True or False

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

| Endpoint                | Method  | Description                                               | Data                                            | Authorization Token |
|-------------------------|---------|-----------------------------------------------------------|-------------------------------------------------|---------------------|
| /users/register         | `POST`  | Register a new user.                                      |first_name, last_name, email, username, password | No                  |
| /users/login            | `POST`  | User login.                                               |username, password                               | No                  |
| /users/                 | `GET`   | Retrieve the user with the help of Token.                 |                                                 | Yes                 |
| /users/                 | `PUT`   | Update password of a user with the help of Token.         |password                                         | Yes                 |
| /users/                 | `DELETE`| Delete a user with the help of Token.                     |                                                 | Yes                 |
| /blog/menu/             | `GET`   | Retrieve a list of available careers Data.                |                                                 | No                  |
| /blog/list/             | `GET`   | Retrieve a list of all blogs of HomePage.                 |                                                 | No                  |
| /blog/list/             | `POST`  | Retrieve a list of all blogs of Particular career option. |url                                              | No                  |
| /blog/content/          | `POST`  | Retrieve content of a specific blog by URL.               |url                                              | No                  |


## Usage

- Access the API endpoints using your preferred HTTP client or tools like Postman.
- Refer to the API documentation or codebase for available endpoints and usage instructions.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Django](https://www.djangoproject.com/): High-level Python web framework for rapid development and clean design.
- [Django Rest Framework](https://www.django-rest-framework.org/): Toolkit for building Web APIs in Django.