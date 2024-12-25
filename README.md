# BidZone Auction System

BidZone is a dynamic auction and bidding platform where users can list products for auction and allow others to bid on them. The bidder with the highest bid within the defined time frame wins the auction. The project implements robust features like user authentication, API documentation, background task processing, and more.

---

## Features

### Core Features
- **Product Listings**: Users can list their products for auctions.
- **Bidding System**: Registered users can place bids on active auctions.
- **Winner Selection**: Automatically selects the highest bidder as the winner when the auction ends.
- **API Documentation**: Detailed API documentation using Django Spectacular.

### Authentication
- JWT Authentication powered by Djoser.
- Secure token-based access to all endpoints.

### Background Tasks
- Background tasks are managed using **Celery**.
- **Redis** is used as a message broker for reliable task queuing.

### Storage
- Static files and media files are organized for easy access and scalability.

---

## Project Structure

```
BidZone
├── Makefile
├── Pipfile
├── Pipfile.lock
├── celerybeat-schedule
├── local
│   └── settings.dev.py
├── media
│   └── auction
│       └── images
├── pyproject.toml
├── src
│   ├── __init__.py
│   ├── auction
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── templates
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── bidzone
│   │   ├── settings
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── views.py
│   ├── manage.py
│   └── utils
│       └── slugs.py
└── static
    ├── admin
    ├── auction
    ├── debug_toolbar
    └── rest_framework
```

---

## Requirements

- Python 3.10+
- Django
- Pipenv
- Redis
- Celery

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/BidZone.git
   cd BidZone
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

3. **Setup environment variables:**
   Create a `.env` file with the required configurations.

4. **Run migrations:**
   ```bash
   make migrate
   ```

5. **Run the development server:**
   ```bash
   make run
   ```

6. **Start Celery worker:**
   ```bash
   celery -A src worker --loglevel=info
   ```

7. **Start Redis server:**
   Ensure Redis is running locally or on a remote server.

---

## API Documentation

- The API documentation is accessible at `/api/schema/swagger-ui/`.
- The documentation is generated using **Spectacular Settings**:

  ```python
  SPECTACULAR_SETTINGS = {
      'TITLE': 'BidZone API',
      'DESCRIPTION': 'API documentation of BidZone',
      'VERSION': '1.0.0',
      'TAGS': [
          {'name': 'Auction', 'description': 'Auction related endpoints'},
          {'name': 'Bids', 'description': 'Auction bids related endpoints'},
          {'name': 'Customer', 'description': 'Customer related endpoints'},
          ...
      ],
  }
  ```

---

## Usage

### Create a New App
```bash
make app name=<app_name>
```

### Run Pre-commit Checks
```bash
make lint
```

### Collect Static Files
```bash
make collectstatic
```

---

## License

This project is licensed under the MIT License.

---
