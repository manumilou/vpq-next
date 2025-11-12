#!/bin/bash
# Export script for migrating from PythonAnywhere to Railway
# Run this on PythonAnywhere

echo "🚀 Exporting data for Railway migration..."
echo ""

# Activate virtualenv
source ~/.virtualenvs/vpq-env/bin/activate

cd ~/vpq-next

# Export database to JSON
echo "📦 Exporting database..."
python manage.py dumpdata \
  --natural-foreign \
  --natural-primary \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions.session \
  --indent 2 \
  > vpq_data_export.json

if [ $? -eq 0 ]; then
    echo "✅ Database exported to vpq_data_export.json"
    echo "   Size: $(du -h vpq_data_export.json | cut -f1)"
else
    echo "❌ Database export failed"
    exit 1
fi

# Create media backup
echo ""
echo "📸 Creating media files backup..."
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

if [ $? -eq 0 ]; then
    echo "✅ Media files backed up to media_backup_$(date +%Y%m%d).tar.gz"
    echo "   Size: $(du -h media_backup_$(date +%Y%m%d).tar.gz | cut -f1)"
else
    echo "❌ Media backup failed"
    exit 1
fi

echo ""
echo "✅ Export complete!"
echo ""
echo "Next steps:"
echo "1. Download these files from PythonAnywhere Files tab:"
echo "   - vpq_data_export.json"
echo "   - media_backup_$(date +%Y%m%d).tar.gz"
echo ""
echo "2. Follow RAILWAY-DEPLOYMENT.md Part 2 to set up Railway"
echo ""
