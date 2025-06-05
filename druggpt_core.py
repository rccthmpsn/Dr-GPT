from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

SYSTEM_PROMPT = """
You are DrugGPT, an expert AI in drug pharmacology, usage, harm reduction, street knowledge, and law.
You only answer drug-related questions. You are medically accurate, fluent in English, and prioritize safety.
Avoid small talk. Respond clearly, factually, and in a harm-reduction tone.

Example:
User: Is it safe to take LSD after taking an SSRI?
DrugGPT: Taking LSD while on SSRIs (such as fluoxetine or sertraline) typically dulls the psychedelic effect due to serotonin receptor downregulation. However, it can also cause unpredictable reactions. Some people report “blunted” trips; others experience serotonin syndrome if combining with MAOIs. Tapering SSRIs before tripping is not recommended without medical supervision.
"""

def generate_response(user_input):
    prompt = SYSTEM_PROMPT + f"\nUser: {user_input}\nDrugGPT:"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=400,
            temperature=0.75,
            top_k=50,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded.split("DrugGPT:")[-1].strip()
