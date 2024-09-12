import httpx #Importando a biblioteca

#Solicita o nome e verifica se esta dentro do padrão aceitavel para a pesquisa
while True:
    nome = input("Digite seu nome: ")
    if nome.isalpha() == False:
        print("Digite apenas letras!")
        continue
    elif " " in nome:
        print("Digite apenas um nome por vez!")
        continue
    else:
        break


#Faz a busca na API do IBGE usando a biblioteca httpx
nomeF = httpx.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?sexo=F")
nomeM = httpx.get(f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?sexo=M")


#Retorna o json da resposta obtida na API
json_feminino = nomeF.json()
json_masculino = nomeM.json()


#Se o retorno não tiver resultado para o nome escrito, informa ao usuário
if len(json_feminino) == 0 and len(json_masculino) == 0:
    print("Seu nome não possui os requisitos do IBGE!")

#Caso seja um nome dentro dos padrões solicitado da API
else:
    #Com função interna sum, soma todos "item" da 'frequencia' no 'res'
    total_freq_F = sum(item['frequencia'] for item in json_feminino[0]['res'])
    total_freq_M = sum(item['frequencia'] for item in json_masculino[0]['res'])

    #Váriavel para saber o valor da frequencia geral e que representa o todo (100%)
    totalgeral = total_freq_F + total_freq_M

    #Váriaveis para saber a representação do individual dentro do valor total 
    prob_fem = (total_freq_F / totalgeral) * 100
    prob_mas = (total_freq_M / totalgeral) * 100

    if prob_fem == prob_mas:
        print("Um nome provavelmente unissex! 50%")
    elif prob_fem > prob_mas:
        print(f"A chance de {prob_fem: .2f}% de ser um nome do sexo feminino")
    else:
        print(f"A chance de {prob_mas: .2f}% de ser um nome do sexo masculino")
        