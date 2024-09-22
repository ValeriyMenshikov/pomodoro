from worker.celery import send_email_task


class MailClient:

    @staticmethod
    def send_welcome_email(to: str) -> None:
        print(f"Sending welcome email to {to}")
        return send_email_task.delay("Welcome email!", "Welcome to pomodoro!", to)
