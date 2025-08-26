#!/bin/bash
# Superset entrypoint script for AMAN

set -e

echo "Starting AMAN Superset initialization..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h postgres -p 5432 -U aman_user -d aman_db; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready!"

# Initialize Superset database
echo "Initializing Superset database..."
superset db upgrade

# Create admin user if it doesn't exist
echo "Creating admin user..."
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@aman.local \
    --password admin123 || echo "Admin user already exists"

# Initialize Superset
echo "Initializing Superset..."
superset init

# Load examples (optional, can be disabled)
# superset load_examples

# Create analytics views in PostgreSQL
echo "Creating analytics views..."
PGPASSWORD=aman_password psql -h postgres -U aman_user -d aman_db -f /app/sql/create_analytics_views.sql || echo "Analytics views creation failed or already exist"

echo "Creating scenario modeling views..."
PGPASSWORD=aman_password psql -h postgres -U aman_user -d aman_db -f /app/sql/create_scenario_views.sql || echo "Scenario views creation failed or already exist"

# Start Superset server in background
echo "Starting Superset server..."
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger &

# Wait for Superset to be ready
echo "Waiting for Superset server to start..."
sleep 30

# Run AMAN dashboard setup
echo "Setting up AMAN dashboards..."
python3 /app/setup_aman_dashboards.py || echo "Dashboard setup failed, continuing..."

# Keep the server running
echo "AMAN Superset is ready!"
echo "Access at: http://localhost:8088"
echo "Username: admin, Password: admin123"

# Keep container running
wait