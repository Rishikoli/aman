#!/bin/bash

# Production Deployment Script for Autonomous M&A Navigator
set -e

echo "🚀 Starting production deployment..."

# Check if .env.prod exists
if [ ! -f ".env.prod" ]; then
    echo "❌ Error: .env.prod file not found. Please create it from .env.prod template."
    exit 1
fi

# Load environment variables
export $(cat .env.prod | grep -v '^#' | xargs)

# Build and deploy
echo "📦 Building production images..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "🔄 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

echo "🔍 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment complete!"
echo "🌐 Frontend: https://your-domain.com"
echo "📊 Superset: https://your-domain.com/superset"
echo "📈 Grafana: https://your-domain.com:3003"