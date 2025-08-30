# 🚀 AMAN - Autonomous M&A Navigator


> **Autonomous M&A Navigator** - An AI-powered platform for comprehensive mergers and acquisitions due diligence, featuring advanced financial analysis, risk assessment, and intelligent automation.

## 🌟 Overview

AMAN is a cutting-edge platform that revolutionizes the M&A due diligence process through AI-powered automation. It combines machine learning, natural language processing, and real-time data analysis to provide comprehensive insights for investment decisions.

### 🎯 Key Features

- **🤖 AI-Powered Financial Analysis** - ML-driven financial ratio calculations, anomaly detection, and 3-year forecasting
- **📊 Interactive Dashboard** - Beautiful Material-UI interface with real-time analytics and visualizations
- **🔍 Multi-Agent Intelligence** - Specialized AI agents for finance, legal, operations, reputation, and compliance
- **⚡ Real-Time Processing** - Live data integration with major financial APIs and news sources
- **🛡️ Risk Assessment** - Advanced risk scoring and geopolitical analysis
- **📈 Predictive Analytics** - Timeline predictions and synergy discovery
- **🔒 Compliance Monitoring** - Automated SOX compliance and audit trail generation
- **🌐 Global Intelligence** - Sanctions screening, supply chain mapping, and market intelligence

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Agents       │
│   (Next.js)     │◄──►│   (Node.js)     │◄──►│   (Python)      │
│   Port: 3000    │    │   Port: 3001    │    │   AI/ML Engine  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
         │   PostgreSQL    │    │     Redis       │    │   Superset      │
         │   Port: 5432    │    │   Port: 6379    │    │   Port: 8088    │
         └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+ with pip
- **Docker** and Docker Compose
- **Git** for version control

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/aman.git
   cd aman
   ```

2. **Start development environment**
   ```bash
   # Unix/Linux/macOS
   ./docker/docker-helper.sh dev
   
   # Windows
   docker\docker-helper.bat dev
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001
   - Analytics: http://localhost:8088

### 🔧 Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Backend Setup
```bash
cd backend
npm install
cp .env.example .env
# Configure your environment variables
npm run dev
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Agents Setup
```bash
cd agents
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure your API keys
```

#### Database Setup
```bash
cd backend
npm run db:init
```

</details>

## 📁 Project Structure

```
aman/
├── 🎨 frontend/          # Next.js 15 + Material-UI dashboard
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utilities and configurations
│   │   ├── types/        # TypeScript type definitions
│   │   └── utils/        # Helper functions
│   ├── jest.config.js    # Testing configuration
│   └── package.json
│
├── 🔧 backend/           # Node.js + Express API server
│   ├── api/              # API routes and controllers
│   ├── database/         # Database schemas and migrations
│   ├── models/           # Data models
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions
│   └── server.js         # Main server file
│
├── 🤖 agents/            # Python AI/ML agents
│   ├── finance/          # Financial analysis agents
│   ├── legal/            # Legal compliance agents
│   ├── operations/       # Operational risk agents
│   ├── reputation/       # Reputation analysis agents
│   ├── synergy/          # Synergy discovery agents
│   ├── monitoring/       # System monitoring agents
│   └── audit/            # Compliance audit agents
│
├── 🐳 docker/            # Docker configurations
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
│
├── 📊 database/          # Database scripts and schemas
├── 📚 docs/              # Documentation
├── 🧪 tests/             # Integration tests
└── 📋 scripts/           # Utility scripts
```

## 🔑 Key Components

### 🎨 Frontend Dashboard
- **Technology**: Next.js 15, React 19, Material-UI, TypeScript
- **Features**: Interactive charts, real-time updates, responsive design
- **Testing**: Jest + React Testing Library
- **Styling**: Material-UI + Emotion

### 🔧 Backend API
- **Technology**: Node.js, Express, PostgreSQL, Redis
- **Features**: RESTful APIs, real-time processing, task queues
- **Security**: Helmet, CORS, rate limiting, input validation
- **Monitoring**: Comprehensive logging and health checks

### 🤖 AI Agents
- **Technology**: Python, scikit-learn, pandas, NumPy
- **AI Integration**: Google Gemini 2.0 Flash for advanced analysis
- **Capabilities**: 
  - Financial ratio analysis and forecasting
  - Legal document processing
  - Risk assessment and scoring
  - Market intelligence gathering
  - Compliance monitoring

## 🔌 API Integration

AMAN integrates with multiple external APIs:

- **Financial Data**: Alpha Vantage, Financial Modeling Prep, Polygon.io
- **Legal Data**: SEC EDGAR, OpenCorporates
- **News & Sentiment**: NewsAPI, social media APIs
- **Geopolitical**: World Bank, OFAC sanctions
- **Market Intelligence**: Google Trends, BuiltWith
- **AI Services**: Google Gemini 2.0 Flash

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm test                 # Run tests
npm run test:watch      # Watch mode
npm run test:coverage   # Coverage report
```

### Backend Testing
```bash
cd backend
npm test                # Run API tests
npm run test:watch     # Watch mode
```

### Agent Testing
```bash
cd agents
python -m pytest       # Run Python tests
python -m pytest -v    # Verbose output
```

## 🚀 Deployment

### Production Docker
```bash
# Build and start production environment
./docker/docker-helper.sh prod

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Environment Variables

<details>
<summary>Required environment variables</summary>

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aman
REDIS_URL=redis://localhost:6379

# API Keys
ALPHA_VANTAGE_API_KEY=your_key_here
FMP_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Security
JWT_SECRET=your_jwt_secret
API_RATE_LIMIT=100
```

#### Agents (.env)
```env
# AI Services
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# External APIs
NEWS_API_KEY=your_news_api_key
TWITTER_BEARER_TOKEN=your_twitter_token
```

</details>

## 📊 Features in Detail

### 🤖 ML-Powered Financial Analysis
- **Ratio Analysis**: 15+ financial ratios with trend analysis
- **Anomaly Detection**: ML-based irregularity detection
- **Forecasting**: 3-year predictions with confidence intervals
- **Health Scoring**: 0-100 financial health scores with letter grades

### 📈 Interactive Dashboard
- **Real-time Updates**: Live data streaming and updates
- **Customizable Views**: Drag-and-drop dashboard components
- **Advanced Charts**: Interactive visualizations with drill-down
- **Export Capabilities**: PDF reports and data export

### 🔍 Due Diligence Automation
- **Document Processing**: AI-powered document analysis
- **Risk Assessment**: Multi-dimensional risk scoring
- **Compliance Checking**: Automated regulatory compliance
- **Timeline Prediction**: M&A process timeline forecasting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- **Frontend**: ESLint + Prettier, TypeScript strict mode
- **Backend**: ESLint, comprehensive error handling
- **Python**: PEP 8, type hints, docstrings
- **Testing**: Minimum 70% code coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini 2.0 Flash** for advanced AI capabilities
- **Material-UI** for beautiful React components
- **Next.js** for the amazing React framework
- **scikit-learn** for machine learning capabilities
- **PostgreSQL** for robust data storage

---

