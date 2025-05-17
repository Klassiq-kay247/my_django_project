from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from shortuuid.django_fields import ShortUUIDField
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField


STATUS = (
	("draft", "Draft"),
	("disabled", "Disabled"),
	("rejected", "Rejected"),
	("in_review", "In Review"),
	("published", "Published"),
)

class Category(models.Model):
	cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat', alphabet='abcdefgh12345')
	title = models.CharField(max_length=100, default="Category Name")

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.title

class Post(models.Model):
	pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet='abcdefgh12345')

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	categories = models.ManyToManyField(Category, related_name="categories")

	tags = TaggableManager(blank=True)

	image = models.ImageField(upload_to='blog', default="blog.jpg")
	title = models.CharField(max_length=100, default="Post Name")
	subtitle = models.TextField(null=True, blank=True, default="Post Subtitle")
	
	body = RichTextUploadingField(null=True, blank=True, default="Post Body")

	post_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'Posts'

	def blog_image(self):
		return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

	def __str__(self):
		return self.title

class PostImages(models.Model):
	images = models.ImageField(upload_to="post-images", default="post.jpg")
	post = models.ForeignKey(Post, related_name="p_images", on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Post Images'
  
class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = CloudinaryField(
        'video',
        resource_type='video',
        folder='gallery_videos/',
        allowed_formats=['mp4', 'webm', 'mov'],
        transformation={
            'quality': 'auto',
            'fetch_format': 'auto'
        }
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Post Videos'
		
 
class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	body = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Comments'

	def __str__(self):
		return self.post.title

class ContactUs(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	message = models.TextField()

	class Meta:
		verbose_name = 'Contact Us'
		verbose_name_plural = 'Contact Us'

	def __str__(self):
		return self.name

class ArtistBio(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(null=True, blank=True, default="Product Description")
    images = models.ImageField(upload_to='artist_bio_images/', null=True, blank=True)

class Resume(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(null=True, blank=True, default="Product Description")
    images = models.ImageField(upload_to='resume_images/', null=True, blank=True)

class ArtistStatement(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(null=True, blank=True, default="Product Description")
    images = models.ImageField(upload_to='artist_statement_images/', null=True, blank=True)

class ArtistPortfolio(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField(null=True, blank=True, default="Product Description")
    images = models.ImageField(upload_to='artist_portfolio_images/', null=True, blank=True)
    
    
# Add this new model after the existing imports
class FooterGalleryImage(models.Model):
    footer = models.ForeignKey('Footer', related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='footer/gallery', default='testimony.jpg')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"Footer Gallery Image {self.id}"

# Update the Footer model
class Footer(models.Model):
    heading = models.CharField(max_length=500, default='text1')
    logo = models.ImageField(upload_to='footer/logo/', default='logo.png', help_text="Upload your logo")
    company_name = models.CharField(max_length=200, default='Your Company Name')
    about_text = models.TextField(help_text="Short description about your company")
    # Contact Info
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Social Media Links
    facebook = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    # Business Hours
    business_hours = models.TextField(help_text="Enter your business hours", blank=True, null=True)
    
    # Copyright
    copyright_text = models.CharField(max_length=500, default='© 2025. All Rights Reserved.')
    
    # Newsletter
    newsletter_text = models.CharField(max_length=500, default='Subscribe to our newsletter')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer Settings'
    
    
class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery')
    date_created = models.DateTimeField(auto_now_add=True)
    
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='gallery_likes', blank=True)
    
    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['-date_created']
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
