import streamlit as st
import requests

# 🔐 Replace these with your actual Azure values
API_KEY = "8mlIIa27juYTrrhBRKTr9MtedFC3MXFl4ielbFKWFrtY3rlha23qJQQJ99BGACMsfrFXJ3w3AAAaACOGYcLz"
ENDPOINT = "https://language52927870.cognitiveservices.azure.com/"
PROJECT_NAME = "EMAIL_DETECTOR"  # Match your Azure project name
DEPLOYMENT_NAME = "production"            # Match your deployment name

# Store previous results
if "history" not in st.session_state:
    st.session_state.history = []

# Function to call Azure API
def check_email(text):
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "kind": "CustomClassification",
        "parameters": {
            "projectName": PROJECT_NAME,
            "deploymentName": DEPLOYMENT_NAME,
            "stringIndexType": "TextElement_v8"
        },
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": text.strip()
                }
            ]
        }
    }

    response = requests.post(
        f"{ENDPOINT}/language/:analyze-text?api-version=2022-05-01",
        headers=headers,
        json=data
    )

    try:
        result = response.json()
        classification = result["results"]["documents"][0]["classifications"][0]
        label = classification["category"]
        confidence = round(classification["confidenceScore"] * 100, 2)
        return label, confidence
    except Exception as e:
        st.error("API Error: Could not classify the email.")
        return "Error", 0

# UI with Streamlit
st.title("📨 Phishing Email Detector with Dashboard")

email_text = st.text_area("📩 Paste your email content below:")

if st.button("Detect"):
    label, confidence = check_email(email_text)
    st.session_state.history.append({
        "Email": email_text,
        "Result": f"⚠ Phishing" if label == "Phishing" else "✅ Safe",
        "Confidence": f"{confidence}%"
    })

    if label == "Phishing":
        st.error(f"⚠ Phishing Email Detected! (Confidence: {confidence}%)")
    elif label == "Safe":
        st.success(f"✅ Safe Email! (Confidence: {confidence}%)")
    else:
        st.warning("⚠ Something went wrong. Please try again.")

# Display dashboard
if st.session_state.history:
    st.markdown("## 📊 Detection History")
    st.table(st.session_state.history)
    