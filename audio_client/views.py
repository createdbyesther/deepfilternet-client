import os
import base64
import requests
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from pathlib import Path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def say_hello(request):
    print('hello')

    if 'audio_file' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)


    audio_file = request.FILES['audio_file']
    print(audio_file)

    return render(request, 'hello.html', {'name': 'Mosh'})

@api_view(['POST'])
def enhance_audio(request):
    # Define the API endpoint
    API_URL = 'http://localhost:9000/2015-03-31/functions/function/invocations'

    if 'audio_file' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    # Path to the local .wav file you want to send
    input_audio_file = request.FILES.get('audio_file')

    # Get only the file name without the extension
    audio_file_path, _ = os.path.splitext(input_audio_file.name)

    #  Encode the audio data to base64
    encoded_audio = base64.b64encode(input_audio_file.read()).decode('utf-8')

    # Create the payload as a JSON dictionary
    payload = {
        'body': encoded_audio,
        'isBase64Encoded': True,  # Indicate that the body is base64-encoded
        'audio_filename': audio_file_path
    }    

    # Send the POST request with the base64-encoded audio in the body
    response = requests.post(API_URL, json=payload)

    # Check if the response was successful (status code 200)
    if response.status_code == 200 and response.json().get('isBase64Encoded', False):

        # Get the base64-encoded audio data from the response
        base64_audio = response.json()['body']
        
        # Decode the base64 data to binary
        audio_data = base64.b64decode(base64_audio)

        # Save the decoded audio to a local file
        with open(f'{audio_file_path}_enhanced.wav', 'wb') as f:
            f.write(audio_data)
        
        return Response(f"Audio processing is complete! File saved as {audio_file_path}_enhanced.wav", content_type='text/plain', status=status.HTTP_200_OK)

    else:
        # print(f"Error: {response.status_code}, {response.text}")
        print(f"Failed to process the audio. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return Response({"error": "Processed file not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)