import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")
    while texto:
        textos.append(texto)
        i += 1
        texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()

def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''IMPLEMENTAR. Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    # Recebemos os parametros na função main() do arquivo
    
    soma = 0
    for i in range(len(as_a)):
        soma += abs(as_a[i] - as_b[i])
    similaridade = soma / len(as_a)
    return similaridade

def calcula_assinatura(texto):
    '''IMPLEMENTAR. Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    # Armazena os resultados wal, rtt, hlr, sal, sac, pal, etc...
    assinatura = []
    
    # Declaramos as variaveis com o valor das funções modelos.
    sentences = separa_sentencas(texto)
    palavras = separa_palavras(texto)
    
    #Tiraremos a pontuação de cada palavra e armazenaremos em uma lista "palavras_puras"
    palavras_puras = []
    
    for palavra in palavras:
        palavra = re.sub(r"[^\w\s]", "", palavra)
        palavras_puras.append(palavra)
    #Calculo do "wal"
    tamanho_palavra = 0
    for palavra in palavras_puras:
        tamanho_palavra = tamanho_palavra + len(palavra)
    wal = tamanho_palavra / len(palavras)
    assinatura.append(wal)
    
    # Relação type-token
    ttr = n_palavras_diferentes(palavras_puras)
    ttr = ttr / len(palavras_puras)
    assinatura.append(ttr)
    
    # Razão hapax-legomana
    hlr = n_palavras_unicas(palavras_puras)
    hlr = hlr / len(palavras_puras)
    assinatura.append(hlr)
    
    #Tamanho médio de uma sentença. 
    # Semelhante ao de "palavras" mas aqui iremos contabilizar o char na sentença.
    sentence_pura = []
    
    for sentence in sentences:
        sentence = re.sub(r"[^\w\s]", "", sentence)
        sentence_pura.append(sentence)
    total_char = 0
    for sentence in sentences:
        total_char = total_char + len(sentence)
    sal = total_char / len(sentences)
    assinatura.append(sal)
    
    # Usaremos a mesma estratégia de separar os elementos e append
    # Nesse caso, a variavel frase é atribuida o valor da função "separa_frase".
    # Aproveitamos os resultados anteriores
    frases_lista = []
    
    for sentence in sentences:
        frases = separa_frases(sentence)
        frases_lista.append(frases)
    total_frase = 0
    for frase in frases_lista:
        total_frase += len(frase)
    sac = total_frase / len(sentence_pura)
    assinatura.append(sac)
 
    # Usaremos uma tática similar.
    # Ao invés de criar lista, apenas atribuimos a uma variavel e tiramos o len.
    string = ""
    for frases in frases_lista:
        for frase in frases:
            string += frase
    pal = len(string) / total_frase
    assinatura.append(pal)

    return assinatura

def avalia_textos(textos, ass_cp):
    '''IMPLEMENTAR. Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    # Inicializaremos com ~~pouco_similar irá guardar o menor valor.
    # texto_infectado ira guardar o indice da posição
    pouco_similar = None
    texto_infectado = 0
    #Função "enumerate()" recebe textos da função " le_textos()"
    #Itera sobre lista de "textos" enquanto também mantém o controle do índice de cada [i]. 
    # Ela retorna um objeto enumerado que produz pares de índice e valor. 
    for i, texto in enumerate(textos):
        assinatura = calcula_assinatura(texto)
        similaridade = compara_assinatura(assinatura, ass_cp)
        # Checagem de similaridade.
        if (pouco_similar is None) or (similaridade < pouco_similar):
            pouco_similar = similaridade
            texto_infectado = i +1
    return texto_infectado
#obs.: NO FUTURO PODE-SE MODIFICAR A ENTRADA DE DADOS PARA UM "IF NOT"
def main():
    assinatura_infectado = le_assinatura()  # Passo 1: ler assinatura a ser comparada
    textos = le_textos()                    # Passo 2: ler os textos a serem analisados
    texto_infectado = avalia_textos(textos, assinatura_infectado)  # Passo 3: descobrir o texto mais parecido com a assinatura
    print(f"O autor do texto {texto_infectado} está infectado com COH-PIAH.")
main()