import json

d = {
    "jobAd": """
    Machine Learning Engineer - Freelance 
Germany · Reposted 6 days ago · Over 100 applicants

 Remote
Matches your job preferences, workplace type is Remote.
Contract
1 of 9 skills match: Python (Programmiersprache)
1 of 9 required skills are found on your profile

Easy Apply

Save
Save Machine Learning Engineer - Freelance  at THRYVE
Stand out to the employer by marking this job as a top choice when you apply. Learn more
Your AI-powered job assessment


Am I a good fit?

Tailor my resume

How can I best position myself?
People you can reach out to
Ben profile photo
Ben profile photo
Ben Burton
 
· 1st
Building Freelance Project and Product Manager teams in Germany

Message
Meet the hiring team
Chloé
Chloé Dingomal 
 2nd
I help scale and cultivate high-performing AI & ML teams in Europe 🚀
Job poster · 8 mutual connections

Message
About the job
Job Title: Freelance Machine Learning Engineer

Location: Germany (Remote/On-Site Flexibility)

Industry: Financial Services

Duration: Project-Based (3-6 months, with potential extension)



Responsibilities

Fraud Detection and Prevention:
Develop and implement ML models to identify and prevent fraudulent activities, such as unauthorized transactions and identity theft.
Utilise anomaly detection techniques (e.g., unsupervised learning) to identify unusual patterns in data.
Train supervised learning models on labelled fraud datasets to improve accuracy and precision in fraud identification.
Implement real-time fraud monitoring systems using reinforcement learning or similar approaches.
Collaborate with cross-functional teams, including data analysts, engineers, and compliance officers, to align solutions with business needs and regulatory requirements.
Build and optimise scalable pipelines for fraud detection in real-time environments.
Ensure all models comply with data privacy laws (e.g., GDPR) and adhere to the highest standards of security.
Conduct ongoing research on the latest ML techniques for fraud prevention and integrate new methodologies into existing systems.
Document processes, models, and findings, and provide knowledge transfer to internal teams.


Qualifications

Technical Skills:

Strong programming skills in Python and expertise in ML frameworks such as TensorFlow, PyTorch, or Scikit-learn.
Proven experience in anomaly detection, supervised learning, and reinforcement learning techniques.
Hands-on experience with real-time monitoring systems and building scalable data pipelines.
Familiarity with financial datasets and understanding of challenges in fraud detection within the financial services industry.
Proficiency in using SQL and data processing tools for feature engineering and analysis.
    """
}

print(json.dumps(d, indent=8))
