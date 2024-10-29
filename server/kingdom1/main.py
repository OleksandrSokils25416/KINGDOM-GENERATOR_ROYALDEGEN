from transformers import pipeline

gen_pipeline = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')


def generate_text(context, max_length=300, temperature=0.9, output_file='output.txt'):
    """
    Parameters:
    - context (str): The input context for text generation.
    - max_length (int): Maximum length of generated text.
    - temperature (float): Sampling temperature to control creativity.
    - output_file (str): The file path to save the generated text.
    """
    output = gen_pipeline(context, max_length=max_length, do_sample=True, temperature=temperature,
                          pad_token_id=50256, truncation=True)

    if output:
        generated_text = output[0]['generated_text']
        with open(output_file, 'w') as f:
            f.write(generated_text)
        return generated_text
    else:
        print("No text was generated.")
        return None
