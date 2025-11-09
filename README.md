# Hello World Advanced

A sophisticated Python greeting application demonstrating advanced software development practices including logging, configuration management, testing, and modular architecture.

## 🌟 Features

- **Multiple Greeting Modes**:
  - Standard greetings with customizable names
  - Multi-language support (English, Spanish, French, German, Italian)
  - Time-based greetings (morning, afternoon, evening, night)
  - Custom message processing

- **Advanced Logging**:
  - Structured logging with YAML configuration
  - Multiple log levels and destinations
  - Separate error logging
  - Debug and production modes

- **Configuration Management**:
  - YAML-based configuration
  - Hot-reload capabilities
  - Environment-specific settings
  - Nested configuration access

- **Comprehensive Testing**:
  - Unit tests with pytest
  - Integration tests
  - Mock-based testing
  - Test coverage reporting

- **Statistics & Analytics**:
  - Usage tracking
  - Session duration monitoring
  - Language usage statistics

## 🚀 Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd simple_hello_world
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test files:
```bash
pytest tests/test_config_manager.py
pytest tests/test_greeting_manager.py
pytest tests/test_integration.py
```

## 📁 Project Structure

```
simple_hello_world/
├── src/                          # Source code
│   ├── __init__.py
│   ├── config_manager.py         # Configuration management
│   └── greeting_manager.py       # Greeting logic and statistics
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_config_manager.py    # Config manager tests
│   ├── test_greeting_manager.py  # Greeting manager tests
│   └── test_integration.py       # Integration tests
├── config/                       # Configuration files
│   ├── logging.yaml              # Logging configuration
│   └── settings.yaml             # Application settings
├── logs/                         # Log file directory
├── .github/                      # GitHub configuration
│   └── copilot-instructions.md   # AI coding assistance
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🔧 Configuration

### Application Settings (`config/settings.yaml`)

- **App Configuration**: Name, version, debug mode
- **Greeting Settings**: Default names, language templates, time-based greetings
- **Output Settings**: Color support, file output options

### Logging Configuration (`config/logging.yaml`)

- **Multiple Handlers**: Console, file, and error-specific logging
- **Flexible Formatting**: Standard and detailed formatters
- **Log Levels**: Configurable per handler and logger

## 🎯 Usage Examples

### Interactive Mode
```bash
python main.py
```

### Programmatic Usage
```python
from src.config_manager import ConfigManager
from src.greeting_manager import GreetingManager

# Initialize
config = ConfigManager("config/settings.yaml")
greetings = GreetingManager(config)

# Generate greetings
standard = greetings.get_standard_greeting("Alice")
spanish = greetings.get_multilang_greeting("Carlos", "es")
time_based = greetings.get_time_based_greeting("Bob")

# Get statistics
stats = greetings.get_statistics()
```

## 🧪 Development

### Adding New Languages

1. Edit `config/settings.yaml`
2. Add language template to `greetings.languages`
3. Test with existing test suite

### Adding New Greeting Modes

1. Implement method in `GreetingManager`
2. Add configuration options if needed
3. Write corresponding tests
4. Update main.py menu system

### Logging

The application uses structured logging with multiple levels:
- **DEBUG**: Detailed information for development
- **INFO**: General application flow
- **WARNING**: Potentially harmful situations
- **ERROR**: Error events that might allow application to continue

## 📊 Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Mock Testing**: Test external dependencies
- **Coverage Reporting**: Ensure comprehensive test coverage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏗️ Architecture Notes

- **Separation of Concerns**: Configuration, business logic, and presentation are separated
- **Dependency Injection**: Components receive their dependencies explicitly
- **Error Handling**: Comprehensive error handling with appropriate logging
- **Extensibility**: Easy to add new greeting modes and languages
- **Testability**: All components are designed to be easily testable