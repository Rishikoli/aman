# Synergy Discovery Engine

## Overview

The Synergy Discovery Engine is an intelligent system that identifies and quantifies merger & acquisition synergies using pandas/NumPy-based financial modeling and AI-powered strategic analysis.

## Features

### Cost Synergies Analysis
- **Personnel Overlap**: Identifies duplicate roles and calculates elimination savings
- **Technology Consolidation**: Analyzes software license and infrastructure consolidation opportunities
- **Facilities Optimization**: Evaluates office space and facilities consolidation potential
- **Operations Streamlining**: Identifies process redundancies and efficiency improvements

### Revenue Synergies Analysis
- **Cross-selling Opportunities**: Analyzes potential for selling products to combined customer base
- **Market Expansion**: Identifies new geographic or segment expansion opportunities
- **Competitive Positioning**: Evaluates enhanced market position benefits

### Integration Risk Assessment
- **Cultural Integration**: Assesses cultural compatibility and change management risks
- **Technology Integration**: Evaluates system compatibility and integration complexity
- **Regulatory Compliance**: Identifies regulatory approval and compliance risks
- **Customer Retention**: Analyzes customer concentration and retention risks

### Financial Modeling
- **NPV Calculations**: 5-year net present value analysis with 10% discount rate
- **Break-even Analysis**: Timeline to recover integration investments
- **Confidence Scoring**: Risk-adjusted confidence levels for synergy realization
- **Sensitivity Analysis**: Impact of various risk factors on synergy value

## Requirements Satisfied

- **6.4**: Single-variable cost savings estimates (eliminated positions, etc.)
- **6.5**: Integration risk identification and dependency highlighting

## Usage

```python
from synergy_discovery_engine import SynergyDiscoveryEngine

# Initialize the engine
engine = SynergyDiscoveryEngine()

# Prepare company data
acquirer_data = {
    "name": "AcquirerCorp",
    "revenue": 100000000,
    "employees": 1000,
    "customers": 2000,
    "industry": "technology",
    "locations": ["New York", "San Francisco"],
    "markets": ["North America", "Europe"],
    "technology_stack": ["Python", "React", "PostgreSQL"],
    "avg_salary": 85000
}

target_data = {
    "name": "TargetCorp",
    "revenue": 50000000,
    "employees": 500,
    "customers": 1000,
    "industry": "technology",
    "locations": ["Austin", "Chicago"],
    "markets": ["North America"],
    "technology_stack": ["Java", "Angular", "MySQL"],
    "avg_salary": 80000
}

# Run synergy analysis
analysis = engine.analyze_synergies(acquirer_data, target_data, "DEAL_001")

# Generate AI insights (requires Gemini API key)
insights = engine.generate_ai_insights(analysis)
```

## Output Structure

### SynergyAnalysis
- `deal_id`: Unique deal identifier
- `acquirer_name`: Name of acquiring company
- `target_name`: Name of target company
- `cost_synergies`: List of identified cost reduction opportunities
- `revenue_synergies`: List of identified revenue enhancement opportunities
- `integration_risks`: List of integration challenges and risks
- `total_estimated_value`: Total annual synergy value
- `net_present_value`: 5-year NPV of synergies
- `time_to_break_even`: Months to recover integration costs
- `confidence_level`: Overall confidence in synergy realization

### Cost Synergy Details
- Type (personnel, technology, facilities, operations)
- Annual savings amount
- One-time implementation costs
- Time to realize (months)
- Risk level and confidence score
- Affected departments
- Implementation complexity assessment

### Revenue Synergy Details
- Type (revenue, market expansion)
- Annual revenue potential
- Required investment
- Time to realize (months)
- Risk level and confidence score
- Target market segments
- Competitive advantage description

### Integration Risk Details
- Risk category and description
- Severity level and probability
- Business impact assessment
- Mitigation strategies
- Timeline and cost impact

## Configuration

Set the following environment variables:

```bash
# Optional: For AI-powered insights
GEMINI_API_KEY=your_gemini_api_key

# Database connection (inherited from main config)
DATABASE_URL=postgresql://username:password@localhost:5432/aman_db
```

## Dependencies

- pandas: Financial data analysis and modeling
- numpy: Numerical calculations and statistical analysis
- requests: API calls for external data sources
- python-dotenv: Environment variable management
- dataclasses: Structured data models

## Testing

Run the built-in test example:

```bash
cd agents/synergy
python synergy_discovery_engine.py
```

This will run a sample analysis with mock data and display the results.

## Integration

The Synergy Discovery Engine integrates with:

- **Deal Orchestrator**: Receives analysis requests via message queue
- **Finance Agent**: Uses financial data for synergy calculations
- **Database**: Stores analysis results and historical patterns
- **Gemini API**: Generates strategic insights and recommendations

## Limitations

- Geographic overlap detection uses simple string matching (production would use geocoding)
- AI insights require Gemini API key configuration
- Industry-specific synergy patterns are generalized
- Customer and market data assumptions may need calibration for specific industries

## Future Enhancements

- Machine learning models for synergy prediction based on historical deals
- Integration with external market research APIs
- Advanced geographic analysis using mapping services
- Industry-specific synergy templates and benchmarks
- Real-time competitive intelligence integration