# Use Alpine as the base image
FROM alpine:latest

# Install Wine and necessary dependencies
RUN apk add --no-cache wine xvfb

# Set working directory
WORKDIR /app

# Copy your EXE file into the container
COPY dist/Main.exe /app/dist/Main.exe

# Run the EXE using Wine in headless mode
CMD ["wine", "dist/Main.exe"]