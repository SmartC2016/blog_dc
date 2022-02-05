from django.views import generic
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)  # only published Posts, no drafts
    template_name = "index.html"
    context_object_name = "posts"


class PostDetail(generic.DetailView):
    model = Post
    template_name = "post_detail.html"
