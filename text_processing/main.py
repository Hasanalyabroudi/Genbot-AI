from text_processing.TextProcessing import TextProcessing

text = 'Hello, my name is hamza'

text_processor = TextProcessing()
text_processor.set_text(text)
print(text_processor.process_text().text)
matrix =(text_processor.CreateWordFrequencyMatrix())
print(matrix['words'][1])
for word, frequency in matrix.values:
    print(f" Word: {word} Frequency: {frequency}")