# TDD Example Workflow: Campaign Performance Calculator

This document demonstrates the TDD process in action using a real-world example from your dbt project.

## Scenario: Create a Campaign Performance Calculator

**Requirement**: Build a function that calculates key advertising metrics like CTR, CPM, and conversion rates from campaign performance data.

## Phase 1: Test-First Development (RED)

### Step 1: Understand Requirements
- Calculate Click-Through Rate (CTR)
- Calculate Cost Per Mille (CPM) 
- Calculate Cost Per Click (CPC)
- Handle edge cases (zero impressions, negative values)
- Validate input data types

### Step 2: Write Tests First

```python
# test_campaign_calculator.py
import pytest
from campaign_calculator import CampaignCalculator

class TestCampaignCalculator:
    
    def test_calculate_ctr_with_valid_data(self):
        """Test CTR calculation with valid impression and click data"""
        calculator = CampaignCalculator()
        ctr = calculator.calculate_ctr(impressions=1000, clicks=50)
        assert ctr == 0.05  # 5%
    
    def test_calculate_ctr_with_zero_impressions(self):
        """Test CTR calculation when impressions is zero"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Impressions cannot be zero"):
            calculator.calculate_ctr(impressions=0, clicks=10)
    
    def test_calculate_ctr_with_negative_impressions(self):
        """Test CTR calculation with negative impressions"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Impressions must be positive"):
            calculator.calculate_ctr(impressions=-100, clicks=10)
    
    def test_calculate_ctr_with_negative_clicks(self):
        """Test CTR calculation with negative clicks"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Clicks must be non-negative"):
            calculator.calculate_ctr(impressions=100, clicks=-10)
    
    def test_calculate_ctr_with_more_clicks_than_impressions(self):
        """Test CTR calculation when clicks exceed impressions"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Clicks cannot exceed impressions"):
            calculator.calculate_ctr(impressions=100, clicks=150)
    
    def test_calculate_cpm_with_valid_data(self):
        """Test CPM calculation with valid spend and impression data"""
        calculator = CampaignCalculator()
        cpm = calculator.calculate_cpm(spend=100.0, impressions=1000)
        assert cpm == 100.0  # $100 per 1000 impressions
    
    def test_calculate_cpm_with_zero_impressions(self):
        """Test CPM calculation when impressions is zero"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Impressions cannot be zero"):
            calculator.calculate_cpm(spend=100.0, impressions=0)
    
    def test_calculate_cpc_with_valid_data(self):
        """Test CPC calculation with valid spend and click data"""
        calculator = CampaignCalculator()
        cpc = calculator.calculate_cpc(spend=100.0, clicks=50)
        assert cpc == 2.0  # $2 per click
    
    def test_calculate_cpc_with_zero_clicks(self):
        """Test CPC calculation when clicks is zero"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Clicks cannot be zero"):
            calculator.calculate_cpc(spend=100.0, clicks=0)
    
    def test_calculate_cpc_with_negative_spend(self):
        """Test CPC calculation with negative spend"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Spend must be positive"):
            calculator.calculate_cpc(spend=-100.0, clicks=50)
    
    def test_calculate_conversion_rate_with_valid_data(self):
        """Test conversion rate calculation"""
        calculator = CampaignCalculator()
        conv_rate = calculator.calculate_conversion_rate(clicks=100, conversions=10)
        assert conv_rate == 0.10  # 10%
    
    def test_calculate_conversion_rate_with_zero_clicks(self):
        """Test conversion rate calculation when clicks is zero"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Clicks cannot be zero"):
            calculator.calculate_conversion_rate(clicks=0, conversions=10)
    
    def test_calculate_conversion_rate_with_conversions_exceeding_clicks(self):
        """Test conversion rate calculation when conversions exceed clicks"""
        calculator = CampaignCalculator()
        with pytest.raises(ValueError, match="Conversions cannot exceed clicks"):
            calculator.calculate_conversion_rate(clicks=50, conversions=75)
    
    def test_input_type_validation(self):
        """Test that non-numeric inputs raise TypeError"""
        calculator = CampaignCalculator()
        with pytest.raises(TypeError, match="All inputs must be numeric"):
            calculator.calculate_ctr(impressions="100", clicks=50)
        
        with pytest.raises(TypeError, match="All inputs must be numeric"):
            calculator.calculate_cpm(spend=[100], impressions=1000)
```

### Step 3: Verify Tests Fail (RED)
```bash
pytest test_campaign_calculator.py -v
# Expected: All tests fail because CampaignCalculator class doesn't exist yet
```

