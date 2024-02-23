from nltk import RegexpTokenizer

class Text_tokenizer:
    def __init__(self):
        """Tokenize Text
        
        Split a text into separate words.
        
        Use:    tokenizer = Text_tokenizer("tu es l'amour de ma vie")
                token = tokenizer.tokenize()
                print(token)
                >>> ["tu", "es", "l'", "amour", "de", "ma", "vie"]

        Args:
            text_input (str): The text you want to tokenize as a string.
        """
        
        
                

    def tokenize(self, text_input:str):
        """Tokenize Text
        
        Split a text into separate words.
        
        Use:    tokenizer = Text_tokenizer("tu es l'amour de ma vie")
                token = tokenizer.tokenize()
                print(token)
                >>> ["tu", "es", "l'", "amour", "de", "ma", "vie"]

        Args:
            text_input (str): The text you want to tokenize as a string.
        """
        toknizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
        tokens = toknizer.tokenize(text_input)
        #tokens = [x.lower() for x in tokens]
        return tokens
    
    

if __name__ == '__main__':
    token = Text_tokenizer("Tu es l'amour de ma vie.")
    tokens = token.tokenize()
    print(tokens)
    