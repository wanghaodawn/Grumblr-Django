# User class for built-in authentication module
from django.contrib.auth.models import User

from django import forms
from models import *

class SignupForm(forms.Form):
	username = forms.CharField(max_length = 20, 
															widget = forms.TextInput(attrs={'class':'form.control'}))
	password1 = forms.CharField(max_length = 200,
															label = 'Password',
															widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 200,
															label = 'Confirm Password',
															widget = forms.PasswordInput())
	firstname = forms.CharField(max_length = 20, 
															widget = forms.TextInput(attrs={'class':'form.control'}))
	lastname = forms.CharField(max_length = 20, 
															widget = forms.TextInput(attrs={'class':'form.control'}))
	email = forms.EmailField(max_length = 20, 
															widget = forms.TextInput(attrs={'class':'form.control'}))

	# Customizes form validation for properties that apply to more
  # than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
    # of cleaned data as a result
		cleaned_data = super(SignupForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password Did Not Match!")

		# We must return the cleaned data we got from our parent.
		return cleaned_data

	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact = username):
			raise forms.ValidationError("Username is already taken!")

		# We must return the cleaned data we got from the cleaned_data
    # dictionary
		return username


class InfoForm(forms.ModelForm):
	class Meta:
		model = Info
		exclude = ('owner', 'followers', 'email')
		widgets = {'photo': forms.FileInput()}


class PasswordChangeForm(forms.Form):
		username = forms.CharField(max_length = 20)

		def clean(self):
				cleaned_data = super(PasswordChangeForm,self).clean()
				if not User.objects.filter(username = cleaned_data.get('username')):
						raise forms.ValidationError("user does not exist")
				return cleaned_data


class PasswordResetForm(forms.Form):
		password1 = forms.CharField(max_length = 200, label = 'Password', widget = forms.PasswordInput())
		password2 = forms.CharField(max_length = 200, label = 'Confirm password', widget = forms.PasswordInput())

		def clean(self):
				cleaned_data = super(PasswordResetForm,self).clean()
				password1 = cleaned_data.get('password1')
				password2 = cleaned_data.get('password2')
				if password1 and password2 and password1 != password2:
						raise forms.ValidationError("Password did not match.")
				return cleaned_data


class PostForm(forms.ModelForm):
		class Meta:
				model = Post
				fields = ('text',)


class CommentForm(forms.ModelForm):
		class Meta:
				model = Comment
				fields = ('text',)



