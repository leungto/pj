# Project Documentation

## Overview

This project is a seat booking system that allows users to book and reserve seats in various rooms. It utilizes SQLAlchemy for database interactions and Alembic for database migrations.

## Project Structure

- **backend/database/**: Contains the database models and connection logic.
  - `__init__.py`: Marks the directory as a Python package.
  - `connection.py`: Establishes the connection to the database.
  - `models.py`: Defines the database models including `User`, `Room`, `Seat`, `Booking`, `TimeSlot`, and `Reservation`.

- **backend/alembic/**: Contains the migration scripts and environment configuration for Alembic.
  - `env.py`: Configures the Alembic environment for running migrations.

- **backend/alembic.ini**: Configuration file for Alembic, specifying the database URL and settings for migrations.

- **backend/requirements.txt**: Lists the dependencies required for the project, including SQLAlchemy and Alembic.

- **backend/README.md**: Documentation for the project.

## Setting Up the Database

To generate the corresponding database tables based on the models defined in `models.py`, follow these steps:

1. Ensure that your database connection is properly configured in `connection.py`.
2. Use Alembic to create a migration script:
   - Run the command `alembic revision --autogenerate -m "Initial migration"` to create a new migration script based on the models.
3. Apply the migration to the database:
   - Run the command `alembic upgrade head` to create the tables in the database.

This process will create the necessary tables according to the schema defined in your SQLAlchemy models.

## Usage

After setting up the database, you can start implementing the application logic to handle user interactions, bookings, and reservations. Make sure to install the required dependencies listed in `requirements.txt` before running the application.