from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

@app.route('/')
def career():
    return render_template("hometest.html")

@app.route('/predict', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        res = result.to_dict(flat=True)
        arr = [float(value) for value in res.values()]
        data = np.array(arr).reshape(1, -1)

        loaded_model = pickle.load(open("careerlast.pkl", 'rb'))
        predictions = loaded_model.predict(data)
        pred = loaded_model.predict_proba(data) > 0.05

        res, final_res = {}, {}
        for j in range(17):
            if pred[0, j]:
                res[len(res)] = j
        for idx, val in res.items():
            if val != predictions[0]:
                final_res[len(final_res)] = val

        jobs_dict = {
            0: 'AI ML Specialist',
            1: 'API Integration Specialist',
            2: 'Application Support Engineer',
            3: 'Business Analyst',
            4: 'Customer Service Executive',
            5: 'Cyber Security Specialist',
            6: 'Data Scientist',
            7: 'Database Administrator',
            8: 'Graphics Designer',
            9: 'Hardware Engineer',
            10: 'Helpdesk Engineer',
            11: 'Information Security Specialist',
            12: 'Networking Engineer',
            13: 'Project Manager',
            14: 'Software Developer',
            15: 'Software Tester',
            16: 'Technical Writer'
        }

        data1 = predictions[0]
        labels_to_index = {v: k for k, v in jobs_dict.items()}
        index = labels_to_index.get(data1, None)

        if index is None:
            return "Invalid career prediction"

        predicted_career = data1

        return render_template("testafter.html", final_res=final_res,
                               jobs_dict=jobs_dict, job0=index,
                               career_name=predicted_career)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "")
    career = data.get("career", "")

    prompt = f"""You are a career guidance assistant. The user is interested in the career: {career}.

User: {user_message}
Assistant:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma:2b",  # ✅ Set to gemma:2b
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that gives career-specific guidance."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )
        reply = response.json()["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        print("Ollama error:", e)
        return jsonify({"reply": "Sorry, Ollama is not responding."})

if __name__ == '__main__':
    app.run(debug=True)
