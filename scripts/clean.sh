#!/bin/bash
# Clean up containers and volumes

echo "🧹 Cleaning up Bank API..."

# Stop and remove containers
docker-compose down

# Remove volumes (optional)
if [ "$1" = "--volumes" ]; then
    echo "🗑️  Removing volumes..."
    docker-compose down -v
    docker volume prune -f
fi

# Remove images (optional)
if [ "$1" = "--all" ]; then
    echo "🗑️  Removing images..."
    docker-compose down -v --rmi all
    docker system prune -f
fi

echo "✅ Cleanup complete!"
