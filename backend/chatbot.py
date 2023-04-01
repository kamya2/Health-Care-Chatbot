from classify_query import *
from query_generator import *
from phase_one_handlers import *
import openai
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(
    "./medical_question_similarity_model_25_6")
model = AutoModelForSequenceClassification.from_pretrained(
    "./medical_question_similarity_model_25_6")


def check_duplicate_question_pair(ques1, ques2):
    # Tokenize the input
    inputs = tokenizer(ques1, ques2, padding="max_length",
                       truncation=True, max_length=128, return_tensors="pt")

    # Pass the input through the model to get the predicted label
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits).item()
    print(ques2)
    print(torch.softmax(outputs.logits, dim=1)[0][predicted_label].item())
    return predicted_label


def find_similar_question(user_query):
    with open('data/questionDoctorQAs.json', encoding='utf-8', errors='ignore') as f:
        dt_questions = json.load(f)
        scores = []
        for i in range(10):
            question = dt_questions[i]['question']
            score = check_duplicate_question_pair(user_query, question)
            scores.append(score)
        mn = 9999
        for i in range(len(scores)):
            if scores[i] < mn:
                mn = i
        question = dt_questions[mn]['question']
        answer = dt_questions[mn]['answer']
        return question, answer


class HealthCareChatBot:
    def __init__(self):
        self.que_classifier = ClassifyQuery()
        self.query_generator = QueryGenerator()
        self.phase_one_find_answers = FindQueryResultPhaseOne()

    def get_response(self, user_query):
        classified_result = self.que_classifier.classify_que_category(user_query)

        if not classified_result:
            _, second_phase_answer = find_similar_question(user_query)

            if os.getenv('ERROR_TXT') in second_phase_answer:
                openai.organization = os.getenv('OPEN_AI_ORGANIZATION')
                openai.api_key = os.getenv('OPEN_AI_SECRET_KEY')
                res = openai.Completion.create(
                    model=os.getenv('OPEN_AI_MODEL'),
                    prompt=os.getenv('OPEN_AI_PROMPT') + user_query,
                    max_tokens=2048,
                    temperature=0
                )
                second_phase_answer = res.choices[0].text
                return second_phase_answer
            else:
                pass

            return "I'm not entirely sure if I grasp the question, but this is what I discovered: " + second_phase_answer

        sql_query = self.query_generator.generate_query(classified_result)

        bot_answer = self.phase_one_find_answers.phase_one_searcher(sql_query)

        if not bot_answer:
            # Perform Stage 2: Using Datasets by checking question similarity in a loop and extracting answer from least score
            _, second_phase_answer = find_similar_question(user_query)

            if os.getenv('ERROR_TXT') in second_phase_answer:
                openai.organization = os.getenv('OPEN_AI_ORGANIZATION')
                openai.api_key = os.getenv('OPEN_AI_SECRET_KEY')
                res = openai.Completion.create(
                    model=os.getenv('OPEN_AI_MODEL'),
                    prompt=os.getenv('OPEN_AI_PROMPT') + user_query,
                    max_tokens=2048,
                    temperature=0
                )
                second_phase_answer = res.choices[0].text

                return second_phase_answer
            else:
                pass
            return "I'm not entirely sure if I grasp the question, but this is what I discovered: " + second_phase_answer

        else:
            return '\n'.join(bot_answer)
