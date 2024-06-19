def remove_empty_values(sentences):
    return [value for value in sentences if value != '']


def sent_tokenize(text, dot=True, new_line=True, question_mark=True, exclamation_mark=True):
    """
    This method tokenizes a text into a set of sentences based on the selected separators, including the dot, new line, question mark, and exclamation mark.

    Args:
        text (:obj:`str`): Arabic text to be tokenized.
        dot (:obj:`str`): flag to split text based on Dot (default is True).
        new_line (:obj:`str`): flag to split text based on new_line (default is True).
        question_mark (:obj:`str`): flag to split text based on question_mark (default is True).
        exclamation_mark (:obj:`str`): flag to split text based on exclamation_mark (default is True).

    Returns:
        :obj:`list`: list of sentences.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from nlptools.utils import sentence_tokenizer
        sentences = sentence_tokenizer.sent_tokenize("مختبر سينا لحوسبة اللغة والذكاء الإصطناعي. في جامعة بيرزيت.", dot=True, new_line=True, question_mark=True, exclamation_mark=True)
        print(sentences)

        #output
        ['مختبر سينا لحوسبة اللغة والذكاء الإصطناعي.', 'في جامعة بيرزيت.']
    """
    separators = []
    split_text = [text]
    if new_line==True:
        separators.append('\n')
    if dot==True:
        separators.append('.')
    if question_mark==True:
        separators.append('?')
        separators.append('؟')
    if exclamation_mark==True:
        separators.append('!')
    
    for sep in separators:
        new_split_text = []
        for part in split_text:
            tokens = part.split(sep)
            tokens_with_separator = [token + sep for token in tokens[:-1]]
            tokens_with_separator.append(tokens[-1].strip())
            new_split_text.extend(tokens_with_separator)
        split_text = new_split_text
    
    split_text = remove_empty_values(split_text)    
    return split_text