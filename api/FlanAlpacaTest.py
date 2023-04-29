from transformers import pipeline

prompt = "Write an email about an alpaca that likes flan"
model = pipeline(model="declare-lab/flan-alpaca-xl")
model(prompt, max_length=128, do_sample=True)

# Dear AlpacaFriend,
# My name is Alpaca and I'm 10 years old.
# I'm excited to announce that I'm a big fan of flan!
# We like to eat it as a snack and I believe that it can help with our overall growth.
# I'd love to hear your feedback on this idea.
# Have a great day!
# Best, AL Paca
