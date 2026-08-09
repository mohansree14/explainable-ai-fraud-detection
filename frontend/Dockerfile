# Use Node LTS as base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start the dev server, bound to all interfaces for Docker networking
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
