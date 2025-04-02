1. Introduction 

1.1 Problem Formulation  
Define the problem, why it matters, and how chatbots improve healthcare navigation. 
In the healthcare industry, timely and accurate diagnosis is critical for effective treatment. However, many patients struggle to determine which medical department they should visit based on their symptoms. This often results in unnecessary visits to the wrong department, leading to inefficiencies, increased waiting times, and additional costs for both patients and healthcare providers. 
Medical chatbots combined with machine learning have emerged as a potential solution to streamline the healthcare navigation process. A symptom-checking chatbot can engage in conversations with patients, systematically collecting symptoms and providing preliminary assessments. By analyzing patient responses, the chatbot can suggest potential medical conditions and direct them to the most relevant hospital department. This not only improves the triage process but also enhances patient experience and optimizes hospital resource utilization. 
However, implementing such systems in practice presents several challenges, particularly in understanding user input and generating accurate medical suggestions. During medical consultations, users often describe their symptoms in natural language and expect accurate diagnoses or meaningful medical advice in return. Traditional rule-based dialogue systems struggle to interpret complex, domain-specific inputs, while large language models (LLMs), although powerful, are prone to hallucinations that may lead to misdiagnoses. 

2 Objective of the project  
Outline the goal of your chatbot, such as guiding patients to the correct hospital department, improve triage process 
The primary objective of this project is to design and implement an intelligent chatbot-based healthcare guidance system that assists patients in identifying potential health conditions and recommending the appropriate hospital department for consultation. By reducing uncertainty in self-assessment and improving the triage process, the system aims to enhance patient experience and optimize hospital resource allocation. 
The proposed solution consists of two main components: 

(1) DialogFlow-based Chatbot 
The chatbot is responsible for engaging users in interactive, multi-turn conversations to collect relevant information, including symptoms, family medical history, age, gender, and other contextual details. 

(2) Machine Learning Classification Model 
This model is trained on structured medical data, such as disease descriptions extracted from medical books and symptom-disease mappings obtained from validated datasets. Once the chatbot gathers sufficient information, the model processes the inputs to predict the most likely disease and suggest the corresponding medical department.  

By integrating DialogFlow with a domain-adapted machine learning model, the system aims to: 

• Collect patient symptoms through natural language interactions 

• Perform preliminary analysis to suggest possible medical conditions 

• Recommend the most relevant hospital department based on the predicted disease

• Reduce patient uncertainty and improve the efficiency of hospital visits 
