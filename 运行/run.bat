@echo off
echo Starting Anschreiben Generator...
echo.
echo Make sure Docker Desktop is running!
echo.
echo Setting up environment...
if not exist ../.env (
    copy ../.env.example ../.env
    echo Please edit .env file with your API keys before running again!
    pause
    exit /b 1
)

echo Starting the application with existing image...
echo (To rebuild, run: docker-compose up --build)
cd ../deployment && docker-compose up

pause