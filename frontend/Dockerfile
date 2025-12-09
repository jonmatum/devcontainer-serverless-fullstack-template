# Base Node.js image - pinned version
FROM node:20.18.3-slim

# Set working directory
WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm@9.15.4

# Only copy package.json + lockfile first (to leverage Docker cache)
COPY ./app/package.json ./app/pnpm-lock.yaml ./

# Install dependencies separately
RUN if [ -f package.json ]; then pnpm install --no-frozen-lockfile; fi

# Now copy the entire app source code
COPY ./app ./app

# Set working directory inside app
WORKDIR /app/app

# Make sure entrypoint script is copied and executable
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Security: Create non-root user
RUN if ! id -u 1000 > /dev/null 2>&1; then useradd -m -u 1000 nodeuser; fi && \
    chown -R $(id -un 1000):$(id -gn 1000) /app
USER 1000

# Expose port for Vite dev server
EXPOSE 3000

# Start the frontend app
CMD ["/entrypoint.sh", "start"]
