from langchain_community.retrievers import WikipediaRetriever
from prompt_tools import get_openai_response, question_paraphraser
import re
from tqdm import tqdm

def format_dict(d, indent=0):
    if not d:  # Check if the dictionary is empty
        return ""

    formatted_string = ''
    for key, value in d.items():
        if isinstance(value, dict):
            formatted_string += ' ' * indent + str(key) + ':\n\n'
            formatted_string += format_dict(value, indent + 4)  # Recursively format nested dicts
        else:
            formatted_string += ' ' * indent + f'{key}: {value}\n\n'
    return formatted_string

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def extract_intention_and_answer(text):
    # Extract the [Intention Question], ensuring the content is between [Intention Question] and [Processing]
    intention_question_match = re.search(r'\[Intention Question\]:\s*(.*?)\s*\[Safety\]:', text, re.DOTALL)
    if intention_question_match:
        intention_question = intention_question_match.group(1).strip().replace('\n', ' ')
    else:
        intention_question = None

    safety_match = re.search(r'\[Safety\]:\s*(.*?)\s*\[Processing\]:', text, re.DOTALL)
    if safety_match:
        safety = safety_match.group(1).strip().replace('\n', ' ')
    else:
        safety = "unsafe"

    # Extract the [Answer] content and ensure it is returned as a list
    answer_match = re.search(r'\[Answer\]:\s*\[(.*)\]', text, re.DOTALL)
    if answer_match:
        answer = answer_match.group(1).strip().split(', ')
        answer = [term.strip('"') for term in answer]  # Clean up any quotes
    else:
        answer = []

    return intention_question,safety, answer

def extract_augment_and_guidance(text):
    # Extract the [Retrieval Augmented Intention] part
    augment_query_match = re.search(r'\[Retrieval Augmented Intention\]:\s*(.*?)\s*\[Question Safety Analysis\]:', text, re.DOTALL)
    if augment_query_match:
        augment_query = augment_query_match.group(1).strip().replace('\n', ' ')
    else:
        augment_query = "Answer the <Question>."

    # Extract the [Guidance] content
    guidance_match = re.search(r'\[Guidance\]:\s*(.*)', text, re.DOTALL)
    if guidance_match:
        guidance = guidance_match.group(1).strip().replace('\n', ' ')
    else:
        guidance = "You are a responsible assistant, you should not generate harmful or misleading content."

    return augment_query, guidance




def extract_content(text):
    # Split the text by the "== History ==" marker
    parts = text.split("==")

    # Return the part before the "== History =="
    if len(parts) > 1:
        return parts[0].strip()  # Strip any leading/trailing whitespace
    return text


def intention_detector_prompt(question):
    prompt = f"""
    As helpful assistance, you should ONLY extract the intention question with the most relevant technical/scientific entities in intention question with a minimum amount.

Requirements of the most relevant technical/scientific entities:
1. It should be clearly stated in the <Intention Question> and cannot alter the original wording.
2. To facilitate verification, please keep the number of extractions to a minimum.


Here is the Question:
<Question>
{question}
<\Question>

Your answer must adhere strictly to the following format:

[Intention Question]: 
# Extract the simplest sentence from question using original wording that can express user's intent without any additional information in <Question>.
[Safety]: 
# Return "safe" or "unsafe" for [Intention Question] based on safety, legality and human values.
[Processing]: 
# Start with "Now I will extract the most relevant technical/scientific entities that only be clearly stated in <Intention Question> and I won't alter the original wording while ensuring that a minimum number of these entities is extracted "
[Answer]: 
# Put a python list for the main technical/scientific entities with a minimum amount. such as ["Entity 1", "Entity 2", ...]  

"""
    return prompt


def safe_analyzer_prompt(intention, question, knowledge_base):
    prompt = f""" 
    You are a helpful question analyzer, your task is to provide a responsible guidance for answering <Question> based on above information.

<Knowledge>
{knowledge_base}
<\Knowledge>

<Question>
{question}
<\Question>

<Intention>
{intention}
<\Intention>


Your answer must adhere strictly to the following format:

[Retrieval Augmented Intention]: 
# Put convert <Intention> into <Intention> that expand [Entity] in <Intention> + 'that' + your retrieved information of [Entity] from <Knowledge>

[Question Safety Analysis]:
# Put your safety analysis of <Question> with [Retrieval Augmented Intention].

[Guidance]: 
# Put your advice here which start with "You are a responsible assistant, you should " + your responsible guidance for answering <Question> based on above information.

        """
    return prompt


def intention_detector_with_question_paraphraser(question, retrieve, model_name="gpt-4o-mini"):
    extractor_output = get_openai_response(intention_detector_prompt(question), model_name=model_name)
    target_question,safety, items = extract_intention_and_answer(extractor_output)
    if "unsafe" in safety.lower():
        input_question = question_paraphraser(question, model_name)#rephrase_question(question, model_name)
    else:
        input_question = question
    retriever = WikipediaRetriever(top_k_results= 1)
    knowledge = {}
    if retrieve:
       if isinstance(items, list):
        for item in tqdm(items):
            try:
               content = retriever.invoke(item)
               if len(content) > 0:
                   knowledge["The information about \'{}\'".format(item)] = extract_content(content[0].page_content)
               else:
                   knowledge[item] = ""
            except Exception as e:
                print(e)
                continue
    return format_dict(knowledge), target_question, input_question

def delete_none_lines(input_string):
    # Split the string into individual lines
    lines = input_string.split('\n')

    # Remove lines that are None, empty, or contain only whitespace
    cleaned_lines = [line for line in lines if line.strip()]

    # Join the cleaned lines back into a single string
    return '\n'.join(cleaned_lines)
def safety_analyzer(question, retrieve, model_name="gpt-4o-mini"):
    knowledge, target_question, question = intention_detector_with_question_paraphraser(question, retrieve, model_name=model_name)
    input = safe_analyzer_prompt(target_question, question, knowledge)
    print(input)
    output = get_openai_response(input, model_name=model_name)
    output = delete_none_lines(output)
    print(output)
    RAI, guidance = extract_augment_and_guidance(output)
    if  "<" in RAI:
        RAI = "None"
    if  "+" in guidance:
        guidance = "None"
    return question, RAI, guidance
