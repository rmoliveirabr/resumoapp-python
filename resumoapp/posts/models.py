from django.db import models
from django.urls import reverse
from django.conf import settings

from taggit.managers import TaggableManager

# Managers
# class PostManager(models.Manager):
#     def search(self, query):
#         return self.get_queryset().filter(
#             ####################### REVIEW AFTER POST IS CREATED
#             models.Q(name__icontains=query) | \
#             models.Q(description__icontains=query)
#         )

# Models
class EducationGroup(models.Model):
    name = models.CharField('Grupos de Educação', max_length=100)
    small = models.CharField('Grupos de Educação - Reduzido', max_length=10)

    def __str__ (self):
        return '{0} - {1}'.format(self.small, self.name)

    class Meta:
        verbose_name = 'grupo de educação'
        verbose_name_plural = 'grupos de educação'
        ordering = [ 'name']

class EducationYear(models.Model):
    group = models.ForeignKey(EducationGroup,
        verbose_name = 'Grupo de Educação',
        related_name = 'years',
        on_delete=models.CASCADE,)
    year = models.CharField('Ano / Período', max_length=100)

    def __str__ (self):
        # return '{0} do {1}'.format(self.year, self.group)
        return self.year

    class Meta:
        verbose_name = 'ano ou período'
        verbose_name_plural = 'anos ou períodos'
        ordering = [ 'year']

class EducationSubject(models.Model):
    subject = models.CharField('Matéria', max_length=100)

    def __str__ (self):
        return self.subject

    class Meta:
        verbose_name = 'matéria'
        verbose_name_plural = 'matérias'
        ordering = [ 'subject']

class SubjectTopic(models.Model):
    subject = models.ForeignKey(EducationSubject,
        verbose_name = 'Matéria',
        related_name = 'topics',
        on_delete=models.CASCADE,)
    topic = models.CharField('Assunto da Matéria', max_length=100)

    def __str__ (self):
        # return '{0} dentro de {1}'.format(self.topic, self.subject)
        return self.topic

    class Meta:
        verbose_name = 'assunto da matéria'
        verbose_name_plural = 'assuntos das matérias'
        ordering = [ 'topic']

class Post(models.Model):
    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name = 'Autor',
        related_name = 'posts',
        on_delete=models.CASCADE,)
    group = models.ForeignKey(EducationGroup,
        verbose_name = 'Grupo de Educação',
        related_name = 'posts',
        on_delete=models.CASCADE,)
    year = models.ForeignKey(EducationYear,
        verbose_name = 'Ano / Período',
        related_name = 'posts',
        on_delete=models.CASCADE,)
    subject = models.ForeignKey(EducationSubject,
        verbose_name = 'Matéria',
        related_name = 'posts',
        on_delete=models.CASCADE,)
    topic = models.ForeignKey(SubjectTopic,
        verbose_name = 'Assunto da Matéria',
        related_name = 'posts',
        on_delete=models.CASCADE,)
    draft = models.BooleanField('Rascunho?', default=True)
    views = models.IntegerField('Visualizações', blank=True, default=0)
    rating = models.IntegerField('Avaliação (1-5)', blank=True, default=0) #1-5, 1 is lowest

    tags = TaggableManager(blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def get_absolute_url(self):
        return reverse('posts:details', kwargs={'slug': self.slug} )

    def __str__ (self):
        return '{0} dentro de {1} por {2}'.format(self.topic, self.year, self.user)

    class Meta:
        verbose_name = 'resumo'
        verbose_name_plural = 'resumo'
        ordering = [ '-updated_at']
