from django.shortcuts import render
from django.http import JsonResponse
from artwork.models import Gallery, Post, Footer, FooterGalleryImage, Comment, Category, ContactUs, ArtistBio, Resume, ArtistStatement, ArtistPortfolio
from artwork.forms import CommentFrom
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def blog_view(request):
    posts = Post.objects.filter(post_status='published').order_by("-date_created")

    # Create a Paginator object
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    # Get the page number from the GET parameters (default to 1 if not present)
    page_number = request.GET.get('page', 1)
    
    try:
        # Fetch the correct page
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page number is not an integer, return the first page
        page = paginator.page(1)
    except EmptyPage:
        # If the page number is out of range, return the last page
        page = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "posts": posts,
    }
    
    return render(request, 'artwork/artwork.html', context)

def blog_category_view(request, cid):
	category = Category.objects.get(cid=cid)
	posts = Post.objects.filter(
		post_status='published', categories=category
	).order_by("-date_created")

	context = {
		"category": category,
		"posts": posts,
	}
	return render(request, "artwork/category.html", context)

def blog_detail_view(request, pid):
	post = Post.objects.get(pid=pid)
	posts = Post.objects.filter(categories__in=post.categories.all()).exclude(pid=pid).distinct()
	comments = Comment.objects.filter(post=post).order_by('-date_created')

	comment_form = CommentFrom()

	make_comment = True
	if request.user.is_authenticated:
		user_comment_count = Comment.objects.filter(
			user=request.user, 
			post=post
		).count() 

		if user_comment_count > 0:
			make_comment = False
	p_image = post.p_images.all()  # Fetching all images related to the post
	p_videos = post.p_videos.all()
	
	media_dimensions = {
        'thumbnail': {
            'width': '300px',
            'height': '200px',  # Changed to rectangular format
        },
        'video': {
            'width': '100%',
            'max-height': '480px',
        }
    }
 	
	context = {
		"post": post,
		"comments": comments,
		"comment_form": comment_form,
		"make_comment": make_comment,
		"posts": posts,
  		"p_image": p_image,  # Adding post images to the context
    	"p_videos": p_videos,
		"media_dimensions": media_dimensions,
	}
	return render(request, 'artwork/artwork-detail.html', context)

def blog_tags(request, tag_slug=None):
	posts = Post.objects.filter(post_status='published').order_by('-id')

	tag = None
	if tag_slug:
		tag = Tag.objects.get(slug=tag_slug)
		posts = posts.filter(tags__in=[tag])

	context = {
		'posts': posts,
		'tag': tag,
	}
	return render(request, 'artwork/tag.html', context)

def ajax_add_comment(request, pid):
	post = Post.objects.get(pk=pid)
	user = request.user
	image = user.image.url

	comment = Comment.objects.create(
		user=user,
		post=post,
		body=request.POST['comment'],
	)
	
	context = {
		'user': user.username,
		'comment': request.POST['comment'],
		'image': image
	}
	return JsonResponse(
		{
			'bool': True,
			'context': context,
		}
	)
 
 
def contact(request):
	return render(request, 'artwork/contact.html')

def ajax_contact_form(request):
	name = request.GET['name']
	email = request.GET['email']
	message = request.GET['message']

	contact = ContactUs.objects.create(
		name=name,		
		email=email,		
		message=message,		
	)

	data = {
		'bool': True,
	}

	return JsonResponse({'data': data})


def artist_bio(request):
    bios = ArtistBio.objects.all()
    return render(request, 'artwork/artist_bio.html', {'bios': bios})

def resume(request):
    resumes = Resume.objects.all()
    return render(request, 'artwork/resume.html', {'resumes': resumes})

def artist_statement(request):
    statements = ArtistStatement.objects.all()
    return render(request, 'artwork/artist_statement.html', {'statements': statements})

def artist_portfolio(request):
    portfolios = ArtistPortfolio.objects.all()
    return render(request, 'artwork/artist_portfolio.html', {'portfolios': portfolios})


# Add this context processor
def footer_context(request):
    try:
        footer = Footer.objects.first()
        footer_images = FooterGalleryImage.objects.all()[:6]  # Get first 6 images
        return {
            'footer': footer,
            'footer_images': footer_images
        }
    except:
        return {}

# Update your existing views to include footer context
def gallery_view(request):
    galleries = Gallery.objects.all()
    footer_data = footer_context(request)
    context = {
        'galleries': galleries,
        **footer_data
    }
    return render(request, 'artwork/gallery.html', context)



