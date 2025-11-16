#!/bin/bash
# One-time data import script for Railway

MARKER_FILE="/tmp/data_imported.marker"

if [ ! -f "$MARKER_FILE" ]; then
    echo "First deployment detected - importing data from PythonAnywhere..."

    # Import database data
    python manage.py import_from_pythonanywhere vpq_production_export.json

    # Extract media files
    if [ -f "media_backup_20251113.tar.gz" ]; then
        echo "Extracting media files..."
        tar -xzf media_backup_20251113.tar.gz
    fi

    # Create marker file so this only runs once
    touch "$MARKER_FILE"
    echo "Data import completed!"
else
    echo "Data already imported, skipping..."
fi
