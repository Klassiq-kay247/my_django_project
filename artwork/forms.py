from django import forms
from artwork.models import Comment, PostVideo

class CommentFrom(forms.ModelForm):
	comment = forms.CharField(widget=forms.Textarea(attrs={
		'placeholder': 'Write comment', 
		'class': "form-control", 
		'id': "textAreaExample", 
		'rows': "4", 
		'style': "background: #fff;"}))

	class Meta:
		model = Comment
		fields = ['comment']
  
  
class PostVideoForm(forms.ModelForm):
    class Meta:
        model = PostVideo
        fields = ['video']

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError("Video file size must be under 50MB")
        return video