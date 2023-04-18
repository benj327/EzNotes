# EzNotes

Using this application, users can upload an mp3 file of a lecture or meeting and have it summarized for them in a txt file using a multithreaded server and the OpenAI API.

## Installation

Requires npm and python3

`git clone https://github.com/benj327/EzNotes.git`

`cd Backend`

`python3 server.py`

`cd ../`

`npm start`

## Front End

EzNotes uses a fairly simple React front end to take the user file and return the txt file. It's a very minimalistic design in order to keep things functional while still looking modern.

## Backend

EzNotes runs a Flask server to handle requests. The backend splits an mp3 file into parts large enough for the Whisper API to accept(25 MB max) using a thread for each request. It then takes the response and recombines it, before splitting the transcription into groups of 20 sentences to be summarized with a GPT3.5 prompt, which also uses a thread for each request. These responses are then put into a text document, which can be downloaded by the user.

## Example

You can check out a sample output from a [51 minute MIT Lecture on dynamic programming](https://www.youtube.com/watch?v=OQ5jsbhAv_M) in the Backend/output.txt file. There is also a sample demo available on [YouTube](https://www.youtube.com/watch?v=nUtlPEr-Dp0)
