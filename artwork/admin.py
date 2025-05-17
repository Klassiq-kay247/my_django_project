from django.contrib import admin
from artwork.models import Post, Category, Comment, Footer, FooterGalleryImage, PostImages, Gallery, ArtistBio, Footer, Resume, ArtistStatement, ArtistPortfolio, PostVideo

class PostVideoAdmin(admin.TabularInline):
    model = PostVideo
    extra = 1
    max_num = 3  # Limit number of videos
    classes = ['collapse']  # Makes the video section collapsible
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs[:3]  # Limit query to 3 videos

class PostImagesAdmin(admin.TabularInline):
	model = PostImages

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImagesAdmin, PostVideoAdmin]
    list_display = ['title', 'blog_image', 'pid']

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'cid']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'post']
 
 
@admin.register(ArtistBio)
class ArtistBioAdmin(admin.ModelAdmin):
    list_display = ['title']  # Customize the displayed fields as needed

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title']  # Customize the displayed fields as needed

@admin.register(ArtistStatement)
class ArtistStatementAdmin(admin.ModelAdmin):
    list_display = ['title']  # Customize the displayed fields as needed

@admin.register(ArtistPortfolio)
class ArtistPortfolioAdmin(admin.ModelAdmin):
    list_display = ['title']  # Customize the displayed fields as needed
    
    
class FooterGalleryImageInline(admin.TabularInline):
    model = FooterGalleryImage
    extra = 1
    max_num = 6

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    inlines = [FooterGalleryImageInline]
    fieldsets = (
        ('Logo & Company Info', {
            'fields': (
                'logo',
                'company_name',
                'about_text',
            )
        }),
        ('Contact Information', {
            'fields': (
                'address',
                'email',
                'phone',
            )
        }),
        ('Social Media', {
            'fields': (
                'facebook',
                'twitter',
                'instagram',
                'youtube',
            )
        }),
        ('Business Hours & Copyright', {
            'fields': (
                'business_hours',
                'copyright_text',
            )
        }),
    )

    def has_add_permission(self, request):
        # Check if footer already exists
        if Footer.objects.exists():
            return False
        return True
    

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(Gallery)

