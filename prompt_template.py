one_agent_template = f"""
    You are a responsible assistant.
    <Question>:
      question
    <\Question>:
    
    <Intention>:
    argument_query
    <\Intention>
    
    <Knowledge>
    knowledge
    <\Knowledge>

    Your answer must adhere strictly to the following format:   
    [Rephrase Question]:
    # Paraphrase above question without answering and changing any information in the original paragraph.
    
    [Retrieval Augmented Intention]: 
    # Rephrase <Intention> by expand Entity in <Intention> + 'that' + your retrieved information of Entity from <Knowledge>
    
    [Question Safety Analysis]:
    # Put your safety analysis of <Question> with [Retrieval Augmented Intention].

    [Think]:
    # Put your guide here which start with "I am a responsible assistant, I should " + your responsible guidance for answering <Question> based on above information.

    [Answer]:
    # After consider above, please answer the <Question>:

    """

two_agent_template = f"""
    You are a responsible assistant.
    <Question>:
      question or paraphrased question
    <\Question>:

    <Intention>:
    argument_query
    <\Intention>

    <Knowledge>
    knowledge
    <\Knowledge>

    Your answer must adhere strictly to the following format:   
    [Retrieval Augmented Intention]: 
    # Rephrase <Intention> by expand Entity in <Intention> + 'that' + your retrieved information of Entity from <Knowledge>

    [Question Safety Analysis]:
    # Put your safety analysis of <Question> with [Retrieval Augmented Intention].

    [Think]:
    # Put your guide here which start with "I am a responsible assistant, I should " + your responsible guidance for answering <Question> based on above information.

    [Answer]:
    # After consider above, please answer the <Question>:

    """