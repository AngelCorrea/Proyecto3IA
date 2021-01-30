import pandas as pd
import string
import nltk

data = pd.read_csv("spam.csv")

nltk.download('stopwords')
nltk.download('punkt')

palabras_vacia = nltk.corpus.stopwords.words('english')
puntuacion = string.punctuation

#Pasamos el texto completamente a minúsculas para después
#quitar las palabras vacías o stopwords, ya que no nos sirven para nada.
def pre_process(text):
    minusculas = "".join([char.lower() for char in text])
    quita_puntuacion = "".join([char for char in minusculas if char not in puntuacion])
    tokenize = nltk.tokenize.word_tokenize(quita_puntuacion)
    quita_palabras_vacia = [word for word in tokenize if word not in palabras_vacia]
    return quita_palabras_vacia

data['processed'] = data['text'].apply(lambda x: pre_process(x))


#Categorizar spam de ham con palabras asociadas, es decir,
#separamos las palabras que se consideran spam de las que se consideran ham.
def categorize_words():
	palabras_spam = []
	palabras_ham = []

	#palabras asociadas a 'spam'
	for sms in data['processed'][data['type'] == 'spam']:
		for word in sms:
			palabras_spam.append(word)

	#palabras asociadas a 'ham' (no spam)
	for sms in data['processed'][data['type'] == 'ham']:
		for word in sms:
			palabras_ham.append(word)

	return palabras_spam, palabras_ham

palabras_spam, palabras_ham = categorize_words();


#Contamos cuantas palabras consideradas spam y cuantas palabras
#consideradas ham tiene la entrada, luego comparamos ambos y
#decide si es spam o no, también puede no saber si es spam.
def predict(user_input):
	contador_spam = 0;
	contador_ham = 0

	for word in user_input:
		contador_spam+= palabras_spam.count(word)
		contador_ham += palabras_ham.count(word)

	print("---------------------------------------------")

	if (contador_ham > contador_spam):
		print('El mensaje no es spam')
	elif (contador_spam > contador_ham):
		print('EL mensaje es spam')
	else:
		print('El mensaje podria ser spam')
	print("---------------------------------------------")

#Informacion de entrada del usuario
user_input = input('Por favor ingrese un mensaje para decidir si es spam o no: \nEscriba -quit para salir\n')

while (user_input != "-quit"):

	procesed_input = pre_process(user_input)

	predict(procesed_input)
	
	user_input = input('Por favor ingrese un mensaje para decidir si es spam o no: \nEscriba -quit para salir\n')



