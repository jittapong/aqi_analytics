# Use an official Node.js runtime as a parent image (Node 20)
FROM node:20-alpine

# Install pnpm
RUN npm install -g pnpm

# Set working directory inside the container
WORKDIR /app

# Copy package.json and pnpm-lock.yaml from the current directory (ui folder)
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --production

# Copy the rest of the project files from the current directory (ui folder)
COPY . .

# Build Next.js app
RUN pnpm run build

# Expose the port Next.js runs on
EXPOSE 3000

# Start Next.js
CMD ["pnpm", "start"]
