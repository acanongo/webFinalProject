from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User as auth_user

from . import models

class SuggestionForm(forms.Form):

    suggestionField = forms.CharField(
        label = "Suggestion:",
        max_length= 300,
    )

    image = forms.ImageField(
        label = "Image File",
        required= False
    )
    imageDescription = forms.CharField(label = "Image Description", max_length=244, required=False)

    def save(self,request):
        print("inside here")
        suggestionInstance = models.SuggestionModel()
        suggestionInstance.suggestionText = self.cleaned_data["suggestionField"]
        suggestionInstance.image = self.cleaned_data["image"]
        suggestionInstance.imageDescription = self.cleaned_data["imageDescription"]
        suggestionInstance.author = request.user
        suggestionInstance.save()

        return suggestionInstance

class CommentForm(forms.Form):

    commentField = forms.CharField(
        label = "Comment",
        max_length= 300,
    )

    def save(self,request, sugg_id):

        suggestion_instance = models.SuggestionModel.objects.get(id = sugg_id)

        commentInstance = models.CommentModel()
        commentInstance.commentText = self.cleaned_data["commentField"]
        commentInstance.author = request.user
        commentInstance.suggestion = suggestion_instance
        commentInstance.save()

        return commentInstance


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(

        label = "Email",
        required= True,
    )

    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user