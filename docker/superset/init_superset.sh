#!/bin/bash
# Superset initialization script for AMAN

set -e

echo "Initializing Apache Superset for AMAN..."

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U aman_user; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Initialize Superset database
echo "Initializing Superset database..."
superset db upgrade

# Create admin user
echo "Creating admin user..."
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@aman.local \
    --password admin123

# Initialize Superset
echo "Initializing Superset..."
superset init

# Load example data (optional)
echo "Loading AMAN-specific configurations..."

# Import AMAN database connection
echo "Setting up AMAN database connection..."
superset set_database_uri \
    --database_name "AMAN PostgreSQL" \
    --uri "postgresql://aman_user:aman_password@postgres:5432/aman_db"

echo "Superset initialization complete!"
echo "Access Superset at http://localhost:8088"
echo "Username: admin"
echo "Password: admin123"