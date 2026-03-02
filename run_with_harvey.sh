#!/bin/bash

# Startup script for running with Harvey AI
# Make this file executable: chmod +x run_with_harvey.sh

echo "🚀 Starting application with Harvey AI..."

# Set Harvey AI environment variables
# IMPORTANT: Replace with your actual Harvey API key
export HARVEY_API_KEY="your-harvey-api-key-here"
export HARVEY_BASE_URL="https://eu.api.harvey.ai"
export HARVEY_TIMEOUT="240"

# Check if API key is set
if [ "$HARVEY_API_KEY" = "your-harvey-api-key-here" ]; then
    echo "❌ ERROR: Please set your actual Harvey API key in this script"
    echo "   Edit run_with_harvey.sh and replace 'your-harvey-api-key-here' with your actual key"
    exit 1
fi

echo "✅ Harvey API key configured"
echo "✅ Base URL: $HARVEY_BASE_URL"
echo "✅ Timeout: $HARVEY_TIMEOUT seconds"

# Run Django development server
echo ""
echo "Starting Django development server..."
python manage.py runserver
