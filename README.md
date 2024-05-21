# CI.AI: Cyberbullying Incineration Agency, Made with AI

## Why combating cyberbullying matters
Cyberbullying is a terrible thing that occurs online where a person is attacked for a certain reason. The rise of cyberbullying has led to Mental Health problems, impacts on education, and social anxiety for those getting bullied. Additionally, many cyberbullying social media posts don't get flagged for cyberbullying before getting posted. This model addresses just that.

## What CI.AI does
CI.AI takes screenshots and runs it through our AI model, which has been trained to identify cyberbullying in messages, and decides whether it is cyberbullying or not.

## How we built it
We built our project with a back-end part and a front-end. 

Our back-end was built using Google Colaboratory and Python, and we fine-tuned a RoBERTa-base language model from OpenAI using a dataset. Specifically, we utilized TensorFlow to successfully fine-tune our dataset. Our dataset is a comma-separated values (CSV) file with two columns: text and classification. A 1 means that it is classified as cyberbullying, and a 0 means that it is not classified as cyberbullying. After fine-tuning this existing model, we exported it using transformers.

Our front-end was built on Visual Studio Code using Flask, HTML, CSS, and JavaScript. The front end  implemented pytesseract and pillows to read an image into text, and used tensorflow, and its respective components, like keras, and models to predict. Not only that, we used os to print to the terminal for any error messages. 

## Challenges we ran into
Some challenges we faced mostly had to do with successfully fine-tuning the large language model (LLM) and connecting the back-end to the front-end. 

Fine-tuning took a long time especially because both the model and the .csv file were so large. To quantify, our model compressed into a .zip file took up about 440 MB of data, and our .csv file was thousands of rows long.

Not only that, connecting to front end was a huge problem. Tensorflow was not properly imported on vscode, and we had to install ten different python versions to get it to work. 

## Accomplishments that we're proud of
Something we're proud of is successfully connecting our back-end to our front-end. Connecting these parts involved heavy amounts of debugging, and required hours of patience.

## What we learned
Some valuable skills we gained through our experience at AcademiesHacks this year was learning to fine-tune a large-language model, as well as just how difficult it is to such a model in a limited time constraint. Additionally, we learned how to select the best large-language model to perform a specific task, and we found that RoBERTa was the best for text classification.

## What's next for CI.AI
Some features we would add in the future would be adapting our back-end code into a chrome extension, because it's more practical to flag cyberbullying directly on a social media website rather than creating a new website. Additionally, we plan on expanding our services by integrating speech-to-text features, as well as direct text input.
