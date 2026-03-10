#!/bin/bash
echo "Starting Anschreiben Generator..."
echo

echo "Make sure Docker is running!"
echo

echo "Setting up environment..."
if [ ! -f ../.env ]; then
    cp ../.env.example ../.env
    echo "Please edit .env file with your API keys before running again!"
    exit 1
fi

echo "Building and starting the application..."
cd ../deployment && docker-compose up --build