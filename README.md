Study Assistant Backend
This repository contains the backend for the AI-powered Study Assistant, a web application designed to help users learn by summarizing text, generating quizzes, and creating flashcards from their study materials.

Table of Contents
Features

Technology Stack

Getting Started

Prerequisites

Installation

Configuration

Running the Application

API Endpoints

Database Schema

AI Integration

Contributing

License

Features
User Authentication: Secure user registration and login.

Document Management:

Allow users to upload or paste text content.

Store and retrieve user-specific study documents.

AI-Powered Content Generation:

Text Summarization: Generate concise summaries of uploaded documents.

Quiz Generation: Create multiple-choice and open-ended questions based on document content.

Flashcard Generation: Extract key terms and definitions to create digital flashcards.

Quiz & Flashcard Storage: Persist generated quizzes and flashcards for later review.

Quiz Attempt Tracking: Record user performance on quizzes.

Technology Stack
Language: Python 3.9+

Web Framework: FastAPI (recommended for its performance and modern features)

Database: PostgreSQL

ORM (Object-Relational Mapper): SQLAlchemy

Database Migrations: Alembic (with SQLAlchemy)

AI Libraries/APIs:

Hugging Face Transformers: For local execution of models like T5, BART (summarization, potentially QG).

OpenAI API: For powerful language models (e.g., GPT-3.5, GPT-4) for summarization, sophisticated question generation, and flashcard extraction.

Environment Management: pipenv or venv

Asynchronous Tasks: Celery (optional, for long-running AI tasks)

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.9+: Download Python

pip (Python Package Installer): Comes with Python.

PostgreSQL:

Download PostgreSQL

Recommended (Docker): Docker Desktop (for easily running PostgreSQL in a container)

Installation
Clone the repository:

Bash

git clone https://github.com/ShaniWolfson/study-assistant-backend.git
cd study-assistant-backend
Create and activate a virtual environment:

Using pipenv (recommended):

Bash

pip install pipenv
pipenv install
pipenv shell
Using venv:

Bash

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt # (You'll create this file later)
