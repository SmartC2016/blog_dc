from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from .models import Post
from .forms import CommentForm

# todo sitemap
# todo user login, logout


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")  # only published Posts, no drafts
    template_name = "index.html"
    context_object_name = "posts"
    paginate_by = 2


class PostDetail(View):
    """Very nice way, to have two views. One for GET request and another for POST request"""

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostDisplay(DetailView):
    # Only for the GET request
    model = Post
    template_name = "post_detail.html"

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.pk)])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(active=True)  # only show active comments
        context["form"] = CommentForm()
        return context


class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = "post_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("post_detail", kwargs={"slug": post.slug}) + "#comments"
