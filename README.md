# DevContainer Developer Workspace Template

A modern, opinionated, and extensible Dev Container template built for cloud, full-stack, DevOps, and infrastructure developers. Easily reproducible, portable, and ready for work in seconds.

## Key Features

### Intelligent Project Initialization
- **One-command setup** with `make init` - automatically configures your entire development environment
- **Dynamic port management** - automatically finds and assigns available ports to prevent conflicts
- **Smart dependency detection** - verifies prerequisites and sets up components intelligently
- **Cross-platform compatibility** - works seamlessly on macOS, Linux, and Windows

### Development Stack
- **Shell Environment**: Zsh, Oh My Zsh, Powerlevel10k with syntax highlighting and autosuggestions
- **Cloud Tools**: AWS CLI v2, Terraform + tfswitch, OpenTofu
- **Languages**: Node.js 20.11.1, Python 3.11.9 with pipenv support
- **Quality Tools**: Pre-commit hooks with optional global configuration
- **Customizable Features**: Toggle each feature as needed with flags

### Installed Tools
`terraform`, `aws`, `node`, `npm`, `python`, `pip`, `pipenv`, `tofu`, `pre-commit`, `zsh`

### VS Code Extensions
Curated, enterprise-grade extensions included:

- **Cloud & Infrastructure**: `hashicorp.terraform`, `amazonwebservices.aws-toolkit-vscode`, `redhat.vscode-yaml`
- **Python Development**: `ms-python.*`, `ms-toolsai.jupyter`
- **Web Development**: `dbaeumer.vscode-eslint`, `esbenp.prettier-vscode`, `bradlc.vscode-tailwindcss`
- **Shell & DevOps**: `timonwong.shellcheck`, `foxundermoon.shell-format`
- **Containers**: `ms-azuretools.vscode-docker`
- **Collaboration**: `eamodio.gitlens`, `ms-vsliveshare.vsliveshare`, `github.vscode-github-actions`
- **Documentation**: `bierner.markdown-mermaid`, `streetsidesoftware.code-spell-checker`
- **Remote Development**: `ms-vscode-remote.*`
- **Productivity**: `visualstudioexptteam.vscodeintellicode`, `naumovs.color-highlight`

## Quick Start

### Method 1: Complete Setup (Recommended)

1. **Clone this template:**
   ```bash
   gh repo create my-devcontainer --template jonmatum/devcontainer-developer-workspace-fullstack-poc
   cd my-devcontainer
   ```

2. **Initialize the project (IMPORTANT):**
   ```bash
   make init
   ```
   
   This single command will:
   - Check system prerequisites
   - Scan and assign available ports automatically
   - Configure DevContainer settings
   - Set up frontend application with Vite + React
   - Verify all components are properly configured

3. **Start the development environment:**
   ```bash
   make up
   ```

4. **Open in VS Code:**
   - Use `Dev Containers: Reopen in Container` from the Command Palette
   - Your development environment is ready!

### Method 2: Manual DevContainer Setup

1. Clone the template
2. Open in Visual Studio Code
3. Use `Dev Containers: Reopen in Container` from the Command Palette
4. Run `make init` inside the container to complete setup

## Why `make init` is Essential

### The Problem It Solves

Without proper initialization, you might encounter:
- **Port conflicts** when multiple projects try to use the same ports (3000, 8000, etc.)
- **Configuration mismatches** between DevContainer settings and actual services
- **Missing dependencies** that cause services to fail silently
- **Manual setup overhead** requiring multiple commands and configuration steps

### What `make init` Does

```bash
>> Starting Complete Project Initialization

[INFO]     Checking system prerequisites...
[SUCCESS]  Prerequisites check completed

[INFO]     Scanning for available ports...
[SUCCESS]  Assigned ports: Frontend(3000) Backend(3001) Admin(3002) DynamoDB(3003)

[INFO]     Rendering devcontainer configuration...
[SUCCESS]  DevContainer configuration rendered

[INFO]     Setting up frontend application...
[SUCCESS]  Frontend application configured

[INFO]     Verifying frontend setup...
[SUCCESS]  Frontend verification passed

[SUCCESS]  Project initialization completed successfully!
```

### Dynamic Port Assignment

The system intelligently manages ports to prevent conflicts:

