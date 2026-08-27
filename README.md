# Cybernet NBB AI Voice Operator

**Made by Ghayoor Hafeez**

A real-time AI voice operator for the authorized Cybernet NBB portal at https://partner.nationalbroadband.pk/

## Core Architecture

```
VOICE COMMAND
    ↓
GEMINI LIVE API
    ↓
Real-Time Speech + Conversation
    ↓
AI Understands Intent & Context
    ↓
PLANNER Creates Structured Steps
    ↓
TOOL Selection & Validation
    ↓
PERMISSION / CONFIRMATION CHECK
    ↓
PLAYWRIGHT Browser Execution
    ↓
Authenticated Cybernet NBB Portal
    ↓
Portal Result Verification
    ↓
Structured Result
    ↓
GEMINI Generates Natural Response
    ↓
LIVE VOICE RESPONSE
```

## Phase 1: Foundation & Dashboard

Phase 1 includes:
- PySide6 desktop dashboard
- Plugin system with auto-discovery
- SQLite persistent memory
- Tool registry & permission system
- Mock Cybernet portal
- Comprehensive logging
- Full test suite

## Installation

```bash
git clone https://github.com/ghayoorhafeez/cybernet-agent.git
cd cybernet-agent
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
python main.py
```

## Development Phases

- **Phase 1** ✓: Dashboard, Plugins, Memory, Tools, Permissions, Mock Portal
- **Phase 2**: Gemini Live API, Microphone, Voice
- **Phase 3**: Playwright, Browser Automation
- **Phase 4**: Customer Search, Status, Package Info
- **Phase 5**: Package Activation, Renewal, Verification
- **Phase 6**: Weather, News, Reminders, Clipboard
- **Phase 7**: Vision, Advanced Features

## Security

- No hardcoded credentials
- Environment variables only
- Permission system for write operations
- Result verification
- Audit logging

## License

MIT License - Made by Ghayoor Hafeez
