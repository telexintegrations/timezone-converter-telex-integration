# Smart Timezone Converter API

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Endpoints](#endpoints)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction
The Smart Timezone Converter API is a FastAPI-based application designed to automatically detect time mentions in messages and convert them to the recipient's local timezone. This helps users avoid confusion when scheduling meetings, events, or deadlines across different time zones.

## Features
- **Automatic Time Detection**: Scans messages for explicit time mentions.
- **Timezone Conversion**: Converts detected times to the recipient's local timezone.
- **User-Friendly Interface**: Provides a JSON response with the converted time.
- **Customizable Settings**: Allows users to select their preferred timezone.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8+
- pip
- FastAPI
- Uvicorn (for running the server)
- Pytest (for running tests)
- Poetry (optional, for dependency management)

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/TryYourBestAndLeaveTheRest/smart-timezone-converter.git
    cd smart-timezone-converter
    ```
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, if you are using Poetry:
    ```bash
    poetry install
    ```
3. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add any necessary environment variables. For example:
    ```env
    IMAGE_PATH=img/logo.png
    ```

## Usage
1. **Run the Server**:
    ```bash
    uvicorn main:app --reload
    ```
    This will start the FastAPI server on `http://localhost:8000`.

2. **Access the API Documentation**:
    - Open `http://localhost:8000/docs` for Swagger UI.
    - Open `http://localhost:8000/redoc` for ReDoc.

## Endpoints

### GET /
**Description**: Check if the server is running.  
**Response**:
    ```json
    {
      "status": "running"
    }
    ```

### GET /app-logo
**Description**: Retrieve the application logo.  
**Response**: Returns the logo image.

### GET /integration-json
**Description**: Retrieve integration JSON data.  
**Response**:
    ```json
    {
      "data": {
         "date": {
            "created_at": "2025-02-20",
            "updated_at": "2025-02-20"
         },
         "descriptions": {
            "app_description": "This modifier automatically detects time mentions in messages and converts them to the recipient’s local time zone.",
            "app_logo": "http://localhost:8000/app-logo",
            "app_name": "Smart Timezone Converter",
            "app_url": "http://localhost:8000",
            "background_color": "#fff"
         },
         "integration_category": "Task Automation",
         "integration_type": "modifier",
         "is_active": false,
         "key_features": [
            "The integration scans messages for any explicit time mentions.",
            "The day (e.g., Sunday, Monday) is optional.",
            "The date sent must be specified ONLY in UTC.",
            "It modifies the message by appending the converted time in the recipient’s local time zone."
         ],
         "settings": [
            {
              "label": "Timezones",
              "type": "dropdown",
              "options": ["Africa/Lagos", ...],
              "description": "User will select their timezone with this",
              "required": true,
              "default": "Africa/Lagos"
            }
         ],
         "target_url": "http://localhost:8000/convert-time"
      }
    }
    ```

### POST /convert-time
**Description**: Convert time in a message to the user's local timezone.  
**Request Body**:
    ```json
    {
      "message": "Sunday February 23, 2025 10:34 AM UTC",
      "settings": [
         {
            "label": "Timezones",
            "type": "dropdown",
            "default": "Africa/Lagos",
            "required": true
         }
      ],
      "channel_id": "test_channel"
    }
    ```
**Response**:
    ```json
    {
      "message": "Sunday February 23, 2025 10:34 AM UTC (Sunday, February 23, 2025 11:34 AM WAT)"
    }
    ```

## Testing
To run the tests, use the following command:
    ```bash
    pytest test_api.py
    ```
Ensure you have pytest installed:
    ```bash
    pip install pytest
    ```

## Contributing
Contributions are welcome! Please follow these guidelines:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.