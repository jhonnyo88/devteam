#!/bin/bash
#
# DigiNativa AI Team Runner
# Laddar .env automatiskt och startar production pipeline
#

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "❌ .env file not found"
    exit 1
fi

# Check if GitHub issue URL provided
if [ -z "$1" ]; then
    echo "❌ Missing GitHub issue URL"
    echo ""
    echo "Usage:"
    echo "  ./run_team.sh https://github.com/owner/repo/issues/123"
    echo "  ./run_team.sh --dry-run https://github.com/owner/repo/issues/123"
    echo ""
    echo "Example:"
    echo "  ./run_team.sh https://github.com/jhonnyo88/diginativa-game/issues/1"
    exit 1
fi

# Make sure script is executable
chmod +x "$0"

# Run the production pipeline
echo "🚀 Starting DigiNativa AI Team..."
echo "📋 Issue: $1"
echo ""

python3 start_production_pipeline.py "$@"