# XRPL-XUMM Service

This is a microservice designed for a decentralized application (dApp) for second-hand product listings using the XRP Ledger (XRPL) for payments and NFTs as authenticity tokens. This service integrates with RabbitMQ for event-driven messaging, Xumm for user authentication, and MongoDB for data persistence.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Metrics and Monitoring](#metrics-and-monitoring)
- [Ngrok Setup](#ngrok-setup)

## Overview

This service provides the backend for a second-hand marketplace, handling functionalities like user authentication using Xumm, managing payments on the XRPL, and communicating via RabbitMQ. The service uses FastAPI for building the REST API and Dependency Injection for modular and scalable components.

## Features
- **User Authentication**: Using the Xumm wallet for secure XRPL-based authentication.
- **Payments and NFTs**: Management of XRPL payments and creation of NFTs for second-hand products.
- **Event-Driven Messaging**: Integration with RabbitMQ for asynchronous communication.
- **Persistence**: MongoDB for storing user and product information.
- **Prometheus Monitoring**: Metrics endpoint to monitor the health and performance of the service.

## Architecture

The project follows a layered architecture to ensure separation of concerns:
- **Core**: Contains the main business logic and use cases.
- **Infrastructure**: Handles external dependencies such as database clients, RabbitMQ, and XRPL.
- **Interfaces**: Defines the API endpoints for interacting with the service.
- **Services**: Encapsulates various services such as XRPL, RabbitMQ, and Xumm, using the repository pattern.

### Project Structure
```
.
├── Dockerfile
├── README.md
├── alerts.yml
├── docker-compose.yml
├── logs
├── post.http
├── prometheus.yml
├── requirements.txt
├── src
│   ├── core
│   │   ├── entities
│   │   ├── repositories
│   │   ├── schemas
│   │   └── use_cases
│   ├── dependencies
│   ├── infrastructure
│   ├── interfaces
│   │   └── api
│   ├── main.py
│   ├── middleware
│   └── services
└── tests
```

## Installation

To run this service locally, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   Use the `requirements.txt` file to install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file with necessary configurations such as database URIs, RabbitMQ host, XRPL URL, Xumm API keys, etc.

## Configuration

- **Docker**: The `Dockerfile` and `docker-compose.yml` files are provided to containerize and orchestrate the services.
- **Prometheus**: Metrics are configured using `prometheus.yml` and can be monitored for application health.
- **Alerts**: The `alerts.yml` file defines alerting rules for important metrics.

## Running the Application

### Using Docker Compose
To run the service with Docker Compose:
```sh
docker-compose up --build
```

### Running Locally
Make sure RabbitMQ, MongoDB, and Redis are running and then start the service:
```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- **GET `/api/v1/health`**: Checks the health of the service.

### XRPL Authentication
- **GET `/api/v1/xumm/auth/`**: Initiates user authentication using Xumm.
- **POST `/api/v1/xumm/webhook`**: Receives Xumm webhook callback for authentication completion.

### User Account Management
- **GET `/api/v1/xrpl/account/`**: Retrieves account information from XRPL.

## Testing

Unit tests are available in the `tests` directory. To run the tests:
```sh
pytest tests/
```

## Metrics and Monitoring
- **Prometheus Metrics**: Expose metrics via `/metrics` endpoint to monitor the health and performance.
- **Logs**: Application logs are stored in the `logs` directory.

To enable monitoring and alerts, configure Prometheus using the `prometheus.yml` and start it using Docker Compose along with the application.

## Ngrok Setup

To test the Xumm webhook locally, you can use [Ngrok](https://ngrok.com/) to expose your local server to the internet. This is useful for receiving callbacks from Xumm.

### Steps to Set Up Ngrok

1. **Install Ngrok**
   Download and install Ngrok from [https://ngrok.com/download](https://ngrok.com/download).

2. **Start Ngrok**
   Run Ngrok to expose your local server. For example, if your service is running on port 8000:
   ```sh
   ngrok http 8000
   ```

3. **Update Webhook URL**
   Use the generated Ngrok URL (e.g., `https://<random-string>.ngrok.io`) and update the Xumm webhook URL to point to `https://<random-string>.ngrok.io/api/v1/xumm/webhook`.

Ngrok allows Xumm to send webhook callbacks to your local machine, enabling you to test the authentication flow end-to-end.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
