from pathlib import Path
import requests
import base64


def main():
    # Define the API endpoint
    api_url = 'http://localhost:9000/2015-03-31/functions/function/invocations'

    # Path to the local .wav file you want to send
    audio_file_path = Path(__file__).parent / 'examples' / 'noisy_snr0.wav'

    # Read the audio file and encode it to base64
    with open(audio_file_path, 'rb') as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')

    # Create the payload as a JSON dictionary
    payload = {
        'body': encoded_audio,
        'isBase64Encoded': True,  # Indicate that the body is base64-encoded
        'audio_filename': audio_file_path.stem
    }
    

    # Send the POST request with the base64-encoded audio in the body
    response = requests.post(api_url, json=payload)

    # Check if the response was successful (status code 200)
    if response.status_code == 200 and response.json().get('isBase64Encoded', False):
        # Get the base64-encoded audio data from the response
        base64_audio = response.json()['body']
        
        # Decode the base64 data to binary
        audio_data = base64.b64decode(base64_audio)
        
        # Save the decoded audio to a file
        with open(f'{audio_file_path.stem}_enhanced.wav', 'wb') as f:
            f.write(audio_data)
        
        print(f'Enhanced audio file saved as "{audio_file_path.stem}_enhanced.wav"')
    else:
        # print(f"Error: {response.status_code}, {response.text}")
        print(f"Failed to process the audio. Status code: {response.status_code}")
        print(f"Response: {response.text}")

    print('done!')


if __name__=='__main__':
    main()