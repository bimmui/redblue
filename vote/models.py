from django.db import models


class ColorTeam(models.Model):
    name = models.CharField(max_length=254, blank=True)
    votes = models.IntegerField(default=0)

    def increaseVotes(self):
        self.votes+=1
        self.save()


class Voter(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    choice = models.ForeignKey(ColorTeam, on_delete=models.CASCADE)
