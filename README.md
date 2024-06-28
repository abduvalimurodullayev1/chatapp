# ChatApp

ChatApp is a real-time chat application built using Django and Django REST Framework (DRF) with WebSocket functionality. The application allows users to send and receive messages instantly and supports private group chats.

## Features

- **User Authentication**: Sign up, login, and manage user profiles.
- **Real-Time Messaging**: Send and receive messages instantly using WebSockets.
- **Private Group Chats**: Create and manage private group chats.
- **User Management**: Follow and unfollow users.

## Prerequisites

- Python 3.10+
- Django 3.2+
- Django REST Framework 3.12+
- Channels 3.0+

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abduvalimurodullayev1/chatapp.git
    cd chatapp
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Configuration

1. **Environment Variables**:
    - Create a `.env` file in the root directory and add your environment-specific variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

2. **Settings**:
    - Update `settings.py` to use the environment variables from your `.env` file:
    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv

    load_dotenv()

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG') == 'True'
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
    ```

## Usage

### Real-Time Messaging

1. **Send a Message**:
    - Use the WebSocket endpoint to connect and send a message to another user or group.

2. **Receive Messages**:
    - Messages sent to the user will be received in real-time through the WebSocket connection.

### Managing Groups

1. **Create a Group**:
    - Use the API endpoint `POST /api/groups/` to create a new group.

2. **Add Members to Group**:
    - Use the API endpoint `POST /api/groups/{id}/add_member/` to add a member to the group.

### API Endpoints

- **POST /api/messages/**: Send a new message.
- **GET /api/messages/**: Retrieve all messages.
- **GET /api/messages/{id}/**: Retrieve a specific message.
- **POST /api/groups/**: Create a new group.
- **GET /api/groups/**: Retrieve all groups.
- **GET /api/groups/{id}/**: Retrieve a specific group.
- **POST /api/groups/{id}/add_member/**: Add a member to a group.
- **DELETE /api/groups/{id}/remove_member/**: Remove a member from a group.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature-branch
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m "Description of changes"
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature-branch
    ```
6. **Create a Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)

## Contact

For any questions or suggestions, feel free to reach out to the project maintainer.
