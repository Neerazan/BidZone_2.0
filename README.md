# BidZone - Real-Time Auction System

BidZone is a sophisticated auction platform built with Django REST Framework that enables users to list products and participate in real-time bidding. The system features JWT authentication, background task processing with Celery, and Redis as a message broker.

## Features

- **User Authentication**: Secure JWT-based authentication system using Djoser
- **Real-time Bidding**: Place and track bids on listed products
- **Product Management**: List and manage products for auction
- **Background Processing**: Celery-based task queue for handling time-sensitive operations
- **API Documentation**: Comprehensive API documentation using Django Spectacular
- **Customer Management**: Handle customer profiles, addresses, and balances
- **Transaction System**: Secure transaction handling for successful bids
- **Wishlist**: Allow users to save and track favorite items
- **Review System**: Product and seller review functionality
- **Collection Management**: Organize products into collections

## Technology Stack

- **Backend Framework**: Django REST Framework
- **Authentication**: JWT (Djoser)
- **Task Queue**: Celery
- **Message Broker**: Redis
- **API Documentation**: Django Spectacular

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd BidZone_2.0
```

2. Install dependencies:
```bash
make install
```

3. Install pre-commit hooks:
```bash
make install-pre-commit
```

4. Set up the database:
```bash
make migrations
make migrate
```

5. Create a superuser:
```bash
make superuser
```

6. Collect static files:
```bash
make collectstatic
```

7. Start the development server:
```bash
make run
```

## Project Structure

```
.
├── src/
│   ├── auction/          # Main auction functionality
│   ├── bidzone/          # Project configuration
│   ├── core/             # Core functionality
│   ├── playground/       # Testing and development area
│   ├── slider/           # Slider management
│   ├── tags/             # Tagging system
│   └── utils/            # Utility functions
├── static/               # Static files
├── media/                # User-uploaded files
└── local/                # Local development settings
```

## API Endpoints

The API is thoroughly documented using Django Spectacular. Major endpoint categories include:

- Auction Management
- Bidding Operations
- Customer Management
- Product Management
- Transaction Processing
- Collection Management
- Review System
- Wishlist Operations

View the complete API documentation at `/api/schema/swagger-ui/` when running the server.

## Development

### Available Make Commands

- `make install`: Install project dependencies
- `make run`: Start the development server
- `make migrate`: Apply database migrations
- `make migrations`: Generate new migrations
- `make lint`: Run linting checks
- `make shell`: Access Django shell
- `make update`: Install dependencies and apply migrations
- `make app name=<app_name>`: Create a new Django app
- `make flush`: Flush the database

### Background Tasks

The project uses Celery for handling background tasks such as:
- Auction completion processing
- Email notifications
- Scheduled maintenance tasks

Make sure Redis is running and Celery worker is started before testing background tasks.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Add your license information here]
