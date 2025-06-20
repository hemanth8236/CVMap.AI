import numpy as np
import nltk as nlp

class SubjectiveTest:
    def __init__(self, skills, noOfQues, valid_keywords=None):
        self.specific_questions = {
            "java": [
                "Explain the concept of OOP in Java.",
                "What are the four pillars of OOP in Java?",
                "Describe the use of inheritance in Java with examples.",
                "What is polymorphism in Java, and how does it work?",
                "Explain exception handling in Java.",
                "What are the types of inheritance and explain each of them with real-world problems?",
                "What are the new features added in java verion 5"
            ],
            "python": [
                "What are Python decorators, and how are they used?",
                "Explain the differences between Python 2 and Python 3.",
                "Describe list comprehensions in Python with examples.",
                "What is the role of the Global Interpreter Lock (GIL) in Python?",
                "Explain how memory management works in Python.",
                "Explain the purpose of __init__ and __str__ methods in a Python class.",
                "How does error handling work in Python? Explain try, except, else, and finally blocks.",
                "What are Python's *args and **kwargs, and how are they useful in functions?"
            ],
            "machine learning": [
                "What is overfitting in machine learning, and how can it be avoided?",
                "Explain the difference between supervised and unsupervised learning.",
                "Describe the concept of feature engineering in machine learning.",
                "How does a decision tree algorithm work in machine learning?",
                "Explain the process of model evaluation and validation.",
                "What is Overfitting and underfitting in Machine Learning?",
                "What is bias and variance in machine learning"
            ],
            "data analysis": [
                "Describe the data cleaning process in data analysis.",
                "What are the common statistical measures used in data analysis?",
                "Explain the importance of data visualization in data analysis.",
                "How would you handle missing values in a dataset?",
                "What is the role of exploratory data analysis (EDA) in data science?"
            ],
            "SQL":[
                "Explain what a stored procedure is in SQL. When and why would you use it?",
                "What is a view in SQL, and how does it differ from a table?",
                "Describe the concept of a trigger in SQL. Provide an example use case.",
                "How does the ROLLBACK command work, and why is it essential in managing transactions?",
                "What is a subquery in SQL, and how does it differ from a join? Provide examples.",
                "What are aggregate functions in SQL? Provide examples of commonly used ones.",
                "Explain what a recursive query is and provide an example of when you would use it."
            ],
            "MySQL":[
                "How does MySQL handle foreign key constraints?",
                "Explain how to optimize a query in MySQL. What are some common performance tuning techniques?",
                "Describe MySQL’s replication architecture and its types (e.g., master-slave, master-master).",
                "What are MySQL’s EXPLAIN and ANALYZE commands? How do they help in optimizing queries?",
                "Explain how to use the AUTO_INCREMENT property in MySQL. What are its advantages and limitations?",
                "How do you manage user permissions in MySQL? Explain the concept of roles and privileges.",
                "What are the advantages of using MySQL’s JSON data type, and how can it be queried?"
            ]
        }

        # General question patterns if no specific templates are found
        self.general_question_pattern = [
            "What is the significance of {} in modern applications?",
            "How does {} contribute to solving real-world problems?",
            "Can you explain the fundamental principles of {}?",
            "What are the challenges associated with {}?",
            "How would you explain the importance of {} to a beginner?",
            "Describe advanced concepts related to {} and their use cases.",
            "How does {} integrate with other technologies?",
            "What are the best practices for using {} effectively?",
            "Explain the historical development of {} and its evolution.",
            "What are the ethical considerations surrounding {}?",
            "In what scenarios would {} be particularly useful?",
            "What are some common misconceptions about {}?",
            "How do you keep up with advancements in {}?",
            "Discuss the advantages and disadvantages of using {}.",
            "Can you provide a practical example of implementing {}?",
        ]

        self.skills = skills  
        self.noOfQues = noOfQues
        self.valid_keywords = valid_keywords if valid_keywords else []

    def generate_questions(self):
        unique_questions = set()  

        for skill in self.skills:
            skill_lower = skill.lower()
            if skill_lower in self.specific_questions:
                questions = self.specific_questions[skill_lower]
                for question in questions[:self.noOfQues]:
                    unique_questions.add(question)
            else:
                for i in range(self.noOfQues):
                    rand_num = np.random.randint(0, len(self.general_question_pattern))
                    question = self.general_question_pattern[rand_num].format(skill)
                    unique_questions.add(question)

        question_list = list(unique_questions)
        return question_list[:self.noOfQues]