- **Automatic Detection**: Scans your system for available ports starting from 3000
- **Conflict Resolution**: If port 3000 is busy, automatically assigns 3001, 3002, etc.
- **Service Mapping**: 
  - Frontend (React/Vite): First available port
  - Backend (FastAPI): Second available port  
  - DynamoDB Admin: Third available port
  - DynamoDB Local: Fourth available port
- **DevContainer Sync**: Automatically updates `.devcontainer/devcontainer.json` with assigned ports
- **Environment Variables**: Creates `.env` file with port assignments for consistent usage

### Port Assignment Example

```bash
# If ports 3000-3002 are busy, the system might assign:
FRONTEND_PORT=3003   # React development server
BACKEND_PORT=3004    # FastAPI server  
ADMIN_PORT=3005      # DynamoDB Admin interface
DYNAMODB_PORT=3006   # DynamoDB Local database
```

### Benefits of Dynamic Port Management

1. **Zero Configuration Conflicts**: Never worry about port collisions with other projects
2. **Team Consistency**: Every developer gets the same relative port assignments
3. **CI/CD Friendly**: Works in any environment without manual port configuration
4. **Multi-Project Support**: Run multiple instances of this template simultaneously
5. **Automatic Documentation**: Port assignments are clearly displayed and saved

## Available Commands

Run `make help` to see all available commands with detailed descriptions:

```bash
make help      # Show comprehensive help with command categories
make status    # Display current project status and port assignments
make init      # Complete project initialization (recommended first step)
make up        # Start all containers
make down      # Stop all containers
make logs      # Follow container logs
make clean     # Clean up Docker resources
```

### Command Categories

- **Initialization & Setup**: Project initialization and configuration
- **Component Setup**: Individual component management  
- **Container Management**: Docker and container orchestration
- **DevContainer Operations**: DevContainer CLI integration
- **Maintenance & Cleanup**: System cleanup and maintenance
- **Utilities & Diagnostics**: Debugging and validation tools

### Project Status Monitoring

Use `make status` to get a comprehensive overview of your project:

```bash
>> Project Status Report

Port Configuration
  Frontend:    3000
  Backend:     3001
  Admin:       3002
  DynamoDB:    3003

Configuration Status
  DevContainer: Configured
  Environment:  Configured

Component Status
  Frontend:    Initialized
  Backend:     Available
```

## Services Overview

This template includes the following services:

- **DevContainer**: Main development environment with all tools
- **Frontend**: React application with Vite (port 3000 by default)
- **Backend**: FastAPI Python application (port 3001 by default)
- **DynamoDB Local**: Local DynamoDB instance for development (port 3003 by default)
- **DynamoDB Admin**: Web interface for DynamoDB management (port 3002 by default)

## Advanced Usage

### Custom Port Range
You can specify a custom starting port:
```bash
PORT_START=4000 make init
```

### Quick Setup (Ports Only)
For faster setup when you only need port configuration:
```bash
make init-quick
```

### Port Conflict Resolution
If you encounter port conflicts after initialization:
```bash
make find-ports  # Reassign to new available ports
make check-ports # Check current port availability
```

### Configuration Validation
Verify your setup is correct:
```bash
make validate-config
```

### Component Management
Initialize or reset individual components:
```bash
make init-frontend   # Set up React frontend
make init-backend    # Set up FastAPI backend
make reset-frontend  # Reset frontend (removes app directory)
make reset-backend   # Reset backend (removes Pipfile)
```

## Troubleshooting

### Common Issues

**Port conflicts during startup:**
```bash
make check-ports  # Check which ports are in use
make find-ports   # Reassign to available ports
make up           # Restart with new ports
```

**DevContainer configuration issues:**
```bash
make validate-config  # Verify all configurations
make init            # Reinitialize if needed
```

**Service not accessible:**
```bash
make status  # Check service status and port assignments
make logs    # View container logs for errors
```

## Customization

You can modify `devcontainer.json` to:

- Enable/disable features
- Change tool versions
- Add your own custom VS Code extensions
- Modify container configurations

The Makefile system will automatically adapt to your changes while maintaining port management and initialization capabilities.

## License

This project is licensed under the [MIT License](LICENSE).

---

> echo 'Pura Vida & Happy Coding!';
