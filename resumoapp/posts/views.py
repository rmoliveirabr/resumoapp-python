from django.shortcuts import render
from django.views.generic import FormView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

from django.utils.text import slugify

from .models import Post, EducationYear, SubjectTopic
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'posts/list_posts.html'
    paginate_by = 3

    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()

        order = self.request.GET.get('order', '')
        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'date':
            queryset = queryset.order_by('-updated_at')
        elif order == 'rating':
            queryset = queryset.order_by('-rating')

        if 'tag' in self.kwargs:
            tag = self.kwargs.get('tag', '')
            if tag:
                queryset = queryset.filter(tags__slug__icontains=tag)

        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/show_post.html'

    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, args, kwargs)
        if not self.request.user.is_authenticated or (self.object.user != self.request.user):
            self.object.views = self.object.views + 1
            self.object.save()
        return response

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/add_post.html'

    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        # set slug if it's not set yet - new objects
        # not treating cases where there is more than one equal title
        self.object.slug = slugify(self.object.title)

        self.object.save()
        form.save_m2m() # many-to-many, to save tags

        return HttpResponseRedirect(self.get_success_url())

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/add_post.html'

    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        # set slug if it's not set yet - new objects
        # not treating cases where there is more than one equal title
        self.object.slug = slugify(self.object.title)

        self.object.save()
        form.save_m2m() # many-to-many, to save tags

        return HttpResponseRedirect(self.get_success_url())

class PostDeleteView(DeleteView):
    model = Post
    form_class = PostForm

    success_url = reverse_lazy('posts:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

add_post = PostCreateView.as_view()
edit_post = PostUpdateView.as_view()
list_posts = PostListView.as_view()
show_post = PostDetailView.as_view()
delete_post = PostDeleteView.as_view()

#
#
#
def load_years(request):
    group_id = request.GET.get('group')
    years = EducationYear.objects.filter(group_id=group_id).order_by('year')
    return render(request, 'posts/year_dropdown_list_options.html', {'years': years})

def load_topics(request):
    subject_id = request.GET.get('subject')
    topics = SubjectTopic.objects.filter(subject_id=subject_id).order_by('topic')
    return render(request, 'posts/topic_dropdown_list_options.html', {'topics': topics})
