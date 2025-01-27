Library Occupancy Detection System

About the Project
The Library Occupancy Detection System is a web-based application designed to monitor and display real-time occupancy data for libraries. This system leverages sensors to detect whether a library is occupied and provides up-to-date information to users via an intuitive web interface.

Technologies Used

Frontend: HTML, CSS
Backend: python
Database: SQLite,Django
IDE: Visual Studio Code

Authors:
shahed alhwashla 
safa hzel
amina ibdah
mohamad abo abid 

Getting Started
Follow the instructions below to set up and run the project on your local machine.

Prerequisites

Install Python:
Download and install Python from the official website: https://www.python.org/downloads/.
Install Django:
Run the following command in your terminal:
pip install django
Setting Up the Environment

Create a virtual environment:
bash
Copy
Edit
python -m venv venv  
source venv/bin/activate  (On Windows: venv\Scripts\activate)
Install dependencies:
pip install -r requirements.txt
Apply Database Migrations
Set up the database using Django migrations:
python manage.py makemigrations  
python manage.py migrate  
Run the Server


Start the development server with the following command:
python manage.py runserver  
Open your browser and navigate to http://127.0.0.1:8000/ to interact with the application.

Run the Tests
To ensure the system is functioning correctly, run:
python manage.py test  
Database Connection Configurations
The Library Occupancy Detection System uses SQLite as its default database engine.

Current Configuration (settings.py):
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.sqlite3',  
        'NAME': BASE_DIR / 'db.sqlite3',  
    }  
}
Features

Real-time Occupancy Updates: Live updates on library occupancy status.
Sensor Integration: Automatically detects and reports library status based on sensor inputs.
User-Friendly Interface: Clean and interactive web pages for users.
Changes to Requirements

Added Features:
Library Status Dashboard: A dashboard displaying real-time data for multiple libraries.
Admin Panel Enhancements: Improved management tools for sensor data and occupancy records.
Removed Features:
User Profile Management: Removed to streamline the project focus on occupancy tracking.
Admin Panel Overview
The admin page allows for efficient data management and includes:

Library Table: Detailed records of each library's occupancy data.
Sensor Management: Tools for managing and configuring sensors.
Data Export: Export data for analysis or backup purposes.
Architecture Model: MVC (Model-View-Controller)

Model

Description: Responsible for managing the system's data.
Stores core data such as library details, occupancy statuses, and sensor records.
Role:
Manages data independently of the user interface.
Handles database operations, including storing, retrieving, and updating information.
View

Description: Presents data to the user in a clean and interactive format.
Includes the user interface built with HTML, CSS, and JavaScript.
Role:
Displays data like library occupancy.
Allows user interactions, such as navigating between libraries.
Controller

Description: Manages application logic and coordinates user requests.
Implemented using Django to process requests, interact with the database, and send responses.
Role:
Bridges the Model and the View.
Handles actions like retrieving sensor data and updating occupancy statuses.
