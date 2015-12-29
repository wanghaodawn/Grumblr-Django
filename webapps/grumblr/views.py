from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.urlresolvers import reverse 

#Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse,Http404

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

#Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Used to send mail from within Django
from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator

from grumblr.models import *
from grumblr.forms import *

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import activate
from django.utils.timezone import localtime

#############################################################
# Add post - The Global Stream Page
#############################################################
@ensure_csrf_cookie
@login_required
def add_post(request):
	context={}
	posts = Post.objects.all().order_by('-date')
	context['posts'] = posts

	form = PostForm(request.POST)
	context['form'] = form
	
	if not form.is_valid():
		return render(request,'global_page.html',context)

	new_post = Post(text = form.cleaned_data['text'], user=request.user)
	new_post.save()
	log_entry = LogEntry(post = new_post)
	log_entry.save()

	context['form'] = PostForm()
	return redirect(reverse('global'))

@login_required
# Returns all recent additions in the database, as JSON
def get_posts(request, log_id = -1):
	max_logentry = LogEntry.get_max_id()
	posts = Post.get_posts(log_id).order_by("-date")
	context = {"max_entry":max_logentry, "posts":posts}
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
# Returns all recent changes to the database, as JSON
def get_changes(request, log_id=-1):
	max_logentry = LogEntry.get_max_id()
	posts = Post.get_changes(log_id).order_by("-date")
	context = {"max_entry":max_logentry, "posts":posts} 
	return render(request, 'posts.json', context, content_type='application/json')

@login_required
def add_comment(request, post_id):
	print("begin add_comment")
	if not 'comment' in request.POST or not request.POST['comment']:
		print("false")
		raise Http404
	else:
		print("true")
		new_comment = Comment(text = request.POST['comment'], \
			post_owner = Post.objects.get(id = post_id), comment_owner = request.user)
		new_comment.save()

	comments = Comment.objects.all().order_by('-date')
	posts = Post.objects.get(id = post_id)
	context = {"comments": comments, "posts": posts}
	print(context)
	return render(request, 'comments.json', context, content_type = 'application/json')

#############################################################
# Implemented the login_page
#############################################################
def login_page(request):
	context = {}

	if 'signup' in request.POST:
		return render(request,'signup_page.html',context)

	# GET is not safe enough now
	if request.method == "GET":
		context['form'] = SignupForm()
		return render(request,'login_page.html',context)
	"""
	errors = []
	context['errors'] = errors

	# Username
	if not 'username' in request.POST or not request.POST['username']:
		errors.append('Username is required.')
	else:
		context['username'] = request.POST['username']

	# Password
	if not 'password' in request.POST or not request.POST['password']:
		errors.append('Password is required')
	else:
		context['password'] = request.POST['password']

	# Whether there are errors
	if errors:
		return render(request, 'login_page.html', context)
	"""
	# Creates a bound form from the request POST parameters and makes the 
  # form available in the request context dictionary.
	form = SignupForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'login_page.html', context)

	user = authenticate(username = form.cleaned_data['username'],
											password = form.cleaned_data['password'])
	
	"""
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('global_page.html')
	errors.append('This Account does not exist')
	"""
	redirect(reverse('global'))

	#return render(request, 'login_page.html', context)

#############################################################
# Implemented the signup_page
#############################################################
def signup_page(request):
	context = {}

	# Just display the registration form if this is a GET request.
	if request.method == "GET":
		context['form'] = SignupForm()
		return render(request,'signup_page.html',context)
	
	"""	
	errors = []
	context['errors'] = errors

	# Username
	if not 'username' in request.POST or not request.POST['username']:
		errors.append('Username is required.')
	else:
		context['username'] = request.POST['username']

	# Firstname
	if not 'firstname' in request.POST or not request.POST['firstname']:
		errors.append('Firstname is required')
	else:
		context['firstname'] = request.POST['firstname']

	# Lastname
	if not 'lastname' in request.POST or not request.POST['lastname']:
		errors.append('Lastname is required')
	else:
		context['lastname'] = request.POST['lastname']

	# Password
	if not 'password1' in request.POST or not request.POST['password1']:
		errors.append('Password is required.')
	if not 'password2' in request.POST or not request.POST['password2']:
		errors.append('Confirm password is required.')
	if 'password1' in request.POST and 'password2' in request.POST \
		and request.POST['password1'] and request.POST['password2'] \
		and request.POST['password1'] != request.POST['password2']:

		errors.append('Passwords does not match.')
	else:
		context['password'] = request.POST['password1']

	# Whether the username has already been taken
	if len(User.objects.filter(username = request.POST['username']))>0:
		errors.append('Username is already taken.')

	# Whether there are errors
	if errors:
		return render(request, 'signup_page.html', context)
	"""

	# Creates a bound form from the request POST parameters and makes the 
  # form available in the request context dictionary.
	form = SignupForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'signup_page.html', context)

	# If we get here the form data was valid.  Register and login the user.
	new_user = User.objects.create_user(username = form.cleaned_data['username'],
																			password = form.cleaned_data['password1'])
	new_user.save()

	info = Info(owner = new_user,
							email = form.cleaned_data['email'],
							firstname = form.cleaned_data['firstname'],
							lastname = form.cleaned_data['lastname'])
	info.save()

	# Logs in the new user and redirects to his/her global page
	new_user = authenticate(username = form.cleaned_data['username'],
													password = form.cleaned_data['password1'])

	login(request, new_user)
	return redirect(reverse('global'))

