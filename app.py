import streamlit as st
from openai import OpenAI
import time
import json
import os
from datetime import datetime
import random
import plotly.graph_objects as go
from streamlit_ace import st_ace

# Initialize the OpenAI client
client = OpenAI()

# AWS SAA-C03 exam domains and their weights
EXAM_DOMAINS = {
    "Design Secure Architectures": 30,
    "Design Resilient Architectures": 26,
    "Design High-Performing Architectures": 24,
    "Design Cost-Optimized Architectures": 20
}

# List of key AWS services mentioned in the cert guide
AWS_SERVICES = [
    "Amazon EC2", "Amazon S3", "Amazon VPC", "Amazon RDS", "Amazon DynamoDB",
    "AWS Lambda", "Amazon CloudFront", "Amazon Route 53", "Elastic Load Balancing",
    "AWS IAM", "Amazon CloudWatch", "AWS CloudTrail", "Amazon SNS", "Amazon SQS",
    "AWS Direct Connect", "Amazon API Gateway", "AWS CloudFormation"
]

# Function to get OpenAI response (existing function, unchanged)
def get_openai_response(messages, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

# Function to stream OpenAI response (existing function, unchanged)
def stream_openai_response(messages, model="gpt-3.5-turbo"):
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to save conversation (existing function, unchanged)
def save_conversation(messages, filename):
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    os.makedirs('conversations', exist_ok=True)
    file_path = os.path.join('conversations', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []
    except json.JSONDecodeError:
        conversations = []
    
    conversations.append(conversation)
    
    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

# Function to load conversations (existing function, unchanged)
def load_conversations(uploaded_file):
    if uploaded_file is not None:
        try:
            conversations = json.loads(uploaded_file.getvalue().decode("utf-8"))
            return conversations
        except json.JSONDecodeError:
            st.error("Error decoding the uploaded file. The file may be corrupted or not in JSON format.")
            return []
    else:
        st.warning("No file was uploaded.")
        return []

# New function to generate a progress chart
def generate_progress_chart(progress_data):
    fig = go.Figure(data=[go.Bar(x=list(progress_data.keys()), y=list(progress_data.values()))])
    fig.update_layout(title_text="Domain Progress", xaxis_title="Domains", yaxis_title="Progress (%)")
    return fig

# New function to create flashcards
def create_flashcard(front, back):
    return {"front": front, "back": back}

# New function for spaced repetition
def spaced_repetition_algorithm(flashcards, user_performance):
    # Simple implementation - adjust review time based on performance
    for card in flashcards:
        if card['id'] in user_performance:
            if user_performance[card['id']] == 'correct':
                card['next_review'] = datetime.now() + timedelta(days=2)
            else:
                card['next_review'] = datetime.now() + timedelta(hours=4)
    return flashcards

# Main function
def main():
    st.set_page_config(layout="wide", page_title="AWS Cert Prep Assistant", page_icon="🚀")
    
    # Apply custom CSS for dark mode
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSelectbox, .stTextInput {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🚀 AWS Certified Solutions Architect - Associate (SAA-C03) Prep Assistant")

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = {"prompt": 0, "completion": 0}
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Student"
    if "progress" not in st.session_state:
        st.session_state.progress = {domain: 0 for domain in EXAM_DOMAINS}
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.session_state.user_name = st.text_input("👤 Enter your name:", value=st.session_state.user_name)

        study_mode = st.selectbox("📚 Choose a study mode", ["Quick Quiz", "Concept Explanation", "Service Deep Dive", "Practice Question", "Flashcards"])
        selected_domain = st.selectbox("🎯 Select a domain to focus on", list(EXAM_DOMAINS.keys()))
        st.write(f"Domain weight: {EXAM_DOMAINS[selected_domain]}%")

        if study_mode == "Service Deep Dive":
            selected_service = st.selectbox("🔍 Select an AWS service", AWS_SERVICES)

        # Custom instructions (similar to before, but with added flashcard support)
        custom_instructions = f"""You are an AWS Certification expert, specifically for the AWS Certified Solutions Architect - Associate (SAA-C03) exam. Your role is to help {st.session_state.user_name} prepare for their exam by providing comprehensive information, asking relevant questions, and offering explanations across all exam domains.

Your knowledge spans:
{', '.join(EXAM_DOMAINS.keys())}

The student is currently focusing on the {selected_domain} domain.

For each domain, you should be able to:
1. Provide detailed explanations of key concepts
2. Ask challenging questions that mimic the style and difficulty of SAA-C03 exam
3. Offer mnemonics and memory aids to help students retain information
4. Explain complex processes step-by-step
5. Highlight common misconceptions and how to avoid them
6. Discuss real-world applications of the knowledge
7. Create flashcards with concise questions on the front and detailed answers on the back

When interacting:
- Tailor your responses to the student's level of understanding
- Use clear, concise language while maintaining technical accuracy
- Encourage critical thinking by asking follow-up questions
- Provide positive reinforcement and motivation
- Offer study strategies and time management tips for SAA-C03 exam preparation

Current study mode: {study_mode}
"""

        if study_mode == "Service Deep Dive":
            custom_instructions += f"\nThe student wants to deep dive into the {selected_service} service. Provide comprehensive information about its features, use cases, and how it relates to the SAA-C03 exam."

        # Study mode specific actions
        if study_mode == "Quick Quiz":
            if st.button("Generate Quick Quiz Question"):
                prompt = f"Generate a multiple-choice question related to the {selected_domain} domain for the AWS Certified Solutions Architect - Associate (SAA-C03) exam. Provide 4 options and indicate the correct answer."
                st.session_state.messages.append({"role": "user", "content": prompt})
        elif study_mode == "Practice Question":
            if st.button("Generate Practice Question"):
                prompt = f"Generate a scenario-based question related to the {selected_domain} domain for the AWS Certified Solutions Architect - Associate (SAA-C03) exam. The question should mimic the actual exam style. Provide a detailed explanation of the correct answer and why the other options are incorrect."
                st.session_state.messages.append({"role": "user", "content": prompt})
        elif study_mode == "Flashcards":
            if st.button("Generate Flashcard"):
                prompt = f"Create a flashcard for a key concept in the {selected_domain} domain. Provide a concise question for the front of the card and a detailed explanation for the back."
                st.session_state.messages.append({"role": "user", "content": prompt})
        else:
            prompt = st.chat_input(f"Ask a question about {selected_domain}:")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": f"{st.session_state.user_name}: {prompt}"})

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Generate and display AI response
        if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in stream_openai_response([
                    {"role": "system", "content": custom_instructions},
                    *st.session_state.messages
                ]):
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            response, prompt_tokens, completion_tokens = get_openai_response([
                {"role": "system", "content": custom_instructions},
                *st.session_state.messages
            ])
            st.session_state.token_count["prompt"] += prompt_tokens
            st.session_state.token_count["completion"] += completion_tokens

            # Update progress for the current domain (simplified implementation)
            st.session_state.progress[selected_domain] += 5
            if st.session_state.progress[selected_domain] > 100:
                st.session_state.progress[selected_domain] = 100

    with col2:
        st.subheader("📊 Your Progress")
        progress_chart = generate_progress_chart(st.session_state.progress)
        st.plotly_chart(progress_chart, use_container_width=True)

        st.subheader("💡 Study Tips")
        st.write("1. Review regularly")
        st.write("2. Practice with real-world scenarios")
        st.write("3. Use AWS documentation")

        st.subheader("🏆 Achievements")
        if sum(st.session_state.progress.values()) >= 100:
            st.success("🎉 You've made significant progress!")

    # Sidebar
    st.sidebar.title("⚙️ Options")

    # Dark mode toggle
    if st.sidebar.checkbox("🌙 Dark Mode", value=True):
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stSelectbox, .stTextInput {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    st.sidebar.subheader("💾 Conversation Management")
    save_name = st.sidebar.text_input("Save conversation as:", "aws_cert_prep_conversation.json")
    if st.sidebar.button("💾 Save Conversation"):
        save_conversation(st.session_state.messages, save_name)
        st.sidebar.success(f"Conversation saved to conversations/{save_name}")

    st.sidebar.subheader("📂 Load Conversation")
    uploaded_file = st.sidebar.file_uploader("Choose a file to load conversations", type=["json"])
    
    if uploaded_file is not None:
        try:
            conversations = load_conversations(uploaded_file)
            if conversations:
                st.sidebar.success(f"Loaded {len(conversations)} conversations from the uploaded file")
                selected_conversation = st.sidebar.selectbox(
                    "Select a conversation to load",
                    range(len(conversations)),
                    format_func=lambda i: conversations[i]['timestamp']
                )
                if st.sidebar.button("📥 Load Selected Conversation"):
                    st.session_state.messages = conversations[selected_conversation]['messages']
                    st.sidebar.success("Conversation loaded successfully!")
            else:
                st.sidebar.error("No valid conversations found in the uploaded file.")
        except Exception as e:
            st.sidebar.error(f"Error loading conversations: {str(e)}")

    st.sidebar.subheader("🧮 Token Usage")
    st.sidebar.write(f"Prompt tokens: {st.session_state.token_count['prompt']}")
    st.sidebar.write(f"Completion tokens: {st.session_state.token_count['completion']}")
    st.sidebar.write(f"Total tokens: {sum(st.session_state.token_count.values())}")

    # New feature: Code playground
    st.sidebar.subheader("🖥️ Code Playground")
    if st.sidebar.checkbox("Show Code Playground"):
        code = st_ace(
            placeholder="Write your AWS-related code here",
            language="python",
            theme="monokai",
            key="code_editor"
        )
        if code:
            st.code(code, language="python")

if __name__ == "__main__":
    main()