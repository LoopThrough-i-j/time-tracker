# Mercor Time Tracker

A comprehensive time tracking application with a FastAPI backend and Electron desktop frontend.

## Project Structure

```
mercor/
├── backend/                    # FastAPI Backend Application
│   ├── app/                   # Main application package
│   │   ├── constants/         # Response messages and constants
│   │   ├── dependencies/      # Authentication dependencies
│   │   ├── dto/              # Data Transfer Objects
│   │   │   ├── request/      # Request DTOs
│   │   │   │   └── v1/       # API v1 request models
│   │   │   └── response/     # Response DTOs
│   │   │       └── v1/       # API v1 response models
│   │   ├── routes/           # API routes
│   │   │   ├── ui/           # UI routes (HTML templates)
│   │   │   └── v1/           # API v1 routes
│   │   ├── static/           # Static files (DMG downloads)
│   │   ├── templates/        # Jinja2 HTML templates
│   │   └── utils/            # Utility functions
│   ├── constants/            # Global constants and exceptions
│   ├── database/             # Database layer
│   │   ├── constants/        # Database constants
│   │   └── mongodb/          # MongoDB implementation
│   │       ├── actions/      # Database operations
│   │       └── models/       # Database models
│   ├── services/             # Business logic layer
│   ├── tests/                # Test files
│   ├── tools/                # Development tools
│   ├── uploads/              # File uploads directory
│   ├── docker-compose.yaml   # Docker composition
│   ├── Dockerfile           # Docker image definition
│   ├── requirements.txt     # Python dependencies
│   └── main.py              # Application entry point
│
└── frontend/                  # Electron Desktop Application
    ├── src/                  # React source code
    │   ├── components/       # React components
    │   └── services/         # API service layer
    ├── public/               # Public assets and Electron main process
    ├── build/                # Production build output
    ├── dist/                 # Electron distribution files
    └── package.json          # Node.js dependencies and scripts
```

## Get Started Locally

### Building the Frontend Application [ Electron & React ]

1. Navigate to the frontend folder and copy the example environment file to create a `.env` file:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Build the macOS desktop application:
   ```bash
   npm run dist-mac
   ```

3. Move the generated DMG file to the backend's static folder:
   ```bash
   cp frontend/dist/Mercor\ Time\ Tracker-1.0.0-arm64.dmg backend/app/static/
   ```

### Starting the Backend with Docker Compose [ Python, FastAPI & MongoDB ]

1. Navigate to the backend folder

2. Start the backend services using Docker Compose:
   ```bash
   docker compose up --build -d
   ```

3. Access the application docs at `http://localhost:8080/docs`

### Testing

For now, there is a basic sanity test for the APIs written at `backend/tests/test_api_sanity.py`. You can run it directly for testing:

```bash
cd backend/tests
python3 test_api_sanity.py
```

This can be improved in the future with E2E tests using Robot Framework or Unit tests with Pytest


### Notes

**Implemented Features:**
- API request and response payloads are designed to be almost 1 to 1 compatible with Insightful, for seamless integration
- We have a route to generate signup link: `/api/v1/auth/get-signup-link`, didn't want to respond with this in the invite route to make sure we keep compatibility with insightful
- One cannot start more than one task at a time from API calls and cannot start a new one, until the old is stopped
- We do a heartbeat to update the values of a time log to ensure if someone closes the app suddenly or it gets crashed we still have the last active timestamp
- An employee can only update or end the latest time log


**Areas for Improvement:**
- Database calls in an API can be optimized using batches
- Ideally data verification should be in the routes layer, but not much verification is done there other than the types by pydantic, rest is directly done from the service layer
- Now it is a simple monolith which might face potential scaling problems with a lot of people online and working at the same time. It can be mitigated with async and aggregated processing

**Not Implemented:**
- We are not sending emails on signup yet
- Consistency of the task status with the project status list and some similar fields are not considered much, as I didn't give a deep thought on how the behavior should be like
- Screenshots are not implemented but can be passed from the heartbeat, can take it up in an iteration if required
