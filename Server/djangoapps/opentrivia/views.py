from django.shortcuts import render
from django.http import HttpResponse
import requests

def find_question(request) :
    url = "https://opentdb.com/api.php?amount=1"
    response = requests.get(url)

    if response.status_code == 200:
        question_data = response.json()
        questions = question_data["results"]
        return (questions)
        # for question in questions:
        #     print("Question:", question["question"])
        #     print("Category:", question["category"])
        #     print("Difficulty:", question["difficulty"])
        #     print("Correct Answer:", question["correct_answer"])
        #     print("Incorrect Answers:", question["incorrect_answers"])
        #     print()
    else:
        return ("Erreur lors de la récupération des questions trivia.")
