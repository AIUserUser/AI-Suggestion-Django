from django.shortcuts import render
from random import randint
from django.utils.html import format_html
import replicate
import openai

openai.api_key = 'sk-hZSaON5MWPtXcd4VvSDAgo9h7IVmAFXgi9JIYmp6RoT3BlbkFJeyZBAmeJTRMy0XZObVyLkZesvCzrmvPRxZwuXarsEA'


def index(request):
    # Retrieve the suggestion from the session
    suggestion = request.session.get('suggestion', '')
    
    if request.method == 'GET':
        # Clear the suggestion after retrieving it (optional)
        request.session['suggestion'] = ''
        return render(request, 'index.html', {'suggestion': suggestion})
    elif request.method == 'POST':
        return render(request, 'index.html', {'suggestion': suggestion})


def suggest(request):
    text = request.POST.get('text', '')
    if text:
        try:
            # Define a prompt template
            prompt_template = (
                "You are a helpful assistant. "
                "Complete the following sentence. Don't write more than 1 sentence.\n----\n{text}"
            )
            formatted_prompt = prompt_template.format(text=text)

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "user", "content": formatted_prompt}
                ],
                max_tokens=1024,
                temperature=0.6
            )
            completion = response['choices'][0]['message']['content']
            request.session['suggestion'] = completion.strip()  # Store in session
        except Exception as e:
            completion = f"Error: {str(e)}"
            print(f"Error generating suggestion: {str(e)}")
            request.session['suggestion'] = completion.strip()  # Store error in session

    else:
        completion = ""
        request.session['suggestion'] = "Error occurred."
    
    print(completion.strip())
    # Return just the suggestion HTML for HTMX to update the suggestion box
    return render(request, 'suggestion.html', {"suggestion": completion.strip()})
        
        
    #     input = {
    #         "prompt":
    #             f"Complete the following sentence. Don't write more than 1 sentence.\n----\n"
    #             f"{text}",
    #         "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    #                            "You are a helpful assistant. Don't include the start of the sentence. "
    #                            "Only include your completion. "
    #                            "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}"
    #                            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
    #         "max_tokens": 1024,
    #         "min_tokens": 0,
    #         "temperature": 0.6,
    #         "system_prompt": "You are a helpful assistant.",
    #         "presence_penalty": 0,
    #         "frequency_penalty": 0
    #     }

    #     output = replicate.run(
    #         "meta/meta-llama-3.1-405b-instruct",
    #         input=input
    #     )
    #     completion = "".join(output)

    # else:
    #     completion = ""
    
    # return render(request, 'suggestion.html', {"suggestion": completion.strip()})

