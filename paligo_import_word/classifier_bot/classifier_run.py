from paligo_import_word.classifier_bot.text_classifier_ai.supervised_leaning import AI_supervised_learning

def run_supervised_learning(list_of_strings: list):
    supervised_ai = AI_supervised_learning(list_of_strings, "paligo_import_word\\classifier_bot\\text_classifier_ai\\text_classifier_data\\classifier_model_1")
    new_data = supervised_ai.run_supervised_learning()
    return new_data