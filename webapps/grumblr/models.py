from django.db import models
# User class for built-in authentication module
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max



class Post(models.Model):
	text = models.CharField(max_length = 200)
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add = True, blank = True)

	def __unicode__(self):
		return self.text

	# Returns all recent additions and deletions to the to-do list.
	@staticmethod
	def get_changes(logentry_id = -1):
		return Post.objects.filter(logentry__gt = logentry_id).distinct()

	# Returns all recent additions to the to-do list.
	@staticmethod
	def get_posts(logentry_id = -1):
		return Post.objects.filter(logentry__gt = logentry_id).distinct()

	# Generates the HTML-representation of a post
	@property
	def html(self):
		result  = "<a href='profile-page/%d'>" % (self.user.id)
		result += "<img src='photo/%d' height='100px'> </a>" % (self.user.id)
		result += "<div class='p2'>%s %s %s</div><br />" % (self.text, self.date.strftime('%m/%d/%y %H:%M:%S'), self.user)
		result += "<ol id = 'comment_list_%d' ></ol>" % (self.id)
		result += "<div class = 'p2'><input id='comment_field_%d' type='text'>" % (self.id)
		result += "<button id ='add_comment_button' btn-id= %d >add comment</button></div>" % (self.id)
		result += "<br /><br />"
		return result
		
	@property
	def get_comments(self):
		return Comment.objects.filter(post_owner = self.user)



class Info(models.Model):
	owner = models.OneToOneField(User)
	firstname = models.CharField(max_length = 20, default = "", blank = True)
	lastname = models.CharField(max_length = 20, default = "", blank = True)
	age = models.CharField(max_length = 3, default = "", blank = True)
	bio = models.CharField(max_length = 420, default = "", blank = True)
	email = models.EmailField(max_length = 20, default = "", blank = True)
	photo = models.ImageField(upload_to = "photo", blank = True)

	followers = models.ManyToManyField(User, related_name = "followers")

	def __unicode__(self):
		return self.first_name

	@staticmethod
	def get_infos(user):
		return Info.objects.get(user = user)
		


# A LogEntry implicitly records when a psot is added and deleted, though its auto-increment id.
class LogEntry(models.Model):
	post = models.ForeignKey(Post)
	
	def __unicode__(self):
		return "LogEntry (%d, %s)" % (self.id, self.post)
	def __str__(self):
		return self.__unicode__()

	# Gets the id of the most recent LogEntry
	@staticmethod
	def get_max_id():
		return LogEntry.objects.all().aggregate(Max('id'))['id__max'] or 0



class Comment(models.Model):
	text = models.CharField(max_length = 100)
	post_owner = models.ForeignKey(Post)
	comment_owner = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add = True, blank = True)

	def __unicode__(self):
		return self.text

	# Generates the HTML-representation of a post
	@property
	def html(self):
		result  = "<a href='profile-page/%d'>" % (self.comment_owner.id)
		result += "<img src='photo/%d' height='100px'> </a>" % (self.comment_owner.id)
		result += "<div class='p2'>%s %s %s</div><br />" \
		  % (self.text, self.date.strftime('%m/%d/%y %H:%M:%S'), self.comment_owner)
		return result



