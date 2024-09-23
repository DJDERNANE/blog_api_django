from eventsourcing.domain import Aggregate, event
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Article(Aggregate):
    """Aggregate root for the Article."""

    # Django fields are not strictly necessary in event-sourced models, but you may use them for certain use cases
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @event('Created')
    def create_article(self, title, content, user):
        """Method to handle creating an article."""
        self.title = title
        self.content = content
        self.published_date = self.published_date
        self.user = user

    @event('Updated')
    def update_article(self, title=None, content=None, published_date=None, user=None):
        """Method to handle updating an article."""
        if title:
            self.title = title
        if content:
            self.content = content
        if published_date:
            self.published_date = published_date
        if user:
            self.user = user

    @event('Deleted')
    def delete_article(self):
        """Method to handle deleting an article."""
        self.title = None
        self.content = None
        self.published_date = None
        self.user = None

    def apply_article_event(self, event):
        """Apply an event to update the state of the article."""
        if event.title is not None:
            self.title = event.title
        if event.content is not None:
            self.content = event.content
        if event.published_date is not None:
            self.published_date = event.published_date
        if event.user_id is not None:
            self.user = User.objects.get(pk=event.user_id)

        # Save the state to the database
        self.save()

class Comment(models.Model):
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', null=True)

    def __str__(self):
        return self.content
