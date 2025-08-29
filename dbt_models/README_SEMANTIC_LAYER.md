# dbt Semantic Layer Implementation

This project now includes the dbt Semantic Layer, powered by MetricFlow, which provides a centralized way to define and consume business metrics.

## What is the Semantic Layer?

The dbt Semantic Layer eliminates duplicate coding by allowing data teams to define metrics on top of existing models and automatically handling data joins. It provides:

- **Centralized metric definitions** - Define metrics once in dbt, use them everywhere
- **Consistent data access** - Ensure all business units work from the same metric definitions
- **Automatic joins** - Handle complex data relationships automatically
- **Secure access control** - Implement robust permissions for metric access

## Project Structure

```
dbt_models/
├── models/
│   └── semantic_layer/
│       ├── _semantic_manifest.yml    # Semantic model definitions
│       ├── metrics.yml               # Business metrics
│       └── campaign_performance.sql  # Data model for semantic layer
├── semantic_layer.yml                # Semantic layer configuration
├── packages.yml                      # Includes MetricFlow package
└── dbt_project.yml                   # Semantic layer enabled
```

## Key Components

### 1. Semantic Models (`_semantic_manifest.yml`)
Defines the structure of your data for the semantic layer:
- **Entities**: Primary business objects (campaign_performance)
- **Dimensions**: Categorical and time-based attributes
- **Measures**: Raw metrics that can be aggregated

### 2. Business Metrics (`metrics.yml`)
Defines business-level metrics using the semantic layer:
- **Simple metrics**: Direct aggregations (sum, avg)
- **Ratio metrics**: Calculated metrics (CTR, CPM, etc.)
- **Derived metrics**: Complex business logic

### 3. Data Models
SQL models that make your data available to the semantic layer.

## Available Metrics

### Core Performance Metrics
- `total_impressions` - Total ad impressions
- `total_clicks` - Total ad clicks  
- `total_spend` - Total advertising spend
- `overall_ctr` - Overall click-through rate
- `cost_per_click` - Average cost per click
- `cost_per_mille` - Cost per thousand impressions (CPM)

### Engagement Metrics
- `total_reach` - Unique audience reach
- `viewability_rate` - Overall viewability rate
- `video_completion_rate_overall` - Video completion rate
- `win_rate` - Auction win rate

### Quality Metrics
- `response_rate_overall` - Overall response rate
- `total_auctions_won` - Successful auctions
- `total_eligible_impressions` - Eligible impressions

## Usage Examples

### Querying Metrics via SQL
```sql
-- Get total impressions and clicks for a specific campaign
SELECT 
  campaign_id,
  {{ metric('total_impressions') }} as impressions,
  {{ metric('total_clicks') }} as clicks,
  {{ metric('overall_ctr') }} as ctr
FROM {{ ref('campaign_performance') }}
WHERE campaign_id = 123
GROUP BY campaign_id
```

### Using Metrics in dbt Models
```sql
-- Create a campaign summary model
SELECT 
  campaign_id,
  {{ metric('total_impressions') }} as total_impressions,
  {{ metric('total_clicks') }} as total_clicks,
  {{ metric('cost_per_click') }} as cpc,
  {{ metric('viewability_rate') }} as viewability
FROM {{ ref('campaign_performance') }}
GROUP BY campaign_id
```

## Setup and Installation

1. **Install dependencies**:
   ```bash
   dbt deps
   ```

2. **Run the semantic layer**:
   ```bash
   dbt run --select semantic_layer
   ```

3. **Test the semantic layer**:
   ```bash
   dbt test --select semantic_layer
   ```

## Configuration

The semantic layer is configured in `semantic_layer.yml`:
- **Connection**: Configured for DuckDB
- **Caching**: Enabled with 1-hour TTL
- **Access Control**: Basic role-based access
- **Validation**: Metric validation enabled

## Benefits

1. **Consistency**: All metrics defined in one place
2. **Maintainability**: Update metric logic once, propagate everywhere
3. **Performance**: Built-in caching and optimization
4. **Governance**: Centralized access control and validation
5. **Self-Service**: Business users can access metrics without SQL knowledge

## Next Steps

1. **Deploy**: Run `dbt run` to materialize the semantic layer
2. **Integrate**: Connect BI tools that support the dbt Semantic Layer
3. **Extend**: Add more metrics and dimensions as needed
4. **Monitor**: Use dbt's built-in testing and validation

## Resources

- [dbt Semantic Layer Documentation](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)
- [MetricFlow Documentation](https://docs.getdbt.com/docs/build/metricflow)
- [Semantic Layer Best Practices](https://docs.getdbt.com/docs/guides/best-practices/semantic-layer)
