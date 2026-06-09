from analyzer.summarizer import generate_summary

text = """
Artificial Intelligence is transforming industries worldwide.
Machine learning and deep learning are helping organizations
automate processes, improve decision making and create
intelligent applications.
"""

summary = generate_summary(text)

print(summary)