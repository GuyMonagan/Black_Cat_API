from django.db import models
from django.utils import timezone
from users.models import User
from books.models import Book

class Review(models.Model):
    """
    Модель отзыва на книгу.

    Каждый отзыв связан с пользователем и книгой.
    Один пользователь может оставить только один отзыв на одну книгу.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('book', 'user')  # один отзыв от одного юзера на книгу
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} on {self.book.title}"
