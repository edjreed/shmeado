from django.db import models

class Supporter(models.Model):
    """A Patreon supporter."""

    uuid = models.CharField(primary_key=True, max_length=32)
    tier = models.IntegerField()
    emoji = models.CharField(max_length=11)
    bio = models.TextField(null=True, blank=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.uuid} (Tier {self.tier})"
