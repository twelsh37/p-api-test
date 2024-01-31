# Perplexity AI API Test Code
Sample code utilising Perplexity API
You will need a perplexity API key for this code to work. I have mine in a .env file that i load in line 68 of my code and use in the headers on line 130. and in the requests.post on line 135

The article [Introducing pplx-api](https://blog.perplexity.ai/blog/introducing-pplx-api) is a good introduction

The point of this code was to allow me to play with the perplexity AI models and be able to select which one I wished to work with.
I store the conversation threads in .plx files and these can be loaded, or saved to at the beginning or end of each session.

Apart from that its all pretty standard stuff. 

The 5 models that are available currently (28/11/2023) are:
| # | Model                  |
|---|------------------------|
| 1 | codellama-34b-instruct |
| 2 | llama-2-70b-chat       |
| 3 | mistral-7b-instruct    |
| 4 | pplx-7b-chat           |
| 5 | pplx-7b-online         |
| 6 |llava-7b-chat           |
| 7 | mixtral-8x7b-instruct  |
| 8 |mistral-medium          |
| 9 |related                 |
