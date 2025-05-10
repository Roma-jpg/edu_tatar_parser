# BrainBox Diary Backend Service

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Backend service for my BrainBox Diary Android app that fetches and parses school schedule data from edu.tatar.ru educational portal. Outdated now, since Russian schools switched to ms-edu.tatar.ru.

## 📖 Project Overview

This Flask-based service provides:
- REST API endpoint for fetching student diary data
- Web scraping integration with edu.tatar.ru
- Telegram bot integration for access monitoring

## ✨ Key Features

- **Educational Portal Integration**
  - Secure credential validation
  - Dynamic schedule generation by date
  - Web scraping of diary entries and marks

- **API Services**
  - JSON responses for Android app
  - Error handling for invalid dates/credentials
  - Request logging system

- **Monitoring**
  - Real-time Telegram notifications
  - Access logging (IP/user-agent tracking)
  - Credential attempt recording

## 🛠️ How It Works

### Data Flow
1. Android app sends POST request with credentials and date
2. Service authenticates with edu.tatar.ru portal
3. Scrapes schedule data for specified week
4. Parses and structures data into JSON format
5. Returns standardized response to Android app

### Core Components
- **Web Scraper**: Uses BeautifulSoup to extract:
  - Student information
  - Class schedule
  - Homework assignments
  - Academic marks

- **Authentication System**:
  - Maintains session cookies
  - Handles portal security headers
  - Manages user agent rotation

- **Date Handling**:
  - Converts dates to portal-specific timestamps
  - Handles month boundary transitions
  - Supports historical data queries

## 🌐 API Endpoints

### `GET /`
- Serves static portfolio website
- Responsive HTML/CSS/JavaScript content

### `POST /`
**Request Format:**
```json
{
  "login": "portal_username",
  "password": "portal_password", 
  "date": "DD-MM-YYYY"
}
```

**Error Responses:**

- `400 Bad Request`: Missing credentials  
  ```json
  {"error": "Login and password are required."}
  ```
- `440 Date Error`: Invalid date format
    ```json
    {"error": "Invalid date format. Please use DD-MM-YYYY."}
    ```
- `401 Unauthorized`: Invalid login credentials
    ```json
    {"error": "Login or password is incorrect"}
    ```
- `500 Server Error`: Unexpected parsing failures
    ```json
    {"error": "Failed to process diary data"}
    ```

## 📊 Example Usage

**cURL request:**
```bash
curl -X POST http://yourserver.com/ \
  -H "Content-Type: application/json" \
  -d '{"login":"school_login","password":"school_password","date":"15-05-2023"}'
```

**Python example**
```python
import requests

response = requests.post(
    "http://yourserver.com/",
    json={
        "login": "school_login",
        "password": "school_password",
        "date": "15-05-2023"
    }
)
print(response.json())
```

\
\
_This project was developed for educational purposes. Use responsibly._





