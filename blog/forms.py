from django import forms
from .models import Blog, Comment
from accounts.models import Author
from django.core.exceptions import ValidationError

class BlogForm(forms.ModelForm):
  title = forms.CharField(
    max_length=200,
    required=True,
    error_messages={'required': 'Title is required'},
    widget=forms.TextInput(attrs={'class': 'form-control'})
  )

  content = forms.CharField(
    required=True,
    widget=forms.Textarea(attrs={'class': 'form-control'}),
    error_messages={'required': 'Content cannot be empty'}
  )

  image = forms.ImageField(
    required=True,
    widget=forms.FileInput(attrs={'class': 'form-control'}),
    error_messages={'required': 'Image cannot be empty'}
  )

  author = forms.ModelChoiceField(
    queryset=Author.objects.all(),
    required=True,
    widget=forms.Select(attrs={'class': 'form-control'}),
    error_messages={'required': 'Author is required'}
  )

  class Meta:
    model = Blog
    fields = ['title', 'content', 'image', 'author']


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['title'].widget.attrs.update({'placeholder': 'Blog Title'})
    self.fields['content'].widget.attrs.update({'placeholder': 'Blog Content'})
    self.fields['image'].widget.attrs.update({'class': 'form-control'})


  def clean_title(self):
    title = self.cleaned_data.get('title')

    if len(title) > 200:
      raise ValidationError('Title must not exceed 200 characters.')

    return title


  def clean_content(self):
    content = self.cleaned_data.get('content')

    if not content or content.strip() == '':
      raise ValidationError('Content cannot be empty.')

    return content


  def clean_image(self):
    image = self.cleaned_data.get('image')

    if image:
      valid_extensions = ['jpg', 'jpeg', 'png']
      file_extension = image.name.split('.')[-1].lower()

      if file_extension not in valid_extensions:
        raise ValidationError('Unsupported file extension. Use JPG, JPEG, or PNG.')

      if image.size > 10 * 1024 * 1024:
        raise ValidationError('The image is too large. Please upload an image smaller than 10MB.')

    return image
  
  
class CommentForm(forms.ModelForm):

  message = forms.CharField(
    max_length=200,
    required=True,
    error_messages={'required': "Message can't be empty"},
    widget=forms.Textarea(attrs={'placeholder': 'Add your comment...'})
  )


  class Meta:
    model = Comment
    fields = ['message']