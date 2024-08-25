# AWS Certification Prep Assistant

![Screenshot 2024-08-21 at 8 31 43 PM](https://github.com/user-attachments/assets/64b943a0-ccde-4c1f-a7b6-89956cf34c71)

## Description

The AWS Certification Prep Assistant is an interactive, AI-powered application designed to help students prepare for the AWS Certified Solutions Architect - Associate (SAA-C03) exam. This Streamlit-based app utilizes OpenAI's GPT models to provide personalized study sessions, quizzes, and in-depth explanations of AWS concepts and services.

## Features

- **Multiple Study Modes:**
  - Quick Quiz: Generate multiple-choice questions for rapid learning
  - Concept Explanation: Ask questions about specific AWS concepts
  - Service Deep Dive: Get comprehensive information about selected AWS services
  - Practice Question: Receive scenario-based questions mimicking the actual exam style

- **Domain-Focused Learning:** Select specific exam domains to focus your study
- **AWS Service Selection:** Choose from a list of key AWS services for targeted learning
- **Conversation Management:** Save and load study sessions for continued learning
- **Token Usage Tracking:** Monitor the extent of your interactions with the AI

## Prerequisites

- Python 3.7+
- Streamlit
- OpenAI Python library

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lalomorales22/AI-AWS-Study-Buddy.git
   cd aws-cert-prep-assistant
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key to the file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`)

3. Enter your name and select a study mode from the sidebar

4. Choose an exam domain to focus on

5. If in "Service Deep Dive" mode, select an AWS service to study

6. Interact with the AI assistant by asking questions or generating quiz/practice questions

7. Save your study session using the "Save Conversation" button in the sidebar

8. Load previous study sessions using the "Load Conversation" feature

## Exam Domains

The app covers the four main domains of the AWS Certified Solutions Architect - Associate (SAA-C03) exam:

1. Design Secure Architectures (30%)
2. Design Resilient Architectures (26%)
3. Design High-Performing Architectures (24%)
4. Design Cost-Optimized Architectures (20%)

## Key AWS Services

The app includes a curated list of key AWS services relevant to the SAA-C03 exam, including but not limited to:

- Amazon EC2
- Amazon S3
- Amazon VPC
- Amazon RDS
- AWS Lambda
- Amazon CloudFront
- Amazon Route 53
- Elastic Load Balancing
- AWS IAM

## Contributing

Contributions to improve the AWS Certification Prep Assistant are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Disclaimer

This application is an unofficial study aid and is not affiliated with or endorsed by Amazon Web Services (AWS). Always refer to official AWS documentation and exam guides for the most up-to-date and accurate information regarding AWS certifications.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/aws-cert-prep-assistant](https://github.com/yourusername/aws-cert-prep-assistant)
