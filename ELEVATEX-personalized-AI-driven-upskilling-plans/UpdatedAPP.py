from flask import Flask, render_template, request
import pandas as pd
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = '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'

# Setup your OpenAI API credentials
openai.api_key = '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'

# Load the data from the Excel sheet
data = pd.read_excel("D:\Test\Data\data.xlsx")

# Define a function to recommend certificates based on job role and years of experience
def recommend_certificates(role, experience, available_certificates):
    filtered_data = data[(data['job_title'] == role) & (data['experience_years'] <= experience)]
    recommended_certificates = filtered_data['courses_or_certificates'].tolist()
    filtered_certificates = [cert for cert in recommended_certificates if cert in available_certificates]
    return filtered_certificates

# Define a function to generate chatbot response using ChatGPT
# Generate a chatbot response using ChatGPT
def generate_chatbot_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    experience = int(request.form['experience'])
    job_role = request.form['job_role']
    certificates_available = request.form.getlist('certificates_available')

    # Filter the recommended certificates based on job role, experience, and available certificates
    recommended_certificates = recommend_certificates(job_role, experience, certificates_available)

    # Generate a chatbot response using ChatGPT
    chatbot_message = f"I recommend the following certificates for a {job_role} with {experience} years of experience:\n"
    if recommended_certificates:
        for i, cert in enumerate(recommended_certificates):
         chatbot_message += f"{i+1}. {cert}\n"
        chatbot_message += "You can start by acquiring these certificates to enhance your career path."
    else:
     chatbot_message += "Unfortunately, no recommended certificates are available or match your criteria."

    chatbot_response = generate_chatbot_response(chatbot_message)

    return render_template('index.html', recommendation=chatbot_response)

if __name__ == "__main__":
    app.run(debug=True)
