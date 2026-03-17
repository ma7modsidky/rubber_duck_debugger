from django.db import models

class DebugLog(models.Model):
    error_message = models.TextField()
    raw_traceback = models.TextField()
    ai_resolution = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Error on {self.created_at.strftime('%Y-%m-%d %H:%M')}"