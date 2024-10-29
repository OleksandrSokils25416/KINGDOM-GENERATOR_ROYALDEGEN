from transformers import pipeline

gen = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

context = "City of Homel, Belarus, Chernobyl history"

# Generate the output text with adjusted parameters
output = gen(context, max_length=300, do_sample=True, temperature=0.9,
             pad_token_id=50256, truncation=True)

# Check if output was generated and write to file
if output:
    with open('dl.txt', 'w') as f:
        f.write(output[0]['generated_text'])
else:
    print("No text was generated.")
