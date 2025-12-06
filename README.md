# Meme Generator - Dockerized Application

A Flask-based web application for generating memes, fully containerized with Docker.

## Features
- Upload any image
- Add top and bottom text (classic meme format)
- Real-time meme generation
- Download generated memes
- Fully Dockerized deployment

## Technology Stack
- **Backend**: Python Flask
- **Image Processing**: Pillow (PIL)
- **Containerization**: Docker & Docker Compose
- **Frontend**: HTML5, CSS3

## Installation & Setup

### Prerequisites
- Docker & Docker Compose installed
- Git

### Quick Start with Docker Compose
```bash
# Clone the repository
git clone <your-repo-url>
cd meme-generator

# Build and run with Docker Compose
docker-compose up --build