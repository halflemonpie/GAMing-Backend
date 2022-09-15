from django.db import models

# Create your models here.
class User(models.Model):
    photo_url = models.ImageField(upload_to='profile', default = 'please upload your profile image')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=50, default = 'Please input user name')
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    mentor = models.BooleanField(default=False)
    skills = []
    language = []
    connection = []
    request = []
    
    def __str__(self):
        return self.email

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'calendar')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'chat')
    participants = models.ManyToManyField(User, related_name='chats')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participants

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'message')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500) # what length you want

    def __str__(self):
        return self.text





