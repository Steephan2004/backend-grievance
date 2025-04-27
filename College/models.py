from django.db import models

class Login(models.Model):
    WhoAreYou = models.CharField(max_length=30)
    Department = models.CharField(max_length=30)
    MobileNumber = models.PositiveIntegerField(default=1234567890)

    def __str__(self):
        return f"{self.WhoAreYou} from {self.Department}"

class GuestLogin(models.Model):
    Name = models.CharField(max_length=50)
    MobileNumber = models.PositiveIntegerField()

    def __str__(self):
        return self.Name

class AdminLogin(models.Model):
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=20)
    Date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.UserName

class QueryForm(models.Model):
    Name = models.CharField(max_length=50)
    MobileNumber = models.PositiveIntegerField()
    Department = models.CharField(max_length=30)
    Date = models.DateField(auto_now_add=True, null=True)
    Venue = models.CharField(max_length=20)
    Floor = models.CharField(max_length=20)
    RoomNo = models.CharField(max_length=20)
    Complaint = models.CharField(max_length=200)
    Status = models.CharField(max_length=15, default='NOT SEEN YET')
    Remark=models.CharField(max_length=200,default='-')

    def __str__(self):
        return f"{self.Venue} - Room {self.RoomNo}"
    
