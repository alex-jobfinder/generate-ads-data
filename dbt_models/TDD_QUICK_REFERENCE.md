# TDD Quick Reference Card for ChatGPT

## 🚫 NEVER WRITE CODE BEFORE TESTS!

## TDD Process (Red-Green-Refactor)

### 🔴 PHASE 1: RED (Write Tests First)
1. **Understand requirements** - Ask clarifying questions
2. **Write comprehensive tests** - Cover all scenarios including edge cases
3. **Verify tests fail** - Run tests to confirm they fail (function doesn't exist yet)

### 🟢 PHASE 2: GREEN (Make Tests Pass)
1. **Write minimal code** - Just enough to make tests pass
2. **Iterate** - Run tests after each small change
3. **Verify all tests pass** - Continue until everything works

### 🔄 PHASE 3: REFACTOR (Clean Up)
1. **Improve code** - Better structure, readability, remove duplication
2. **Verify tests still pass** - Ensure refactoring didn't break anything

## Test Writing Checklist

- [ ] **Unit tests** for each function/method
- [ ] **Edge cases** (zero, negative, boundary values)
- [ ] **Error conditions** (invalid inputs, exceptions)
- [ ] **Happy path** (normal operation)
- [ ] **Integration tests** for component interactions
- [ ] **Descriptive test names** that explain expected behavior

## Test Quality Standards

```python
# ✅ GOOD - Clear, descriptive, tests one thing
def test_calculate_ctr_with_zero_impressions_raises_error():
    """Test that CTR calculation fails when impressions is zero"""
    with pytest.raises(ValueError, match="Impressions cannot be zero"):
        calculator.calculate_ctr(impressions=0, clicks=10)

# ❌ BAD - Vague, tests multiple things
def test_calculator():
    assert calculator.calculate_ctr(100, 5) == 0.05
    assert calculator.calculate_cpm(100, 1000) == 100
```

## Implementation Rules

1. **Start with tests** - Always write tests first
2. **Minimal code** - Write simplest code that passes tests
3. **Run tests frequently** - After every small change
4. **Fix failures immediately** - Don't let tests fail for long
5. **Refactor only after green** - Clean up only when tests pass

## Common Anti-Patterns to Avoid

- ❌ Writing code before tests
- ❌ Skipping edge case tests
- ❌ Over-engineering features not required by tests
- ❌ Refactoring before tests pass
- ❌ Testing implementation details instead of behavior

## Quick Commands

```bash
# Run tests
pytest test_file.py -v

# Run tests with coverage
pytest --cov=module_name test_file.py

# Run specific test
pytest test_file.py::test_function_name

# Run tests and stop on first failure
pytest -x test_file.py
```

## Remember: Tests Are Your Specification!

- Tests define what your code should do
- Tests catch bugs when refactoring
- Tests serve as documentation
- Tests give confidence in your code
- Tests force better design decisions

## When You're Stuck

1. **Write more tests** - Cover the scenario you're trying to implement
2. **Make tests pass one by one** - Focus on one test at a time
3. **Keep it simple** - Don't overthink the implementation
4. **Ask questions** - Clarify requirements if unclear
5. **Break it down** - Smaller tests for smaller pieces of functionality

---

**Bottom Line: If you're not writing tests first, you're not doing TDD!**
