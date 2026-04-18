# Life-Canvas-App
A place to do find everyday task organising and getting best for yourself all at one place.
# Life Canvas

 
**Aditya Dubey**

Life Canvas is a prototype platform that helps customers plan, manage, and coordinate multiple services from one unified dashboard. Instead of switching between separate apps for food, healthcare, travel, home services, or event planning, the customer can create a structured workflow, assign providers, prioritize tasks, and control how service providers collaborate with each other [web:624][web:633].

## Problem

Today, customers often use disconnected platforms for different needs. This creates repeated data entry, poor coordination between providers, delays in execution, and limited control over personal information [web:633][web:635].

For example:
- Booking an event may require venue, catering, decoration, and electrical setup.
- Managing travel may involve transport, food, accommodation, and other services.
- Healthcare journeys may require records, guidance, and sequential support.

In all of these cases, the customer usually becomes the manual coordinator.

## Solution

Life Canvas acts like a **personalized life dashboard** or **digital canvas** where the customer can:
- Add tasks and service needs in one place.
- Organize tasks by category and dependency.
- Select providers based on trust, activity, and collaboration readiness.
- Control whether information from one task can be shared with another provider.
- Track workflow progress through orchestration and trust summary.

The core idea is simple:

**Your money. Your data. Your priorities. Your choice.**

## Key Features

- **Customer Registration Vault**  
  Stores customer profile, preferences, and important information such as health ID, food preferences, payment mode, and other details.

- **Canvas-Based Task Planning**  
  Lets users create and manage tasks like a to-do board for real-life services.

- **Provider Discovery**  
  Shows providers by category and allows filtering based on:
  - Active communicators
  - Collaboration readiness
  - Category match

- **Task Orchestration**  
  Supports dependencies between tasks such as:
  - Independent
  - After previous task
  - Parallel

- **Controlled Collaboration**  
  Allows providers to collaborate only when:
  1. The customer permits it
  2. The service provider is open to collaboration

- **Trust Summary**  
  Gives a simple score based on workflow completion and delays.

## Prototype Use Cases

The current prototype demonstrates workflows such as:
- Travel + Food
- Event Planning
- Home Repair

These examples show how one task can trigger or affect another based on workflow status.

## How It Works

1. The customer registers profile details.
2. The customer creates or selects tasks on the dashboard.
3. Providers are assigned by category.
4. The user decides whether collaboration is allowed.
5. The system checks dependencies between tasks.
6. If one task is delayed, the next task can be blocked or adjusted.
7. A trust summary reflects the workflow status.

## Example Scenario

For event planning:
- The customer adds tasks like venue booking, catering, decoration, and electrical setup.
- Providers are selected for each task.
- If collaboration is enabled, providers can work with context from previous tasks.
- If a delay occurs in one service, the next dependent service can be updated accordingly.

## Tech Stack

- **Frontend:** Streamlit
- **Language:** Python
- **Data Layer:** JSON-based mock data
- **Modules:**
  - Load Data
  - Recommender
  - Orchestrator
  - Permissions

## Project Structure

```bash
life_canvas/
│
├── app.py
├── data/
│   ├── customer_profile.json
│   ├── providers.json
│   └── tasks.json
│
└── utils/
    ├── __init__.py
    ├── load_data.py
    ├── recommender.py
    ├── orchestrator.py
    └── permissions.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/life-canvas.git
cd life-canvas
```

Install dependencies:

```bash
pip install streamlit
```

## Run the Project

```bash
python3 -m streamlit run app.py
```

## Current Scope

This is a **prototype** built to demonstrate the core workflow idea in a short development timeline. It currently uses mock providers and JSON-based local data instead of live APIs.

## Future Enhancements

- Real provider APIs and service integrations
- Authentication for customers and providers
- Provider onboarding and profile verification
- Task prioritization with drag-and-drop canvas
- Ratings and reviews for providers
- Smart recommendations using AI/ML
- Real-time notifications between dependent services
- Better analytics and workflow insights

## Why This Matters

Life Canvas is not just another marketplace app. It is a **service orchestration platform** designed around customer control. It improves coordination, reduces repeated effort, and creates a consent-driven experience for multi-service tasks [web:629][web:631].

## Hackathon Vision

The goal of Life Canvas is to give customers a single platform to:
- Plan services
- Manage preferences
- Control collaboration
- Improve trust between users and service providers

This project explores how fragmented services can become a connected, customer-first ecosystem.

## Team

**Team - Achievers**  
**Aditya Dubey**

## License

This project is currently built for prototype and hackathon demonstration purposes.
