from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer
model_name = "distilbert/distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text_with_few_shot(prompt, examples):
    """Generate text using few-shot examples."""
    # Combine examples with the prompt
    full_prompt = "\n\n".join(examples) + "\n\n" + prompt
    inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True, padding="longest")
    
    # Generate text
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=1024,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Define few-shot examples
examples = [
    "Example 1: Input: 'The car is a 2015 model with a diesel engine.' Output: 'Car Model: 2015, Fuel Type: Diesel'",
    "Example 2: Input: 'The vehicle is a 2018 sedan in blue color.' Output: 'Car Model: 2018, Car Type: Sedan, Color: Blue'",
]

# Define the prompt
prompt = conversation = """
Salesperson: Welcome! Let me show you our selection. This is the I-20 model. Are you planning to pay in cash or take a loan?
Customer: I'm looking for a loan.
Salesperson: Great. What do you do for a living? Do you have a regular salary?
Customer: I work in agriculture.

Salesperson: Do you have an Income Tax Return (ITR)?
Customer: No, I don't.
Salesperson: Do you own any land or agricultural property?
Customer: No, I have a loan. This is Bangalore, right?
Salesperson: Yes, it is. Do you have any outstanding loans to pay off?
Customer: Yes, I do.
Salesperson: Do you have a specific budget in mind?
Customer: Yes, I do.
Salesperson: Could you share your mobile number, please?
Customer: It's 1851595.
Salesperson: And your name?
Customer: Manoj, Do you have vehicles for daily use?
Salesperson: Yes, we do.
Customer: I have two vehicles already. One is from 2017 and the other from 2014.
Salesperson: This one here is priced at 5,39,000 rupees, and that one is 5,24,000 rupees. Both are West Bengal registered.
Customer: WB registration?
Salesperson: Yes, but we can include Karnataka registration at the same price. However, for diesel vehicles, you might not find many options. You could consider petrol vehicles like the I-10 or Eon.
Customer: The I-10 is too small.
Salesperson: In that case, you might want to look at the Alto. With a budget of 3.5 lakhs, you won't find a Venue or I-20.
Customer: What about petrol options?
Salesperson: The Venue starts from 9 lakhs.
Customer: What?
Salesperson: Yes, the Venue starts from 9 lakhs. The I-20 starts from 5 lakhs minimum. You can consider it.
Customer: What are the benefits?
Salesperson: The engine and gearbox come with a one-year guarantee. Please have a seat. We ensure the vehicle has passed 200 checkpoints, and the RC transfer and one-year insurance are included. If you're not satisfied, you can return the vehicle within 5 days or 300 Km for a full cash refund.
Customer: How much is the vehicle price?
Salesperson: We have diesel options available. What do you think about this vehicle?
Customer: It looks okay, but what about the warranty?
Salesperson: The warranty is for one year. If not, the engine and gearbox are covered for 100,000 Km.
Customer: What about the honda diesel?
Salesperson: It's available for 100,000 Km. It's a 2011 model with 1,22,000 Km on it.
Customer: And the second one?
Customer: We have Tiago.
Salesperson: I dont want Tiago.
Salesperson: That one has 3,21,000 Km on it.

"""

# Generate text with few-shot examples
generated_text = generate_text_with_few_shot(prompt, examples)
print(generated_text)
