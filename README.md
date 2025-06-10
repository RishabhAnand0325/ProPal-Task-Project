# ProPal-Task-Project

Hello Sir,

My Name is Rishabh Anand and the above is my speech-to-speech AI Agent.
It uses 3 AI Pipelines(i.e Speech-to-Text(STT), Text-to-Text(TTT) and Text-to-Speech(TTS))

The Models that I used in this task are:-

Speech-to-Text(STT) - Deepgram

Text-to-Text(TTT) - Google Gemini

Text-to-Speech(TTS) - Eleven Labs


![Screenshot 2025-06-10 181117](https://github.com/user-attachments/assets/f5a1f8b7-009d-49fe-b8e3-c0fc5ed63bd3)

when we run the program in the Terminal it asks (Enter(y/n)?) as shown in the above picture,


![Screenshot 2025-06-10 181153](https://github.com/user-attachments/assets/c8777436-163f-4c94-bd12-f4014ea69b00)

After typing ("y") the speech to speech model start. 

First the program records your Audio by using Souddevice python library then Transcribes it using deepgram API. 

After Transcribing, it generates a conversation line according to the transcript using Google Gemini API.

After Generating a dialouge, it ask whether to continue the conversation

![Screenshot 2025-06-10 181207](https://github.com/user-attachments/assets/47497a2f-b73a-4aa6-a9fe-72fc6bff1f14)

When we press ("no") the program  gets exited as shown above




