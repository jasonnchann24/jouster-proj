# Use official Node.js image as base
FROM node:22.12-alpine

# Set working directory
WORKDIR /app

# Copy the rest of the app
COPY client/ .

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY client/package*.json ./

# Expose default React dev server port
EXPOSE 3000

# Run npm install at container startup, then start dev server
CMD ["sh", "-c", "npm install && npm run dev"]