## Phase 2: Implementation (GREEN)

### Step 4: Implement Minimal Code

```python
# campaign_calculator.py
class CampaignCalculator:
    """Calculate advertising campaign performance metrics."""
    
    def calculate_ctr(self, impressions, clicks):
        """Calculate Click-Through Rate."""
        if not isinstance(impressions, (int, float)) or not isinstance(clicks, (int, float)):
            raise TypeError("All inputs must be numeric")
        
        if impressions <= 0:
            raise ValueError("Impressions must be positive")
        
        if clicks < 0:
            raise ValueError("Clicks must be non-negative")
        
        if clicks > impressions:
            raise ValueError("Clicks cannot exceed impressions")
        
        return clicks / impressions
    
    def calculate_cpm(self, spend, impressions):
        """Calculate Cost Per Mille (CPM)."""
        if not isinstance(spend, (int, float)) or not isinstance(impressions, (int, float)):
            raise TypeError("All inputs must be numeric")
        
        if impressions <= 0:
            raise ValueError("Impressions cannot be zero")
        
        return (spend / impressions) * 1000
    
    def calculate_cpc(self, spend, clicks):
        """Calculate Cost Per Click (CPC)."""
        if not isinstance(spend, (int, float)) or not isinstance(clicks, (int, float)):
            raise TypeError("All inputs must be numeric")
        
        if clicks <= 0:
            raise ValueError("Clicks cannot be zero")
        
        return spend / clicks
    
    def calculate_conversion_rate(self, clicks, conversions):
        """Calculate conversion rate."""
        if not isinstance(clicks, (int, float)) or not isinstance(conversions, (int, float)):
            raise TypeError("All inputs must be numeric")
        
        if clicks <= 0:
            raise ValueError("Clicks cannot be zero")
        
        if conversions < 0:
            raise ValueError("Conversions must be non-negative")
        
        if conversions > clicks:
            raise ValueError("Conversions cannot exceed clicks")
        
        return conversions / clicks
```

### Step 5: Run Tests (Confirm GREEN)
```bash
pytest test_campaign_calculator.py -v
# Expected: All tests pass
```

## Phase 3: Refactoring (REFACTOR)

### Step 6: Clean Up Code

```python
# campaign_calculator.py (refactored)
from typing import Union, Tuple
import logging

logger = logging.getLogger(__name__)

class CampaignCalculator:
    """
    Calculate advertising campaign performance metrics.
    
    This class provides methods to calculate common advertising metrics
    including CTR, CPM, CPC, and conversion rates with proper validation.
    """
    
    def _validate_numeric_inputs(self, *args) -> None:
        """Validate that all inputs are numeric."""
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise TypeError("All inputs must be numeric")
    
    def _validate_positive(self, value: Union[int, float], name: str) -> None:
        """Validate that a value is positive."""
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    
    def _validate_non_negative(self, value: Union[int, float], name: str) -> None:
        """Validate that a value is non-negative."""
        if value < 0:
            raise ValueError(f"{name} must be non-negative")
    
    def _validate_ratio(self, numerator: Union[int, float], denominator: Union[int, float], 
                       num_name: str, denom_name: str) -> None:
        """Validate that numerator doesn't exceed denominator."""
        if numerator > denominator:
            raise ValueError(f"{num_name} cannot exceed {denom_name}")
    
    def calculate_ctr(self, impressions: Union[int, float], clicks: Union[int, float]) -> float:
        """
        Calculate Click-Through Rate (CTR).
        
        Args:
            impressions: Number of ad impressions
            clicks: Number of ad clicks
            
        Returns:
            CTR as a decimal (e.g., 0.05 for 5%)
            
        Raises:
            TypeError: If inputs are not numeric
            ValueError: If inputs are invalid (negative, zero, or ratio violation)
        """
        self._validate_numeric_inputs(impressions, clicks)
        self._validate_positive(impressions, "Impressions")
        self._validate_non_negative(clicks, "Clicks")
        self._validate_ratio(clicks, impressions, "Clicks", "Impressions")
        
        ctr = clicks / impressions
        logger.debug(f"Calculated CTR: {ctr:.4f} for {clicks} clicks / {impressions} impressions")
        return ctr
    
    def calculate_cpm(self, spend: Union[int, float], impressions: Union[int, float]) -> float:
        """
        Calculate Cost Per Mille (CPM).
        
        Args:
            spend: Total advertising spend
            impressions: Number of ad impressions
            
        Returns:
            CPM as cost per 1000 impressions
        """
        self._validate_numeric_inputs(spend, impressions)
        self._validate_positive(impressions, "Impressions")
        
        cpm = (spend / impressions) * 1000
        logger.debug(f"Calculated CPM: ${cpm:.2f} for ${spend} / {impressions} impressions")
        return cpm
    
    def calculate_cpc(self, spend: Union[int, float], clicks: Union[int, float]) -> float:
        """
        Calculate Cost Per Click (CPC).
        
        Args:
            spend: Total advertising spend
            clicks: Number of ad clicks
            
        Returns:
            CPC as cost per click
        """
        self._validate_numeric_inputs(spend, clicks)
        self._validate_positive(clicks, "Clicks")
        
        cpc = spend / clicks
        logger.debug(f"Calculated CPC: ${cpc:.2f} for ${spend} / {clicks} clicks")
        return cpc
    
    def calculate_conversion_rate(self, clicks: Union[int, float], 
                                conversions: Union[int, float]) -> float:
        """
        Calculate conversion rate.
        
        Args:
            clicks: Number of ad clicks
            conversions: Number of conversions
            
        Returns:
            Conversion rate as a decimal
        """
        self._validate_numeric_inputs(clicks, conversions)
        self._validate_positive(clicks, "Clicks")
        self._validate_non_negative(conversions, "Conversions")
        self._validate_ratio(conversions, clicks, "Conversions", "Clicks")
        
        conv_rate = conversions / clicks
        logger.debug(f"Calculated conversion rate: {conv_rate:.4f} for {conversions} conversions / {clicks} clicks")
        return conv_rate
    
    def calculate_all_metrics(self, impressions: Union[int, float], clicks: Union[int, float],
                            spend: Union[int, float], conversions: Union[int, float] = 0) -> dict:
        """
        Calculate all available metrics in one call.
        
        Args:
            impressions: Number of ad impressions
            clicks: Number of ad clicks
            spend: Total advertising spend
            conversions: Number of conversions (optional)
            
        Returns:
            Dictionary containing all calculated metrics
        """
        metrics = {
            'ctr': self.calculate_ctr(impressions, clicks),
            'cpm': self.calculate_cpm(spend, impressions),
            'cpc': self.calculate_cpc(spend, clicks)
        }
        
        if conversions > 0:
            metrics['conversion_rate'] = self.calculate_conversion_rate(clicks, conversions)
        
        return metrics
```

