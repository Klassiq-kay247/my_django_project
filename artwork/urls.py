from django.urls import path
from artwork import views

app_name = 'artwork'

urlpatterns = [

	# Blogpage
	path('', views.blog_view, name='artwork'),

	# Post Details
	path('post/<pid>/', views.blog_detail_view, name='artwork-detail'),

	# Blog Category
	path('category/<cid>/', views.blog_category_view, name="artwork-category"),

	# Blog Tags
	path('tag/<slug:tag_slug>/', views.blog_tags, name='artwork-tag'),

	# Add Post Comment
	path('ajax-add-comment/<int:pid>/', views.ajax_add_comment, name='ajax-add-comment'),
 
	path('contact/', views.contact, name='contact'),

	# Ajax Contact From
	path('ajax-contact-form/', views.ajax_contact_form, name='ajax-contact-form'),
 
	path('artist_bio/', views.artist_bio, name='artist_bio'),
    path('resume/', views.resume, name='resume'),
    path('artist_statement/', views.artist_statement, name='artist_statement'),
    path('artist_portfolio/', views.artist_portfolio, name='artist_portfolio'),
    path('gallery/', views.gallery_view, name='gallery'),
	
]