from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Profile
from django.http import JsonResponse




from chat.models import Thread
# Create your views here.


@login_required
def messages_page(request):
    # Fetch threads associated with the logged-in user
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    
    # Fetch the profile of the logged-in user
    user_profile = Profile.objects.get(user=request.user)
    
    # Define 'thread' based on some condition or logic
    # For example, if you want to select the first thread from the queryset
    if threads:
        thread = threads[0]  # Assuming you want to select the first thread
    else:
        thread = None  # If no threads are found
    
    # Fetch the profile of the second person in the thread
    if thread:
        if request.user == thread.first_person:
            second_person_profile = Profile.objects.get(user=thread.second_person)
        else:
            second_person_profile = Profile.objects.get(user=thread.first_person)
    else:
        second_person_profile = None
    
    context = {
        'Threads': threads,
        'user_profile': user_profile,
        'second_person_profile': second_person_profile,  # Add the profile of the second person to the context
        
    }
    return render(request, 'messages.html', context)

def index(request):
    return render(request, 'index.html')



def create_thread_api(request):
    if request.method == 'POST':
        # Assuming you're passing the other user's ID via POST request
        second_person_id = request.POST.get('second_person_id')
        
        # Check if the thread between the current user and second person already exists
        thread_exists = Thread.objects.filter(
            first_person=request.user,
            second_person_id=second_person_id
        ).exists()
        
        if not thread_exists:
            # If the thread doesn't exist, create a new one
            thread = Thread.objects.create(
                first_person=request.user,
                second_person_id=second_person_id
            )
            # Redirect to the messages page
            return redirect('messages')
        else:
            # Thread already exists, return a JSON response indicating the same
            # return JsonResponse({'message': 'Thread already exists.'}, status=400)
            return redirect('messages')
    else:
        # Handle GET requests
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    


