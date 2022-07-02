from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, JsonResponse

from .models import Voter, ColorTeam
from .forms import EmailForm

def index(request):
    form = EmailForm()
    return render(request, 'index.html', {'form': form})


def vote(request):
    form = EmailForm()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid(): 
            rawemail = form.cleaned_data['email']
            # handling if email is already in session data
            if 'user_email' in request.session:
                voter = Voter.objects.get(email=request.session['user_email'])
                if voter.choice == ColorTeam.objects.get(name="Filler"):
                    if request.session['user_email']==rawemail:
                        messages.success(request, 'You may now vote! May the best team win!')                        
                        return render(request, 'votefr.html', {'user': voter, 'success': True})
                    else:
                        request.session['user_email'] = rawemail
                        messages.success(request, 'You may now vote! May the best team win!')
                        return render(request, 'votefr.html', {'user': voter, 'success': True})
                else:
                    messages.error(request, 'An error occured! Make sure you are not entering an email that has already been used to vote.')
                    return HttpResponseRedirect(request.META["HTTP_REFERER"]) 
            else:
                if Voter.objects.filter(email=rawemail).exists():
                    print("new user has voted")
                    messages.error(request, 'An error occured! Make sure you are not entering an email that has already been used to vote.')
                    return HttpResponseRedirect(request.META["HTTP_REFERER"])
                else:
                    fillerteam = ColorTeam.objects.get(name="Filler")
                    newvoter = Voter.objects.create(email=rawemail, choice=fillerteam)
                    request.session['user_email'] = rawemail
                    print("all good")
                    messages.success(request, 'You may now vote! May the best team win!')
                    return render(request, 'votefr.html', {'user': newvoter, 'success': True})

    if 'user_email' not in request.session:
        messages.error(request, 'An error occured! You must enter a valid email to continue.')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    print("there was no post")
    return index(request)

def submit(request):
    form = EmailForm()
    if request.method == 'POST':
        if 'user_email' not in request.session:
            messages.error(request, 'An error occured! You must enter a valid email to continue.')
            return index(request)
        else:
            if request.POST.get('action') == 'post':
                team = request.POST.get('team')
                print("got the team", team)
            if "Blue" in team:
                fetchedteam = ColorTeam.objects.get(name="Blue")
            else:
                fetchedteam = ColorTeam.objects.get(name="Red")
            fetchedteam.increaseVotes()
            print(fetchedteam.votes)
            try:
                user = Voter.objects.get(email=request.session['user_email'])
            except:
                raise Http404
            user.choice = fetchedteam
            del request.session['user_email']
            response = JsonResponse({'success': "ok"})
            return response

def complete(request):
    redvotes = ColorTeam.objects.get(name="Red").votes
    bluevotes = ColorTeam.objects.get(name="Blue").votes
    undecided = ColorTeam.objects.get(name="Filler").votes
    return render(request, 'checkstats.html', {'redvotes': redvotes, 'bluevotes': bluevotes, 'undecided': undecided})