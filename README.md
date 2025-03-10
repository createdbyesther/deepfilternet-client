# deepfilternet-client

### Prerequisite
* The DeepFilterNet/Lambda container from [github] must be running in advance.
* Start Python3 virtual environment

### Installation
Install all the requirements:
```
pip install -r requirements.txt
```

Now you are ready to go.

### Basic Usage
Currently, the `client.py` file will take a noisy example audio file (examples/noisy_snr0.wav) by default, and send this file to the DeepFilterNet/Lambda container for audio enhancement.

Once completed, the container will return the file and save it in the current directory as `noisy_snr0_enhance.wav`.

Run the following:
```
python client.py
```
### API Call
In order to perform a POST request with `audio_file` as an input, you can run the following curl command:
```
curl -X POST -F "audio_file=@/ABSOLUTE/FILE/PATH/TO/AUDIO_FILE" http://localhost:8000/audio/process_audio/
```
This should save the audio file from the server.