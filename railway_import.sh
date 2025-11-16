#!/bin/bash
# Helper script to run Django commands on Railway
# Usage: railway shell < railway_import.sh

echo "Running data import on Railway..."
python manage.py loaddata vpq_production_export.json

echo "Extracting media files..."
tar -xzf media_backup_20251113.tar.gz

echo "Creating superuser..."
python create_superuser.py

echo "Done!"
