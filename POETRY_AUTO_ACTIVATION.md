# Poetry Auto-Activation Setup

This repository is configured to automatically activate the Poetry virtual environment when you enter the directory. Choose one of the methods below:

## 🚀 Method 1: Automatic with `direnv` (Recommended)

### Prerequisites
- Install `direnv`: `sudo apt install direnv` (Ubuntu/Debian) or `brew install direnv` (macOS)
- Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
# Add to ~/.bashrc or ~/.zshrc
eval "$(direnv hook bash)"  # or zsh for zsh users
```

### Setup
1. The `.envrc` file is already created and configured
2. Run `direnv allow` once to enable it
3. **That's it!** The environment will auto-activate when you `cd` into this directory

### What happens automatically:
- ✅ Poetry virtual environment activates
- ✅ DBT profiles directory is set
- ✅ Python path is configured
- ✅ Helpful info is displayed

## 🐚 Method 2: Manual Activation Script

### Usage
```bash
# From the project root directory
source activate_env.sh

# Or run it directly
./activate_env.sh
```

### What the script does:
- Activates Poetry virtual environment
- Sets DBT profiles directory
- Configures Python path
- Shows available commands

## 🔧 Method 3: Shell Profile Integration

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
# Auto-activate Poetry when entering specific directories
poetry_auto_activate() {
    if [[ -f "pyproject.toml" ]]; then
        POETRY_VENV=$(poetry env info --path 2>/dev/null)
        if [[ -n "$POETRY_VENV" && -d "$POETRY_VENV" ]]; then
            source "$POETRY_VENV/bin/activate"
            export DBT_PROFILES_DIR="$(pwd)/dbt_models"
            export PYTHONPATH="$(pwd):$PYTHONPATH"
            echo "🐍 Poetry environment activated for $(basename $(pwd))"
        fi
    fi
}

# Hook into directory changes
cd() {
    builtin cd "$@"
    poetry_auto_activate
}
```

## 🎯 Current Configuration

This repository is set up with:

- **Poetry**: Python dependency management
- **dbt-duckdb**: DBT adapter for DuckDB
- **dbt-metricflow**: Semantic layer capabilities
- **Auto-activation**: Virtual environment activates automatically

## 🚨 Troubleshooting

### Environment not activating?
1. Check if `direnv` is installed: `which direnv`
2. Verify `.envrc` is allowed: `direnv status`
3. Check Poetry installation: `poetry --version`

### DBT commands not found?
1. Ensure Poetry environment is active: `poetry env info`
2. Check if dbt is installed: `poetry show dbt-duckdb`
3. Verify virtual environment: `which dbt`

### Permission denied on `.envrc`?
```bash
direnv allow
```

## 🔄 Manual Commands

If auto-activation isn't working, you can always:

```bash
# Activate manually
poetry shell

# Or run commands directly
poetry run dbt --version
poetry run python your_script.py
```

## 📚 Useful Commands

```bash
# Check environment status
poetry env info

# List installed packages
poetry show

# Add new package
poetry add package-name

# Run DBT commands
poetry run dbt debug
poetry run dbt run
poetry run dbt test

# Exit environment
deactivate  # if using source activate_env.sh
exit        # if using poetry shell
```

## 🎉 Benefits of Auto-Activation

- **No more forgetting to activate environments**
- **Consistent development environment**
- **Automatic DBT configuration**
- **Project-specific Python path**
- **Helpful command reminders**

---

**Note**: The `.envrc` file is already configured and should work immediately after running `direnv allow` once.