### Step 7: Verify Tests Still Pass
```bash
pytest test_campaign_calculator.py -v
# Expected: All tests still pass after refactoring
```

## Additional Test Cases for Refactored Code

```python
# test_campaign_calculator_refactored.py
def test_calculate_all_metrics(self):
    """Test calculating all metrics in one call"""
    calculator = CampaignCalculator()
    metrics = calculator.calculate_all_metrics(
        impressions=1000, 
        clicks=50, 
        spend=100.0, 
        conversions=5
    )
    
    assert metrics['ctr'] == 0.05
    assert metrics['cpm'] == 100.0
    assert metrics['cpc'] == 2.0
    assert metrics['conversion_rate'] == 0.10

def test_calculate_all_metrics_without_conversions(self):
    """Test calculating all metrics without conversions"""
    calculator = CampaignCalculator()
    metrics = calculator.calculate_all_metrics(
        impressions=1000, 
        clicks=50, 
        spend=100.0
    )
    
    assert 'conversion_rate' not in metrics
    assert metrics['ctr'] == 0.05
    assert metrics['cpm'] == 100.0
    assert metrics['cpc'] == 2.0

def test_logging_output(self):
    """Test that debug logging is working"""
    calculator = CampaignCalculator()
    with self.assertLogs(level='DEBUG') as log:
        calculator.calculate_ctr(1000, 50)
    
    assert any("Calculated CTR" in msg for msg in log.output)
```

## Summary of TDD Benefits Demonstrated

1. **Test-First Design**: Tests forced us to think about the interface and edge cases first
2. **Comprehensive Coverage**: All scenarios are tested, including error conditions
3. **Regression Prevention**: Refactoring didn't break existing functionality
4. **Documentation**: Tests serve as examples of how to use the class
5. **Confidence**: We know the code works correctly in all scenarios

## Key TDD Principles Applied

1. **Red-Green-Refactor Cycle**: Tests failed, then passed, then code was improved
2. **Test as Specification**: Tests defined exactly what the code should do
3. **Incremental Development**: Small changes with continuous testing
4. **Edge Case Coverage**: Comprehensive testing of failure scenarios
5. **Clean Code**: Refactoring improved readability and maintainability

This example demonstrates how TDD leads to better, more reliable code through systematic testing and validation.
