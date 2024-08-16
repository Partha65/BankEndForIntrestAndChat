# InterestChatAPI - Django Backend

This is the backend for the InterestAndChat application, built using Django and Django Rest Framework. The API provides user authentication, interest requests, chat functionality, and real-time messaging with WebSocket integration.

## Features

- **User Authentication**: Users can register, log in, and obtain authentication tokens.
- **Interest Requests**: Users can send, accept, and reject interest requests.
- **Real-Time Chat**: Once interest requests are accepted, users can chat in real time using WebSockets.
- **List of Users**: Provides a list of users to whom interest requests can be sent.
- **Accepted Interests**: Allows users to view who accepted their requests and start a conversation.

## Requirements

- Python 3.x
- Django 4.x
- Django Rest Framework
- Django Channels
- Channels (for channel layer)
- Postman (for API testing)

## Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/Partha65/BankEndForIntrestAndChat.git
```
# Install the Required Dependencies*
pip install -r requirements.txt

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

# Run the Development Server
python manage.py runserver


