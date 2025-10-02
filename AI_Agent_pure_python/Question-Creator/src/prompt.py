prompt_template = """
You are an expert at creating exam questions from a given text document. 
Your goal is to prepare a student or programmer for their exams and coding tests.
You do this by asking questions about the text below:

------------
  {text}
------------

Create 10 questions that will prepare the students or programmers for their tests.
Make sure not to lose any important information. If there is no text between the dashes line, Do NOT make up any questions.

QUESTIONS:
"""

refined_template = ("""
    You are an expert at creating practice questions based a given text document.
    Your goal is to help a student or programmer prepare for an exam or coding test.
    We have received some practice questions to a certain extent: {existing_answer}.
    We have the option to refine the existing questions or add new ones.
    (only if necessary) with some more context below.
    ------------
    {text}
    ------------

    Given the new context, refine the original questions.
    If the context is not helpful, please provide the original questions.
    If there is no text between the dashes line, Do NOT make up any questions.
    QUESTIONS:
    """
)