from celery import shared_task


@shared_task
def test_task(message):
    return f"Task processed: {message}"


@shared_task
def send_email_task(email, subject, message):
    # Simulate email sending
    return f"Email sent to {email} with subject: {subject}"