#############################################################
# Implemented the profile_page
#############################################################

@login_required
def profile_page(request, id):
	user = User.objects.get(id = id)
	info = Info.objects.get(owner=user)
	posts = Post.objects.filter(user = user).order_by('-date')
	owner_info = Info.objects.get(owner = request.user)

	if len(owner_info.followers.filter(id = id)) > 0:
		follow_flag = True
	else: 
		follow_flag = False

	context = {'posts':posts, 'current_user':user, 'login_user':request.user, 'follow_flag':follow_flag, 'info':info}
	return render(request, 'profile_page.html', context)

@login_required
def profile(request):
	user = request.user
	posts = Post.objects.filter(user= request.user).order_by('-date')
	info = Info.objects.get(owner=request.user)
	context = {'posts':posts, 'info':info, 'current_user':user,'login_user':user}		
	return render(request, 'profile_page.html', context)

@login_required
def upload_photo(request, id):
	user = get_object_or_404(User, id = id)
	info = get_object_or_404(Info, owner = user)

	if not info.photo:
		raise Http404

	content_type = guess_type(info.photo.name)
	return HttpResponse(info.photo, content_type = content_type)

@login_required
def edit_page(request):
	edit_profile = get_object_or_404(Info, owner = request.user)

	if request.method == "GET":
		form = InfoForm(instance = edit_profile)
		context = {'form': form}
		return render(request, 'edit_page.html', context)

	form = InfoForm(request.POST, request._files, instance = edit_profile)

	if not form.is_valid():
		context = {'form': form}
		return render(request, 'edit_page.html', context)

	form.save()

	return redirect(reverse('profile'))

@login_required
def follow_page(request):
	info = Info.objects.get(owner = request.user)
	follower = info.followers.all()
	posts = Post.objects.filter(user = follower).order_by('-date')
		
	context = {'info':info,'posts':posts}
	return render(request,'follow_page.html',context)

@login_required
def follow(request,id):
	other_user = User.objects.get(id = id)
	info = Info.objects.get(owner = request.user)
	info.followers.add(other_user)
	info.save()
		
	path = "/profile-page/"+str(id)
	return redirect(path)

@login_required
def unfollow(request,id):
	info = Info.objects.get(owner = request.user)
	info.followers.remove(User.objects.get(id = id))
	info.save()
	path = "/profile-page/"+ str(id)
	return redirect(path)

@login_required
def reset_password(request):
	if request.method == 'GET':
		form = PasswordResetForm()
		return render(request,'login_reset_password.html',{'form':form})

	form = PasswordResetForm(request.POST)
	if not form.is_valid():
		return render(request,'login_reset_password.html',{'form':form})

	user = request.user
	password = form.cleaned_data['password1']
	user.set_password(password)
	user.save()
	
	return redirect(reverse('profile'))

def change_password(request):
	context = {}

	if request.method == "GET":
		form = PasswordChangeForm()
		return render(request,'change_password.html', {'form':form})

	form = PasswordChangeForm(request.POST)

	if not form.is_valid():
		return render(request,'change_password.html', {'form':form})

	username = form.cleaned_data['username']
	user = User.objects.get(username= username)
	token = default_token_generator.make_token(user)

	email_body = """
	This email is used to reset your password.
	
	http://%s%s

	"""%(request.get_host(), reverse('email_sent', args=(token, username)))

	send_mail(subject = 'Password to be change',
						message = email_body,
						from_email = 'wanghaodawn@cmu.edu',
						recipient_list = [user.email])

	return render(request, 'email_sent.html',context)

def email_sent (request,username,token):
	user = get_object_or_404(User,username = username)
	if not default_token_generator.check_token(user,token):
		raise Http404

	if request.method == "GET":
		form = PasswordResetForm()
		return render(request,'reset_password.html',{'token':token,'username':username,'form':form})

	form = PasswordResetForm(request.POST)

	if not form.is_valid():
		return render(request,'reset_password.html',{'token':token,'username':username,'form':form})

	password = form.cleaned_data['password1']
	user.set_password(password)
	user.save()
		
	return redirect(reverse('profile'))

