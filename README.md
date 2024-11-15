# Website Visitor Classifier

## Overview

This is a web application that generates survey style questions which aim to classify the intent behind a user's visit to a website. It utilizes a React frontend for user interaction and a Flask backend for processing requests, including web scraping and calling a Large Language Model (LLM) API to generate questions related to the URL's content.

## Features

- **React Frontend**: 
  - Displays an input box for the user to enter a URL.
  - Sends the entered URL to the Flask backend via an HTTP request.
  - Displays the generated questions to the user.

- **Flask Backend**:
  - Receives the URL from the React frontend.
  - Scrapes the website corresponding to the provided URL.
  - Calls an LLM API to generate questions that classify the user's intent based on the scraped data.
  - Utilizes Redis to cache responses
  - Returns the generated questions to the React frontend.

## How It Works

1. User enters a URL in the React application's input box.
2. React sends an HTTP request containing the URL to the Flask backend.
3. The Flask backend:
   - Scrapes the content of the provided website.
   - Sends a prompt embedded with the scraped data to an LLM API.
   - Processes the LLM's response to generate user-facing questions.
4. The backend returns the questions to the React frontend.
5. The React application displays the questions for the user.

## Technologies Used

- **Frontend**: React.js
- **Backend**: Flask
- **Web Scraping**: `BeautifulSoup`
- **LLM API**: NVIDIA NIM API using Llamma 70b

## Setup and Installation

### Prerequisites
- Node.js (for the React frontend)
- Python 3.9+ (for the Flask backend)
- An API key for the LLM API service

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd intent-classifier-app
2. Set up the backend:
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
3. Set up the frontend:
    ```bash
    cd frontend
    npm install
    npm start
4. Open your browser and navigate to http://localhost:3000