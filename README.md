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
    - [The Environment](#the-environment)
      - [Option 1: Dev Containers](#option-1-dev-containers)
      - [Option 2: Manually](#option-2-manually)
    - [Creating image artifact and running the application with Docker](#creating-image-artifact-and-running-the-application-with-docker)
  - [Continuous Integration](#continuous-integration)
  - [Further Improvements](#further-improvements)

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

Clone the repository:
```sh
git clone https://github.com/talaman/hexagonal-pager.git
cd hexagonal-pager
```

### The Environment 

#### Option 1: Dev Containers

I have included a vscode devcontainer configuration to make it easier to get started with the project. If you have vscode, the Dev Containers extension and Docker installed, you can open the project in a container and have all the dependencies set up automatically.

Just open the project in vscode and click on the "Reopen in Container" button when prompted.

When the container is ready, you can run the tests using the following command in the terminal:

```sh
pytest
``` 

#### Option 2: Manually

Otherwise, get your preferred Python environment set up, I have used 3.12 for this project.

Install the dependencies:
```sh
pip install -r requirements.txt
```

When the dependencies are installed, you can run the tests using the following command in the terminal:

```sh
pytest
```

### Creating image artifact and running the application with Docker

As a production-ready application, the Pager System can be packaged as a Docker image and run in a containerized environment. This is automated with the CI pipeline, but here is an example of how to build and run the application with Docker:

1. **Build the Docker image**:
    ```sh
    docker build -t hexagonal-pager .
    ```
2. **Test the application**:
    ```sh
    docker run --rm hexagonal-pager pytest
    ```
3. **Run the application**:
    This is an example of how to run the application. But a real application would have an adapter layer to interact with external systems.
    ```sh
    docker run -d hexagonal-pager
    ```

Then you can push the image to a container registry and deploy it to your preferred container orchestration platform.

## Continuous Integration

[![ci](https://github.com/talaman/hexagonal-pager/actions/workflows/ci.yml/badge.svg)](https://github.com/talaman/hexagonal-pager/actions/workflows/ci.yml)

This project uses GitHub Actions for continuous integration. The CI pipeline is defined in .github/workflows/ci.yml and it runs tests in 2 different environments: Github hosted runners and Docker. 

It includes the following steps:

- Checkout code: Uses the actions/checkout@v3 action to checkout the code.
- Set up Python: Uses the actions/setup-python@v4 action to set up Python 3.12.
- Install dependencies: Installs the required dependencies using pip.
- Run tests: Runs the tests using pytest.
- Build and export to Docker: Uses the docker/build-push-action@v6 action to build and export the Docker image.

The CI pipeline is triggered on every push or pull request to the main branch, and runs the tests to ensure the code quality and functionality.

## Further Improvements

- Implement the Adapters Layer to integrate with external systems.
- Add more use cases and scenarios to cover additional functionalities.
- Ensure the Pager Service handles concurrency issues, such as preventing multiple notifications to the same target when multiple alerts are received simultaneously.
- Define the expected guarantees from the database regarding consistency and reliability.
- Implement a robust test strategy to cover all edge cases and concurrency scenarios.