#!/bin/bash

# Shell Setup Script for Poetry Auto-Activation
# Source this script to add Poetry auto-activation functions to your current shell session
# Or add the functions to your ~/.bashrc or ~/.zshrc for permanent setup

echo "🔧 Setting up Poetry auto-activation functions..."

# Function to auto-activate Poetry environment
poetry_auto_activate() {
    if [[ -f "pyproject.toml" ]]; then
        POETRY_VENV=$(poetry env info --path 2>/dev/null)
        if [[ -n "$POETRY_VENV" && -d "$POETRY_VENV" ]]; then
            # Only activate if not already active
            if [[ "$VIRTUAL_ENV" != "$POETRY_VENV" ]]; then
                source "$POETRY_VENV/bin/activate"
                export DBT_PROFILES_DIR="$(pwd)/dbt_models"
                export PYTHONPATH="$(pwd):$PYTHONPATH"
                echo "🐍 Poetry environment activated for $(basename $(pwd))"
            fi
        fi
    fi
}

# Function to check and setup Poetry environment
poetry_setup() {
    if [[ -f "pyproject.toml" ]]; then
        echo "📦 Poetry project detected: $(basename $(pwd))"
        
        # Check if Poetry is installed
        if ! command -v poetry >/dev/null 2>&1; then
            echo "❌ Poetry is not installed. Please install Poetry first."
            return 1
        fi
        
        # Check if virtual environment exists
        POETRY_VENV=$(poetry env info --path 2>/dev/null)
        if [[ -z "$POETRY_VENV" ]] || [[ ! -d "$POETRY_VENV" ]]; then
            echo "🔧 Virtual environment not found. Creating one..."
            poetry install
        fi
        
        # Activate environment
        poetry_auto_activate
        
        echo "✅ Poetry environment ready!"
        echo "📁 DBT profiles: $DBT_PROFILES_DIR"
        echo "🐍 Python: $(which python)"
        echo "🔧 DBT: $(which dbt)"
    else
        echo "❌ No pyproject.toml found. Not a Poetry project."
    fi
}

# Function to show Poetry project status
poetry_status() {
    if [[ -f "pyproject.toml" ]]; then
        echo "📊 Poetry Project Status:"
        echo "  Project: $(basename $(pwd))"
        echo "  Poetry: $(poetry --version)"
        echo "  Environment: $(poetry env info --name)"
        echo "  DBT: $(dbt --version | head -1)"
        echo "  Python: $(which python)"
        echo "  DBT Profiles: $DBT_PROFILES_DIR"
    else
        echo "❌ Not a Poetry project (no pyproject.toml)"
    fi
}

# Hook into directory changes (for current session)
if [[ "$BASH_VERSION" ]]; then
    # Bash
    cd() {
        builtin cd "$@"
        poetry_auto_activate
    }
elif [[ "$ZSH_VERSION" ]]; then
    # Zsh
    cd() {
        builtin cd "$@"
        poetry_auto_activate
    }
fi

echo "✅ Poetry auto-activation functions added to current shell session!"
echo ""
echo "🚀 Available functions:"
echo "  poetry_setup     # Setup and activate Poetry environment"
echo "  poetry_status    # Show Poetry project status"
echo "  poetry_auto_activate  # Manually trigger auto-activation"
echo ""
echo "💡 Tip: Add these functions to your ~/.bashrc or ~/.zshrc for permanent setup"
echo "💡 Tip: Use 'poetry_setup' to initialize the environment in this directory"
