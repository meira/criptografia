import requests
import json 
import hashlib

request = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=12768e626035a6d4296b9e316aa251154397643e')

json_dados = json.loads(request.content)

caracteres = 'abcdefghijklmnopqrstuvwxyz'
chave = json_dados["numero_casas"]
mensagem_cifrada = json_dados["cifrado"]
mensagem_decifrada = ''

for caractere in mensagem_cifrada:
    if caractere in caracteres:
        numero = caracteres.find(caractere)        
        numero = numero - chave
        if numero >= len(caracteres):
            numero = numero - len(caracteres)
            mensagem_decifrada = mensagem_decifrada + caracteres[numero]
        elif numero < 0:
            numero = numero + len(caracteres)
            mensagem_decifrada = mensagem_decifrada + caracteres[numero]
        else:
            mensagem_decifrada = mensagem_decifrada + caracteres[numero]
    else:
         mensagem_decifrada = mensagem_decifrada + ' '

print('O texto decifrado é ', mensagem_decifrada)

json_dados["mensagem_decifrada"] = mensagem_decifrada

sha1 = hashlib.sha1(mensagem_decifrada.encode())
json_dados["resumo_criptografico"] = sha1.hexdigest()
print(json_dados)

with open("answer.json", "w") as f:
    json.dump(json_dados, f, ensure_ascii=False, indent=4)


answer = {'answer': ('answer.json', open("answer.json", "rb"))}

request = requests.post('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=12768e626035a6d4296b9e316aa251154397643e', file = answer)

print(request.json())