# Contributing to AMAN

Thank you for your interest in contributing to the Autonomous M&A Navigator (AMAN)! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed steps to reproduce the issue
- Provide system information (OS, Node.js version, etc.)
- Include relevant logs and error messages

### Suggesting Features
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Provide use cases and examples
- Consider the impact on existing functionality

### Code Contributions
1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes following our coding standards
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 🛠️ Development Setup

### Prerequisites
- Node.js 18+
- Python 3.8+
- Docker and Docker Compose
- Git

### Local Development
```bash
# Clone your fork
git clone https://github.com/your-username/aman.git
cd aman

# Start development environment
./docker/docker-helper.sh dev

# Or manual setup
cd backend && npm install && npm run dev
cd frontend && npm install && npm run dev
cd agents && pip install -r requirements.txt
```

## 📝 Coding Standards

### Frontend (TypeScript/React)
- Use TypeScript strict mode
- Follow ESLint configuration
- Use functional components with hooks
- Write comprehensive tests
- Use Material-UI components consistently

### Backend (Node.js)
- Use async/await for asynchronous operations
- Implement proper error handling
- Follow RESTful API conventions
- Write unit and integration tests
- Use proper logging levels

### Python Agents
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Use pytest for testing
- Handle exceptions gracefully

## 🧪 Testing Requirements

### Minimum Coverage
- Frontend: 70% code coverage
- Backend: 70% code coverage
- Python agents: 70% code coverage

### Running Tests
```bash
# Frontend
cd frontend && npm test

# Backend
cd backend && npm test

# Python agents
cd agents && python -m pytest
```

## 📋 Pull Request Process

1. **Branch Naming**: Use descriptive names
   - `feature/add-new-analysis`
   - `fix/dashboard-loading-issue`
   - `docs/update-api-documentation`

2. **Commit Messages**: Follow conventional commits
   ```
   feat: add financial ratio analysis
   fix: resolve dashboard loading issue
   docs: update API documentation
   test: add unit tests for ML engine
   ```

3. **Pull Request Template**
   - Describe the changes made
   - Reference related issues
   - Include screenshots for UI changes
   - List breaking changes if any

4. **Review Process**
   - All PRs require at least one review
   - Address reviewer feedback promptly
   - Ensure CI/CD checks pass
   - Maintain clean commit history

## 🏗️ Architecture Guidelines

### Frontend Architecture
- Use component composition over inheritance
- Implement proper state management
- Follow atomic design principles
- Ensure responsive design
- Optimize for performance

### Backend Architecture
- Follow MVC pattern
- Use middleware for cross-cutting concerns
- Implement proper validation
- Use database transactions appropriately
- Design for scalability

### Agent Architecture
- Keep agents focused and single-purpose
- Use dependency injection
- Implement proper logging
- Handle rate limiting
- Design for fault tolerance

## 🔒 Security Guidelines

- Never commit sensitive information
- Use environment variables for configuration
- Implement proper input validation
- Follow OWASP security guidelines
- Use secure communication protocols

## 📚 Documentation

- Update README.md for significant changes
- Document new API endpoints
- Include code comments for complex logic
- Update type definitions
- Provide usage examples

## 🚀 Release Process

1. **Version Bumping**: Follow semantic versioning
   - Major: Breaking changes
   - Minor: New features
   - Patch: Bug fixes

2. **Release Notes**: Include in each release
   - New features
   - Bug fixes
   - Breaking changes
   - Migration guides

## 🎯 Areas for Contribution

### High Priority
- Performance optimizations
- Additional financial metrics
- Enhanced AI capabilities
- Mobile responsiveness
- Accessibility improvements

### Medium Priority
- Additional data sources
- Advanced visualizations
- Export functionality
- User management
- Notification system

### Documentation
- API documentation
- User guides
- Developer tutorials
- Architecture diagrams
- Best practices

## 💬 Communication

- Use GitHub issues for bug reports and feature requests
- Use GitHub discussions for general questions
- Be respectful and constructive in all interactions
- Follow the code of conduct

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Annual contributor highlights

## 📞 Getting Help

- Check existing documentation
- Search closed issues
- Ask in GitHub discussions
- Contact maintainers for complex questions

Thank you for contributing to AMAN! 🚀