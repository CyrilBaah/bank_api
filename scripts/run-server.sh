#!/bin/bash

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
