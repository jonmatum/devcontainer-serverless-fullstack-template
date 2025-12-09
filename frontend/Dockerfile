# Base Node.js image - pinned version
FROM node:20.18.3-slim

# Set working directory
WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm@9.15.4

# Only copy package.json + lockfile first (to leverage Docker cache)
COPY ./app/package.json ./app/pnpm-lock.yaml ./

# Install dependencies separately
RUN if [ -f package.json ]; then pnpm install --frozen-lockfile; fi

# Now copy the entire app source code
COPY ./app ./app

# Set working directory inside app
WORKDIR /app/app

# Make sure entrypoint script is copied and executable
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Security: Create non-root user
RUN useradd -m -u 1000 nodeuser && chown -R nodeuser:nodeuser /app
USER nodeuser

# Expose port for Vite dev server
EXPOSE 3000

# Start the frontend app
CMD ["/entrypoint.sh", "start"]
