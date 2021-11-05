# from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'test',
            email = 'test@test.com',
            password = 'secret'
        )
        self.post = Post.objects.create(
            title = "a title",
            body = "a body",
            author = self.user
        )

    def test_string_representation(self):
        post = Post (title = " a sameple title")
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "a title")
        self.assertEqual(f"{self.post.body}" "a body")
        self.assertEqual(f"{self.post.author}" "a test")

    def test_post_list_view(self):
        response = self.client.get("/")  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "body.html")
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_post_detail_view(self):
        response = self.client.get("/post/1/")
        no_response = self.client.get("/post/1000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "A Title")
        self.assertTemplateUsed(response, "post_detal.html")
        self.assertTemplateUsed(response, "base.html")

    def test_reverse_lookup(self):
        post_list_response = self.client.get(reverse("home"))
        post_detail_response = self.client.get(reverse("post_detail", args=["1"]))
        self.assertEqual(post_list_response.status_code, 200)
        self.assertEqual(post_detail_response.status_code, 200)
        self.assertContains(post_list_response, "A title")
        self.assertTemplateUsed(post_list_response,"home.html")
        self.assertContains(post_detail_response, "A title")
        self.assertTemplateUsed(post_detail_response,"post_detail.html")
