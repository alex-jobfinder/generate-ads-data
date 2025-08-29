# Test-Driven Development Process for ChatGPT

## Overview
This document outlines the Test-Driven Development (TDD) process that ChatGPT must follow when implementing any feature or functionality. The process follows the Red-Green-Refactor cycle and ensures code quality through comprehensive testing.

## TDD Process Flow

### Phase 1: Test-First Development (RED)
**ChatGPT MUST start here - no code implementation until tests are written**

1. **Understand Requirements**
   - Ask clarifying questions about the feature
   - Identify edge cases and failure modes
   - Define acceptance criteria

2. **Write Tests First**
   - Create comprehensive test files
   - Include unit tests, integration tests, and edge case tests
   - Use descriptive test names that explain the expected behavior
   - Test both happy path and failure scenarios

3. **Verify Tests Fail (RED)**
   - Run tests to confirm they fail (this validates the tests are meaningful)
   - Document expected failures
   - Ensure test coverage is comprehensive

### Phase 2: Implementation (GREEN)
**Only after tests are written and verified to fail**

1. **Implement Minimal Code**
   - Write the simplest code that makes tests pass
   - Focus on functionality, not optimization
   - Use the tests as a specification for what to build

2. **Iterate Until All Tests Pass**
   - Run tests after each small change
   - Fix any test failures
   - Continue until all tests pass

### Phase 3: Refactoring (REFACTOR)
**Only after all tests pass**

1. **Clean Up Code**
   - Improve code structure and readability
   - Remove duplication
   - Apply best practices and design patterns
   - Ensure code follows project standards

2. **Verify Tests Still Pass**
   - Run tests after each refactoring step
   - Ensure no functionality is broken
   - Maintain test coverage

## Implementation Rules

### Rule 1: Test-First Mandatory
- **NEVER write implementation code before tests**
- **ALWAYS start with test creation**
- Tests must be comprehensive and cover all scenarios

### Rule 2: Test Quality Standards
- Test names must clearly describe expected behavior
- Each test should test one specific thing
- Include positive and negative test cases
- Test edge cases and boundary conditions
- Mock external dependencies appropriately

### Rule 3: Implementation Standards
- Write minimal code to pass tests
- Follow project coding standards
- Use meaningful variable and function names
- Add appropriate error handling
- Include necessary documentation

### Rule 4: Refactoring Standards
- Only refactor after tests pass
- Maintain test coverage during refactoring
- Apply SOLID principles where appropriate
- Remove code duplication
- Improve readability and maintainability

## Example TDD Workflow

### Step 1: Write Tests (RED)
```python
# test_calculator.py
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(5, 0) == 5

def test_add_floats():
    assert add(2.5, 3.5) == 6.0

def test_add_strings_raises_error():
    with pytest.raises(TypeError):
        add("2", "3")
```

### Step 2: Run Tests (Confirm RED)
```bash
pytest test_calculator.py
# Expected: All tests fail (function doesn't exist yet)
```

### Step 3: Implement Code (GREEN)
```python
# calculator.py
def add(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a + b
```

### Step 4: Run Tests (Confirm GREEN)
```bash
pytest test_calculator.py
# Expected: All tests pass
```

### Step 5: Refactor (REFACTOR)
```python
# calculator.py (refactored)
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
        
    Raises:
        TypeError: If arguments are not numbers
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a + b
```

### Step 6: Verify Tests Still Pass
```bash
pytest test_calculator.py
# Expected: All tests still pass
```

## ChatGPT TDD Checklist

### Before Starting Implementation:
- [ ] Requirements are clear and understood
- [ ] Edge cases identified
- [ ] Acceptance criteria defined
- [ ] Test framework chosen

### Test Creation Phase:
- [ ] Unit tests written for all functions/methods
- [ ] Integration tests written for component interactions
- [ ] Edge case tests written
- [ ] Error handling tests written
- [ ] Tests run and confirmed to fail (RED)

### Implementation Phase:
- [ ] Minimal code written to make tests pass
- [ ] All tests run and pass (GREEN)
- [ ] Code follows project standards
- [ ] Error handling implemented

### Refactoring Phase:
- [ ] Code cleaned up and optimized
- [ ] Duplication removed
- [ ] Best practices applied
- [ ] All tests still pass after refactoring
- [ ] Code is readable and maintainable

## Common TDD Anti-Patterns to Avoid

1. **Writing code before tests** - This violates TDD principles
2. **Incomplete test coverage** - Missing edge cases or failure scenarios
3. **Over-engineering** - Implementing features not required by tests
4. **Skipping refactoring** - Not cleaning up code after tests pass
5. **Testing implementation details** - Tests should focus on behavior, not implementation

## Benefits of This TDD Process

1. **Better Design** - Tests force you to think about the interface first
2. **Regression Prevention** - Tests catch bugs when refactoring
3. **Documentation** - Tests serve as living documentation
4. **Confidence** - You know your code works as expected
5. **Maintainability** - Code is easier to modify with test coverage

## When to Use TDD

- **New feature development**
- **Bug fixes** (write test first to reproduce the bug)
- **Code refactoring** (ensure tests pass before and after)
- **API development** (test the interface first)
- **Legacy code modification** (add tests before making changes)

## Conclusion

Following this TDD process ensures that ChatGPT delivers high-quality, well-tested code. The process emphasizes:

1. **Test-first approach** - Always write tests before implementation
2. **Comprehensive testing** - Cover all scenarios and edge cases
3. **Iterative development** - Small steps with continuous testing
4. **Quality assurance** - Tests validate functionality and prevent regressions

Remember: **Tests are not an afterthought - they are the specification for what you're building.**
