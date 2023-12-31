from django.http import JsonResponse
import requests
import os
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from . import models
from django.shortcuts import render
from django.apps import apps

from .models import Profile


@login_required
def update_location(request):
    try:
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User details")

        point = request.POST["point"].split(",")
        description = request.POST["description"]
        lon_lat = [float(part) for part in point]
        lon, lat = lon_lat
        map_point = Point(lon_lat, srid=4326)

        user_profile.lon = lon
        user_profile.lat = lat
        user_profile.location = map_point
        user_profile.description = f"{description}"
        user_profile.save()
        return JsonResponse({"message": f"Set location to lat: {lat}, lon: {lon}."}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

@login_required
def map_view(request):
    user_profile = Profile.objects.get(user=request.user)
    fishingmark_model = apps.get_model("userlocation", "Fishingmark")
    fishingmarks = fishingmark_model.objects.all()
    return render(request, "map.html", {"fishingmarks": fishingmarks, "favourite_mark": user_profile.description, "last_updated": user_profile.last_updated})


def chatbot_response(request):
    try:
        user_message = request.GET.get('message')
        user_location = request.GET.get('location')
        initial_prompt = f"You are a knowledgeable fishing assistant. Don't say I said that please. My location if relevant is {user_location}. Do not mention coordinates and only refer to this as my location."
        

        # Initialize conversation history if not present
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []

            # Append the initial prompt message to the conversation history
            request.session['chat_history'].append({'role': 'user', 'content': initial_prompt})

        
        api_key = os.getenv('OPENAI_API_KEY')  # Fetching API key from environment variables
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        
        
        # Append the new user message to the conversation history
        request.session['chat_history'].append({'role': 'user', 'content': user_message})

        data = {
            'model': 'gpt-4-1106-preview',
            'messages': request.session['chat_history'],
            'max_tokens': 300
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        
        if response.status_code != 200:
            return JsonResponse({'response': response.text}, status=500)

        response_data = response.json()
        choices = response_data.get('choices')
        if not choices or not choices[0]:
            return JsonResponse({'response': 'Invalid response from GPT-4 API'}, status=500)

        message_content = choices[0].get('message')
        if not message_content:
            return JsonResponse({'response': 'Missing message content from GPT-4 API response'}, status=500)

        bot_response = message_content.get('content', '').strip() 
        request.session['chat_history'].append({'role': 'assistant', 'content': bot_response})

        # Save the updated conversation history to the session
        request.session.modified = True

        return JsonResponse({'response': bot_response})
    
    except Exception as e:
        # Log the exception (consider using logging library)
        print("Error: ", str(e))
        return JsonResponse({'response': 'An error occurred'}, status=500)


