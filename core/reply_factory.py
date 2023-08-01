
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
    else:
        success, error = record_current_answer(message, current_question_id, session)

        if not success:
            return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to session.
    '''
    if current_question_id != None:
        question = PYTHON_QUESTION_LIST[current_question_id - 1] if current_question_id > 0 else None
        if question and question["answer"] == answer:
            session["correct_answers"] = session.get("correct_answers", 0) + 1

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id == None:
        current_question_id=0
        
    if current_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[current_question_id]
        question_text = str(next_question["question_text"])
        options_text = str(next_question["options"])
        return f"{question_text} \n Options: \n {options_text}", current_question_id + 1
    else:
        return None, None

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    correct_answers = session.get("correct_answers", 0)
    if correct_answers != 0:
        del session['correct_answers']
    return f"You answered {correct_answers} out of {len(PYTHON_QUESTION_LIST)} questions correctly!"
