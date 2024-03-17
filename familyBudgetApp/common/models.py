from django.db import models

# Create your models here.
class Tag(models.Model):
    TAG_MAX_LENGTH = 30

    name = models.CharField(max_length=TAG_MAX_LENGTH)

    def __str__(self):
        return self.name

    @property
    def list_tags(self):
        return ', '.join([tag.name for tag in self.tags.all()])

    def save(self, *args, **kwargs):
        if not self.name.islower():
            self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)