[![ci](https://github.com/talaman/hexagonal-pager/actions/workflows/ci.yml/badge.svg)](https://github.com/talaman/hexagonal-pager/actions/workflows/ci.yml)

# Hexagonal Pager System

This repository implements a Pager system using Domain-Driven Design (DDD) and Hexagonal Architecture principles. The system is designed to handle alerts and notifications for monitored services.

## Table of Contents

- [Hexagonal Pager System](#hexagonal-pager-system)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Architecture](#architecture)
    - [Domain Layer](#domain-layer)
    - [Application Layer](#application-layer)
    - [Ports Layer](#ports-layer)
    - [Adapters Layer](#adapters-layer)
  - [Getting Started](#getting-started)
  - [Running Tests](#running-tests)
  - [Continuous Integration](#continuous-integration)

## Overview

The Hexagonal Pager System is built to manage and escalate alerts for various monitored services. It uses DDD to model the core business logic and Hexagonal Architecture to ensure the system is modular, testable, and adaptable to different technologies and interfaces.

## Architecture

### Domain Layer

The Domain Layer contains the core business logic and domain models. It is independent of any external systems or frameworks. This layer is the heart of the application, encapsulating the business rules and ensuring that the system behaves correctly.

- **Models**: Represent the core entities and value objects in the system.
  - [`EscalationPolicy`](pager/domain/models/escalation_policy.py): Defines the rules for escalating alerts.
  - [`MonitoredService`](pager/domain/models/monitored_service.py): Represents a service being monitored.
  - [`NotificationTarget`](pager/domain/models/notification_target.py): Represents the target to be notified.
- **Events**: Define the domain events that occur within the system.
  - [`Alert`](pager/domain/events.py): Triggered when an alert is raised.
  - [`Acknowledgement`](pager/domain/events.py): Triggered when an alert is acknowledged.
  - [`HealthyEvent`](pager/domain/events.py): Triggered when a service is healthy.
  - [`Timeout`](pager/domain/events.py): Triggered when an alert times out.
- **Services**: Contain the business logic and domain services.
  - [`PagerService`](pager/domain/services/pager_service.py): Handles the core logic for managing alerts and notifications.

### Application Layer

The Application Layer orchestrates the use cases and application logic. It interacts with the Domain Layer to fulfill the application's requirements. This layer is responsible for coordinating the application activities and ensuring that the use cases are executed correctly.

- **Application Services**: Implement the use cases of the application.
  - [`PagerApplicationService`](pager/application/pager_application_service.py): Coordinates the alerting process and interacts with the domain services.

### Ports Layer

The Ports Layer defines the interfaces for the external systems and services that the application interacts with. This layer acts as a boundary, ensuring that the core application logic remains decoupled from the external systems.

- **EmailSender**: Interface for sending emails.
  - [`EmailSender`](pager/ports/email_sender.py): Defines the contract for sending email notifications.
- **SmsSender**: Interface for sending SMS.
- **EscalationPolicyRepository**: Interface for accessing escalation policies.
  - [`EscalationPolicyRepository`](pager/ports/escalation_policy_repository.py): Defines the contract for accessing escalation policies.

### Adapters Layer

Ommited for now.

The Adapters Layer implements the interfaces defined in the Ports Layer. It adapts the external systems and services to the application's requirements. This layer is responsible for translating the data and interactions between the application and the external systems.

## Getting Started

To get started with the Hexagonal Pager System, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/talaman/hexagonal-pager.git
    cd hexagonal-pager
    ```

2. **Build the Docker image**:
    ```sh
    docker build -t hexagonal-pager .
    ```

3. **Run the application**:
    ```sh
    docker run -d hexagonal-pager
    ```

## Running Tests

To run the tests, use the following command:

```sh
docker run --rm hexagonal-pager pytest
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The CI pipeline is defined in .github/workflows/ci.yml and includes the following steps:

- Checkout code: Uses the actions/checkout@v3 action to checkout the code.
- Set up Python: Uses the actions/setup-python@v4 action to set up Python 3.12.
- Install dependencies: Installs the required dependencies using pip.
- Run tests: Runs the tests using pytest.
- Build and export to Docker: Uses the docker/build-push-action@v6 action to build and export the Docker image.

The CI pipeline is triggered on every push to the main branch and runs the tests to ensure the code quality and functionality.

