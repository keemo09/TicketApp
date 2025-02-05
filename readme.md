# Sweepstake System

## Overview
This project is a sweepstake system that offers users a unique opportunity to promote their products and gain email subscribers for further marketing campaigns. Additionally, it allows both registered and unregistered users to purchase tickets and participate in sweepstakes.

## Features
- **Campaign Management:**
  - Users can create new campaigns.
  - Define ticket quantity and pricing.
  - Set campaign behavior, including prize claim rules and campaign duration.
  - Manually end campaigns if needed.
  
- **User Management:**
  - Registered users can create and participate in campaigns.
  - User authentication using JWT tokens.
  - Users can update or delete their accounts.
  
- **Prize and Ticket System:**
  - Assign prizes to campaigns.
  - Generate and distribute tickets.
  - Match ticket IDs with prize database upon redemption.
  - Notify users of their winnings based on campaign settings.

## Tech Stack
- **Backend:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Authentication:** OAuth2 with JWT
- **Containerization:** Docker (optional)

## Installation
### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual Environment (recommended)

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/sweepstake-system.git
   cd sweepstake-system

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
    pip install -r requirements.txt

4. Run the FastAPI server:
    uvicorn main:app --reload

## API Endpoints
### Authentication
POST   /register   # Register a new user
POST   /login      # Log in and obtain a JWT token

### Campaigns
POST   /campaigns/                 # Create a new campaign
GET    /campaigns/                 # Get all campaigns for the current user
GET    /campaigns/{campaign_id}    # Get details of a specific campaign
PUT    /campaigns/{campaign_id}    # Update an existing campaign
DELETE /campaigns/{campaign_id}    # Delete a campaign
GET    /campaigns/{campaign_id}/ticket  # Generate a ticket for a campaign

### users
POST   /register   # Register a new user
POST   /login      # Log in and obtain a JWT token
POST   /           # Update user details
DELETE /           # Delete user account
GET    /tickets    # Retrieve all tickets for the current user