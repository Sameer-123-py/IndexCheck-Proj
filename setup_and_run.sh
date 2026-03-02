#!/bin/bash

echo "========================================="
echo "Harvey AI Setup & Run Script"
echo "========================================="
echo ""

# Check if HARVEY_API_KEY is already set
if [ -z "$HARVEY_API_KEY" ]; then
    echo "⚠️  HARVEY_API_KEY is not set!"
    echo ""
    echo "Please enter your Harvey API key:"
    read -r HARVEY_KEY
    export HARVEY_API_KEY="$HARVEY_KEY"
fi

# Set defaults for other variables if not set
if [ -z "$HARVEY_BASE_URL" ]; then
    export HARVEY_BASE_URL="https://eu.api.harvey.ai"
fi

if [ -z "$HARVEY_TIMEOUT" ]; then
    export HARVEY_TIMEOUT="240"
fi

echo ""
echo "✅ Harvey AI Configuration:"
echo "   API Key: ${HARVEY_API_KEY:0:10}..."
echo "   Base URL: $HARVEY_BASE_URL"
echo "   Timeout: $HARVEY_TIMEOUT seconds"
echo ""

# Verify settings.py has Harvey configured
echo "🔍 Checking settings.py..."
if grep -q "AI_PROVIDER = 'harvey'" etf_ai_project/settings.py; then
    echo "✅ AI_PROVIDER is set to 'harvey'"
else
    echo "❌ AI_PROVIDER is not set to 'harvey' in settings.py"
    echo ""
    echo "Would you like me to update it? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        # This would need manual update, just inform the user
        echo "Please manually update etf_ai_project/settings.py:"
        echo "Set: AI_PROVIDER = 'harvey'"
        exit 1
    fi
fi

echo ""
echo "========================================="
echo "🚀 Starting Django server with Harvey AI"
echo "========================================="
echo ""

# Run the Django server
python manage.py runserver
