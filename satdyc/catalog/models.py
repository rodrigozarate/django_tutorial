from django.db import models
import uuid
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    """
    Modelo que representa generos
    """
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género")

    def __str__(self):
        """
        Cadena que representa la instancia del modelo
        """
        return self.name


class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter the book's language")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """
    Modelo de un libro
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # Se usa ForeignKey para poder asignar de uno a muchos

    summary = models.TextField(max_length=1000, help_text="Descripción del libro")

    isbn = models.CharField('ISBN', max_length=13, help_text='Número ISBN de 13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">info</a>')

    genre = models.ManyToManyField(Genre, help_text="Género literario")

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        """
        Cadena de caracteres del objeto Book
        """
        return self.title

    def get_absolute_url(self):
        """
        URL de la instancia de Book
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        String for genre
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
        ('e', 'Extraviado'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)

