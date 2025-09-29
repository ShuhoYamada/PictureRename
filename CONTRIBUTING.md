# Contributing to Image Renamer Pro 🎨

Thank you for your interest in contributing to Image Renamer Pro! We welcome contributions from everyone.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/PictureRename.git
   cd PictureRename
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- macOS (for full compatibility testing)
- Git

### Running the Application
```bash
python main.py
```

## 📝 Making Changes

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following these guidelines:
   - Follow PEP 8 style guidelines
   - Add docstrings to new functions and classes
   - Keep functions focused and small
   - Use meaningful variable and function names

3. **Test your changes**:
   - Run the application and test all functionality
   - Test with different image formats (JPG, PNG, HEIC)
   - Test Excel file loading with sample data

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "✨ Add: Your descriptive commit message"
   ```

## 🎯 Code Style

- Use **4 spaces** for indentation
- Maximum line length of **88 characters**
- Use **type hints** where possible
- Follow **PEP 8** naming conventions

### Commit Message Format
Use emoji prefixes for commit messages:
- `✨ Add:` for new features
- `🐛 Fix:` for bug fixes
- `🎨 Style:` for formatting changes
- `📚 Docs:` for documentation
- `🧪 Test:` for adding tests
- `♻️ Refactor:` for code refactoring

## 🐛 Reporting Bugs

Please use the GitHub issue tracker to report bugs. Include:
- Your operating system and version
- Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Any error messages or logs

## 💡 Suggesting Features

We welcome feature suggestions! Please:
- Check if the feature has already been requested
- Describe the use case and benefit
- Consider backward compatibility
- Provide mockups or examples if applicable

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add or update tests** for new functionality
3. **Ensure all tests pass**
4. **Update the README.md** if necessary
5. **Submit your pull request** with a clear description

### Pull Request Guidelines
- Keep PRs focused on a single feature or fix
- Write a clear title and description
- Reference any related issues
- Include screenshots for UI changes

## 🏗️ Project Structure

```
ImageRenamer/
├── main.py              # Application entry point
├── gui/                 # GUI modules
│   ├── main_window.py   # Main application window
│   ├── input_panel.py   # Input form components
│   └── image_viewer.py  # Image display components
├── utils/               # Utility modules
│   ├── excel_reader.py  # Excel file processing
│   ├── file_handler.py  # File operations
│   └── image_processor.py # Image processing
└── requirements.txt     # Python dependencies
```

## 🎨 UI/UX Guidelines

- Maintain the modern, card-based design aesthetic
- Use the established color scheme
- Ensure accessibility and good contrast
- Test on different screen sizes
- Keep interactions intuitive and responsive

## 📄 License

By contributing to Image Renamer Pro, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Help other contributors
- Ask questions if you're unsure
- Share knowledge and best practices

Thank you for contributing to Image Renamer Pro! 🙏