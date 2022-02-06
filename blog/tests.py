from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post, Comment


class BlogTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="heti",
            email="user@email.com",
            password="secret",
        )

        self.post = Post.objects.create(
            title="First Post - Test",
            slug="first-post-test",
            author=self.user,
            content="Some text about riding motorcycle.",
            status=1,
        )

        self.comment = Comment.objects.create(
            post=self.post,
            name="John Doe",
            email="johnny@doe.com",
            body="A comment on this post",
            active=True,
        )

    def test_post_list(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First Post")
        self.assertTemplateUsed(response, "index.html")

    def test_post_detail(self):
        slug = "first-post-test"
        response = self.client.get(reverse("post_detail", args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First Post")
        self.assertContains(response, "Some text about riding motorcycle.")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "A comment on this post")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_submit_comment_logged_in(self):
        self.client.login(username="heti", password="secret")
        slug = "first-post-test"
        url = reverse("post_detail", args=[slug])
        response = self.client.post(
            url,
            {
                "name": "heti",
                "body": "Thanks for your post.",
            },
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(Comment.objects.last().name, "Samuel")
        # self.assertEqual(Comment.objects.last().body, "Thanks for your post.")

    def test_submit_comment_logged_out_fail(self):
        self.client.logout()
        last_comment = Comment.objects.last()
        slug = last_comment.post.slug
        url = reverse("post_detail", args=[slug])
        response = self.client.post(
            url,
            {
                "name": "Heti",
                "comment": "I am not the real author.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you cannot use this name!")
        self.assertEqual(last_comment, Comment.objects.last())

    def test_submit_comment_logged_out_success(self):
        self.client.logout()
        last_comment = Comment.objects.last()
        slug = last_comment.post.slug
        url = reverse("post_detail", args=[slug])
        response = self.client.post(
            url,
            {
                "name": "Peter",
                "body": "I have to try this",
                "active": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(Comment.objects.last().name, "Peter")
        # self.assertEqual(Comment.objects.last().body, "I have to try this")
