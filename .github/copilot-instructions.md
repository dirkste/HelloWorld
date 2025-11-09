# Copilot Instructions

This is an advanced Python Hello World application demonstrating enterprise-grade development practices with logging, configuration management, testing, and modular architecture.

## Project Architecture

- **Modular Design**: Core logic separated into `src/` modules (`config_manager.py`, `greeting_manager.py`)
- **Configuration-Driven**: YAML-based settings in `config/` with hot-reload capabilities  
- **Comprehensive Logging**: Structured logging with multiple handlers (console, file, error-specific)
- **Test Coverage**: Unit tests, integration tests, and mocking with pytest
- **Interactive CLI**: Menu-driven interface in `main.py` with error handling

## Key Files & Patterns

### Core Modules (`src/`)
- `config_manager.py` - YAML configuration loading with dot-notation access (`config.get('app.name')`)
- `greeting_manager.py` - Business logic with statistics tracking and multiple greeting modes
- Both use dependency injection and structured logging

### Configuration (`config/`)
- `settings.yaml` - Application settings with nested structure (app, greetings, output)
- `logging.yaml` - Logging configuration with multiple formatters and handlers
- Settings accessed via dot notation: `self.config.get('greetings.default_name')`

### Testing Strategy (`tests/`)
- Unit tests with mocking: `Mock(spec=ConfigManager)` for isolated testing
- Integration tests with real YAML config files using `tempfile`
- Time-based testing using `@patch('src.greeting_manager.datetime')`

## Development Workflows

### Running the Application
```bash
python main.py  # Interactive menu-driven interface
```

### Testing
```bash
pytest                           # Run all tests
pytest --cov=src --cov-report=html  # With coverage
pytest tests/test_config_manager.py  # Specific module
```

### Dependencies
```bash
pip install -r requirements.txt  # PyYAML, pytest, pytest-cov, pytest-mock
```

## Code Conventions

### Error Handling Pattern
- Try-catch blocks with structured logging: `logger.error(f"Error: {str(e)}", exc_info=True)`
- User-friendly error messages with emoji: `print("❌ Error generating greeting")`
- Graceful degradation (fallback to basic logging if config fails)

### Logging Pattern
- Get logger per module: `logger = logging.getLogger('hello_world.module')`
- Log user actions: `logger.info(f"Generated {lang} greeting for: {name}")`
- Debug mode for detailed info: `logger.debug(f"User selected option: {choice}")`

### Configuration Access
- Dot notation with defaults: `self.config.get('greetings.default_name', 'World')`
- Type hints for configuration methods: `-> Dict[str, Any]`
- Reload capability: `config_manager.reload_config()`

### Testing Patterns
- Mock external dependencies: `self.mock_config = Mock(spec=ConfigManager)`
- Use temporary files for integration tests with real YAML
- Patch datetime for time-dependent tests: `@patch('src.greeting_manager.datetime')`
- Assert both return values and side effects (statistics updates)

## Adding New Features

### New Greeting Mode
1. Add method to `GreetingManager` with statistics tracking (`self._update_stats()`)
2. Add configuration section to `config/settings.yaml`
3. Add menu option in `main.py` with error handling
4. Write unit and integration tests

### New Configuration
1. Add to `config/settings.yaml` with nested structure
2. Access via `ConfigManager.get()` with dot notation
3. Add validation in relevant module
4. Test configuration reload behavior

### New Language
1. Add template to `config/settings.yaml` under `greetings.languages`
2. Test via existing `get_multilang_greeting()` method
3. Verify language usage statistics tracking

## Project Structure Context

```
├── src/                    # Business logic modules
├── tests/                  # Comprehensive test suite  
├── config/                 # YAML configuration files
├── logs/                   # Runtime log files (created automatically)
├── main.py                 # CLI entry point with interactive menu
└── requirements.txt        # Dependencies: PyYAML, pytest, testing tools
```

This project emphasizes separation of concerns, testability, and enterprise development practices suitable for larger applications.