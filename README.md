# Jouster Project - Assignment
> A web application for text analysis using LLMs.

## Prerequisites
- Docker and Docker Compose installed on your machine.

## Technologies Used
- Django REST Framework for backend API.
- React (NextJs) for frontend UI.
- Shadcn UI components.
- OpenAI API for text analysis. (extendable to other LLMs)
- SQLite for development database.

## Setup Instructions
Run the following commands in your terminal:
1. `make cp-envs`
1. Please set your OpenAI API key in the `.env.api` -> [link](./envs/.env.api) <- file created.
1. `make install`
1. Access simple UI [http://localhost:3000](http://localhost:3000)

## Running Tests
> Simplified integration test

Run tests with: `make test`

## To-Do
- [ ] Batch processing for multiple text inputs.
- [ ] Include confidence score

## Design Choices
TLDR; The project uses a modular, domain-driven Django backend and a separate Next.js frontend for clear separation of concerns and maintainability. External LLM integrations are abstracted via the LLMManager, enabling easy extension to other providers. Dockerized environments and strong type safety ensure scalable, reproducible development and future growth.


- External calling to LLMS is abstracted via the `LLMManager` class, allowing easy extension to other LLM providers in the future.
- API and Frontend separation of concerns
- Modular django app structure, separated by it's own domain, domain driven design.
- Dockerized (development env. only for now) allowing isolated and reproducible environment setup. Simplifying onboarding and development.
- Ensure type safety when possible with TypeScript, Pydantic and Django models/serializers.
- Scalable and maintainable code structure supports future growth, new feature and enhance team collaboration.

## Trade-offs (Timeboxed project)
- Super minimal testing
- Frontend structure could be improved.
- API Throttling, Rate limiting, Caching not implemented.
- Background tasks/queueing not implemented.
- Docker setup is basic for development only, production setup would need more considerations.
- Coding structure or patterns could be further improved with more time.
- API responser as well as error handling or exceptions could be more robust and standardized.

