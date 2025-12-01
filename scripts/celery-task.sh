#!/bin/bash
# Test Celery tasks

echo "🔧 Testing Celery tasks..."

docker exec bank python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from user_auth.tasks import test_task, send_email_task

print('Testing Celery tasks...')
try:
    result1 = test_task.delay('Hello from script!')
    print(f'Test task: {result1.get(timeout=10)}')
    
    result2 = send_email_task.delay('test@example.com', 'Test', 'Message')
    print(f'Email task: {result2.get(timeout=10)}')
    
    print('🎉 All tasks working!')
except Exception as e:
    print(f'Task failed: {e}')
"
