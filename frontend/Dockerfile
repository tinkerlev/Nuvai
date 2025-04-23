# Base image with Node.js
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy only package.json and lock file to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the frontend for production
RUN npm run build

# Install serve to serve static content
RUN npm install -g serve

# Expose the default port for serve
EXPOSE 3000

# Start the app with serve
CMD ["serve", "-s", "dist"]
