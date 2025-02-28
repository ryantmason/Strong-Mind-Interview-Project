# Strong-Mind-Interview-Project
 This take-home project is part of the StrongMind technical assessment. Based on the provided user stories, I interpreted the project as an employee access system for managing a Pizza Shop's menu.

 
## Table of Contents
- [Installation](#installation)
- [Testing](#testing)
- [Technical Choices Overview](#technical-choices-overview)
- [Features](#features)
- [Credits](#credits)


## Installation
Ensure you have docker installed locally [Docker Installation Guide](https://docs.docker.com/get-docker/)
- git clone https://github.com/yourusername/Strong-Mind-Interview-Project.git
- cd path/to/Strong-Mind-Interview-Project
- In a PowerShell window
    - run `docker compose up --build`
- Once the container is running, you can access the application at http://localhost:8000/.


## Testing
- Open the console in the docker container or a powershell window in the project directory
    - run `python manage.py test app.core.tests.tests.PizzaAppTests`


## Technical Choices Overview
### Django
- Built-in ORM to support the PostgreSQL database, storing all relevant Pizza and Topping data.
- Built-in authentication system for easy user group management. -- Simple Username/Password authentication (Users can select their desired role).

### Docker
- Simplifies local deployment and dependency management.
- Ensures a consistent development environment.


## Features
### Role-Based Access Control (RBAC)
- Pizza Store Owners can manage both the Pizza Menu and Available Toppings.
- Pizza Chefs can only manage the Pizza Menu.

### CRUD Operations
- Add, update, and delete pizzas and toppings.
- Update topping availability. (Built to support potential inventory system)

### Dynamic Web Application 
- Uses Django views to handle HTTP requests and modify database records.  
- AJAX-powered interactions for smoother user experience.  
- Built-in Django templates with basic responsive design.  


## Credits
Ryan Mason
