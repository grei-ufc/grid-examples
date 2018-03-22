#! coding:utf-8

# Esta é a implementação do cálculo de fluxo de carga de varredura
# direta-inversa utilizando a estrutura de dados do pacote MyGrid

#from mygrid.util import Fasor
#from mygrid.rede import Gerador, NoDeCarga
#from mygrid.rede import Trecho
from mygrid.util import Fasor
from mygrid.rede import Gerador, NoDeCarga
from mygrid.rede import Trecho
from scipy import linalg
import numpy as np


def atribuir_potencia(subestacao, alimentador):
        """ Funcao que atribui potencia negativa em geradores para o calculo do
        fluxo de potencia  """
        for alimentador in subestacao.alimentadores.values():
            # percorre os nos/geradores do sistema
            for nos in alimentador.nos_de_carga.values():
                # se a classe gerador for instanciada, atribui-se a potência
                # negativa ao nó da iteração.
                if isinstance(nos, Gerador):
                	#print nos.nome
                	#print nos.potencia_fase_a.imag
                	if nos.potencia_fase_a.real < 0:
                		pass
                	elif nos.potencia_fase_a > 0:

	                    nos.potencia_fase_a.real = (-1) * nos.potencia_fase_a.real
	                    nos.potencia_fase_b.real = (-1) * nos.potencia_fase_b.real
	                    nos.potencia_fase_c.real = (-1) * nos.potencia_fase_c.real

	                    nos.potencia_fase_a.imag = (-1) * nos.potencia_fase_a.imag
	                    nos.potencia_fase_b.imag = (-1) * nos.potencia_fase_b.imag
	                    nos.potencia_fase_c.imag = (-1) * nos.potencia_fase_c.imag


def tensaogerador(subestacao, alimentador):
        """ Funcao que retorna uma lista com os geradores que nao convergiram,
        a quantidade de geradores e a matriz
            com as diferenças de tennsoes de cada gerador """

        count_fase_a = 0
        count_fase_b = 0
        count_fase_c = 0

        diftensao_fase_a = list()
        diftensao_fase_b = list()
        diftensao_fase_c = list()

        listager_fase_a = list()
        listager_fase_b = list()
        listager_fase_c = list()
        # percorre nos do sistema
        for nos in alimentador.nos_de_carga.values():
            # identifica os geradores do sistema
            if isinstance(nos, Gerador):
                # trata apenas geradores modelados como PV
                if nos.modelo == 'PV':
                    # calcula a diferença entre a tensão calculada com o fluxo
                    # de carga e a tensao do gerador
                    deltav_fase_a = np.array([[nos.tensaogerador - float(nos.tensao_fase_a.mod)]])
                    deltav_fase_b = np.array([[nos.tensaogerador - float(nos.tensao_fase_b.mod)]])
                    deltav_fase_c = np.array([[nos.tensaogerador - float(nos.tensao_fase_c.mod)]])
                    # se a diferença de tensao for maior do que a tolerancia o
                    # gerador será guardado
                    if abs(deltav_fase_a) > nos.dvtol:
                        # guarda as diferenças de tensões dos geradores não
                        # convergidos na lista
                        diftensao_fase_a.append(deltav_fase_a)
                        # guarda o objeto gerador
                        listager_fase_a.append(nos)
                        # incremento que define a quantidade geradores não
                        # convergidos
                        count_fase_a += 1

                    if abs(deltav_fase_b) > nos.dvtol:
                        # guarda as diferenças de tensões dos geradores não
                        # convergidos na lista
                        diftensao_fase_b.append(deltav_fase_b)
                        # guarda o objeto gerador
                        listager_fase_b.append(nos)
                        # incremento que define a quantidade geradores não
                        # convergidos
                        count_fase_b += 1

                    if abs(deltav_fase_c) > nos.dvtol:
                        # guarda as diferenças de tensões dos geradores não
                        # convergidos na lista
                        diftensao_fase_c.append(deltav_fase_c)
                        # guarda o objeto gerador
                        listager_fase_c.append(nos)
                        # incremento que define a quantidade geradores não
                        # convergidos
                        count_fase_c += 1
        # cria um array para auxiliar na formação da matriz
        # das diferenças de tensões
        aux_fase_a = np.array([[]])
        aux_fase_b = np.array([[]])
        aux_fase_c = np.array([[]])
        # caso diftensao seja diferente de vazio, ou seja, existe gerador que não convergiu
        # forma-se a matriz das diferenças de tensões
        if diftensao_fase_a != []:
            # concatena a primeira diferença de tensão com o array auxiliar
            dif_fase_a = np.concatenate((diftensao_fase_a[0], aux_fase_a), axis=1)
            # remove o primeiro elemento deixando apenas o array vazio
            diftensao_fase_a.pop(0)
            # adiciona todos os elementos à matriz de diferença de tensões, incluindo o elemento removido
            for i in diftensao_fase_a:  # for que percorre a lista de array para realizar o restante da concatenação
                dif_fase_a = np.concatenate((dif_fase_a, i))
            diftensao_fase_a = dif_fase_a

        if diftensao_fase_b != []:
            # concatena a primeira diferença de tensão com o array auxiliar
            dif_fase_b = np.concatenate((diftensao_fase_b[0], aux_fase_b), axis=1)
            # remove o primeiro elemento deixando apenas o array vazio
            diftensao_fase_b.pop(0)
            # adiciona todos os elementos à matriz de diferença de tensões, incluindo o elemento removido
            for i in diftensao_fase_b:  # for que percorre a lista de array para realizar o restante da concatenação
                dif_fase_b = np.concatenate((dif_fase_b, i))
            diftensao_fase_b = dif_fase_b

        if diftensao_fase_c != []:
            # concatena a primeira diferença de tensão com o array auxiliar
            dif_fase_c = np.concatenate((diftensao_fase_c[0], aux_fase_c), axis=1)
            # remove o primeiro elemento deixando apenas o array vazio
            diftensao_fase_c.pop(0)
            # adiciona todos os elementos à matriz de diferença de tensões, incluindo o elemento removido
            for i in diftensao_fase_c:  # for que percorre a lista de array para realizar o restante da concatenação
                dif_fase_c = np.concatenate((dif_fase_c, i))
            diftensao_fase_c = dif_fase_c
        # retorna a lista com os geradores a quantidade de geradores e a matriz coluna da diferença de tensões
        return listager_fase_a, count_fase_a, diftensao_fase_a, listager_fase_b, count_fase_b, diftensao_fase_b, listager_fase_c, count_fase_c, diftensao_fase_c


def matrix_reatancia(subestacao, alimentador):
        """funcao que retorna a matriz X para o calculo da matriz de diferença
        de potência reativa """
        # chama a função tensaogerador retornando os geradores não convergidos,
        # bem como o número de geradores
        listageradores_fase_a, numgeradores_fase_a, dVgeradores_fase_a = tensaogerador(subestacao, alimentador)[0], tensaogerador(subestacao, alimentador)[1], tensaogerador(subestacao, alimentador)[2]
        listageradores2_fase_a = tensaogerador(subestacao, alimentador)[0]
        listageradores3_fase_a = tensaogerador(subestacao, alimentador)[0]

        listageradores_fase_b, numgeradores_fase_b, dVgeradores_fase_b = tensaogerador(subestacao, alimentador)[3], tensaogerador(subestacao, alimentador)[4], tensaogerador(subestacao, alimentador)[5]
        listageradores2_fase_b = tensaogerador(subestacao, alimentador)[3]
        listageradores3_fase_b = tensaogerador(subestacao, alimentador)[3]

        listageradores_fase_c, numgeradores_fase_c, dVgeradores_fase_c = tensaogerador(subestacao, alimentador)[6], tensaogerador(subestacao, alimentador)[7], tensaogerador(subestacao, alimentador)[8]
        listageradores2_fase_c = tensaogerador(subestacao, alimentador)[6]
        listageradores3_fase_c = tensaogerador(subestacao, alimentador)[6]
        # declara uma matriz de zero com a dimensão (n x n), onde n é a
        # quantidade de geradores
        xa = np.zeros((numgeradores_fase_a, numgeradores_fase_a))
        xb = np.zeros((numgeradores_fase_b, numgeradores_fase_b))
        xc = np.zeros((numgeradores_fase_c, numgeradores_fase_c))

        aux_fase_a = []
        rem_fase_a = []
        # for para calcular os elementos xij/xji em ordem
        for i in listageradores2_fase_a:
            for j in listageradores3_fase_a:
                # caso i seja igual a j não faz nada, pois são elementos
                # da diagonal principal
                if i.nome == j.nome:
                    pass
                else:
                    # se o elemento já estiver computado não faz nada
                    if j.nome in rem_fase_a:
                        pass
                    else:
                        # guarda em aux o reatancia xij
                        aux_fase_a.append(xij(subestacao, alimentador, i.nome, j.nome))
                        # guarda o nome do elemento visitado para não
                        # utilizá-lo na próxima iteração
                        rem_fase_a.append(i.nome)
        aux_fase_b = []
        rem_fase_b = []
        # for para calcular os elementos xij/xji em ordem
        for i in listageradores2_fase_b:
            for j in listageradores3_fase_b:
                # caso i seja igual a j não faz nada, pois são elementos
                # da diagonal principal
                if i.nome == j.nome:
                    pass
                else:
                    # se o elemento já estiver computado não faz nada
                    if j.nome in rem_fase_b:
                        pass
                    else:
                        # guarda em aux o reatancia xij
                        aux_fase_b.append(xij(subestacao, alimentador, i.nome, j.nome))
                        # guarda o nome do elemento visitado para não
                        # utilizá-lo na próxima iteração
                        rem_fase_b.append(i.nome)
        aux_fase_c = []
        rem_fase_c = []
        # for para calcular os elementos xij/xji em ordem
        for i in listageradores2_fase_c:
            for j in listageradores3_fase_c:
                # caso i seja igual a j não faz nada, pois são elementos
                # da diagonal principal
                if i.nome == j.nome:
                    pass
                else:
                    # se o elemento já estiver computado não faz nada
                    if j.nome in rem_fase_c:
                        pass
                    else:
                        # guarda em aux o reatancia xij
                        aux_fase_c.append(xij(subestacao, alimentador, i.nome, j.nome))
                        # guarda o nome do elemento visitado para não
                        # utilizá-lo na próxima iteração
                        rem_fase_c.append(i.nome)

        # for onde a matriz xa será preenchida
        for i in range(np.shape(xa)[0]):
            for j in range(np.shape(xa)[1]):
                # se é um elemento da diagonal principal
                if i == j:
                    # percorre a primeira lista auxiliar
                    for no in listageradores_fase_a:
                        # atribui a xii atual a reatância
                        xa[i, j] = xii(subestacao, alimentador, no.nome)
                        # remove o nó atual para não utilizado
                        # novamente
                        listageradores_fase_a.remove(no)
                        # quebra o for para não calcular x22, x33..
                        # e substituir no lugar de x11
                        break
                # se é um elemento em que o número da coluna é maior
                # do que a linha
                elif j > i:
                    # faz for na lista com as reatâncias xij obtidas
                    # em ordem
                    for reat in aux_fase_a:
                        # se xij for 0, ou seja, não foi calulado
                        if xa[i, j] == 0:
                            # atribiu-se o valor de reat a xij e xji

                            xa[i, j] = reat[0]
                            xa[j, i] = reat[0]
                            # remove o elemento para não utilizar
                            # novamente
                            aux_fase_a.remove(reat)
                            # quebra o for para não substituir
                            # os valores de outros xij
                            break
                        # se xij for diferente de zero não faz nada
                        else:
                            pass
        # for onde a matriz xb será preenchida
        for i in range(np.shape(xb)[0]):
            for j in range(np.shape(xb)[1]):
                # se é um elemento da diagonal principal
                if i == j:
                    # percorre a primeira lista auxiliar
                    for no in listageradores_fase_b:
                        # atribui a xii atual a reatância
                        xb[i, j] = xii(subestacao, alimentador, no.nome)
                        # remove o nó atual para não utilizado
                        # novamente
                        listageradores_fase_b.remove(no)
                        # quebra o for para não calcular x22, x33..
                        # e substituir no lugar de x11
                        break
                # se é um elemento em que o número da coluna é maior
                # do que a linha
                elif j > i:
                    # faz for na lista com as reatâncias xij obtidas
                    # em ordem
                    for reat in aux_fase_b:
                        # se xij for 0, ou seja, não foi calulado
                        if xb[i, j] == 0:
                            # atribiu-se o valor de reat a xij e xji
                            xb[i, j] = reat[0]
                            xb[j, i] = reat[0]
                            # remove o elemento para não utilizar
                            # novamente
                            aux_fase_b.remove(reat)
                            # quebra o for para não substituir
                            # os valores de outros xij
                            break
                        # se xij for diferente de zero não faz nada
                        else:
                            pass
        # for onde a matriz xc será preenchida
        for i in range(np.shape(xc)[0]):
            for j in range(np.shape(xc)[1]):
                # se é um elemento da diagonal principal
                if i == j:
                    # percorre a primeira lista auxiliar
                    for no in listageradores_fase_c:
                        # atribui a xii atual a reatância
                        xc[i, j] = xii(subestacao, alimentador, no.nome)
                        # remove o nó atual para não utilizado
                        # novamente
                        listageradores_fase_c.remove(no)
                        # quebra o for para não calcular x22, x33..
                        # e substituir no lugar de x11
                        break
                # se é um elemento em que o número da coluna é maior
                # do que a linha
                elif j > i:
                    # faz for na lista com as reatâncias xij obtidas
                    # em ordem
                    for reat in aux_fase_c:
                        # se xij for 0, ou seja, não foi calulado
                        if xc[i, j] == 0:
                            # atribiu-se o valor de reat a xij e xji
                            xc[i, j] = reat[0]
                            xc[j, i] = reat[0]
                            # remove o elemento para não utilizar
                            # novamente
                            aux_fase_c.remove(reat)
                            # quebra o for para não substituir
                            # os valores de outros xij
                            break
                        # se xij for diferente de zero não faz nada
                        else:
                            pass
        return xa, xb, xc


def reativo(subestacao, alimentador):
        """ função que calcula a matriz de diferença de potência reativa dos
        geradores não convergidos, regula a potência injetada/absorvida e
        verifica se o limite de potência reativa inferior ou superior não
        foi alcançada"""

        # calcula a matriz de diferença de potência dos geradores
        # não convergidos
        dq_fase_a = np.dot(linalg.inv(matrix_reatancia(subestacao, alimentador)[0]), tensaogerador(subestacao, alimentador)[2])
        # dq_fase_b = np.dot(linalg.inv(matrix_reatancia(subestacao, alimentador)[1]), tensaogerador(subestacao, alimentador)[5])
        # dq_fase_c = np.dot(linalg.inv(matrix_reatancia(subestacao, alimentador)[2]), tensaogerador(subestacao, alimentador)[8])
        # percorre a lista com geradores para verificar o seu patamar de tensão
        ##print'aqui -> ', type(tensaogerador(subestacao, alimentador)[0][0])

        for dv_fase_a, pot_fase_a, ger_fase_a in zip(tensaogerador(subestacao, alimentador)[2], dq_fase_a, tensaogerador(subestacao, alimentador)[0]):
            # se a diferença de tensão for maior do que zero o gerador
            # aumenta a produção de reativo

            if ger_fase_a.ativo: # adicionado por felipe

                if dv_fase_a > 0:
                    ger_fase_a.potencia_fase_a.imag = ger_fase_a.potencia_fase_a.imag - pot_fase_a[0]
                # se a diferença de tensão for menor do que zero o gerador
                # reduz a produção de reativo
                elif dv_fase_a < 0:
                    ger_fase_a.potencia_fase_a.imag = ger_fase_a.potencia_fase_a.imag +  pot_fase_a[0]
                # se a potência do gerador ultrapassou o seu limite superior
                # atribui-se o limite superior a potência reativa do gerador
                if abs(ger_fase_a.potencia_fase_a.imag) > abs(ger_fase_a.qmax):
                    ger_fase_a.potencia_fase_a.imag = -ger_fase_a.qmax

                # se a potência do gerador ultrapassou o seu limite inferior
                # atribui-se o limite inferior a potência reativa do gerador
                elif abs(ger_fase_a.potencia_fase_a.imag) < abs(ger_fase_a.qmin):
                    ger_fase_a.potencia_fase_a.imag = -ger_fase_a.qmin

            else:

                pass

        # for dv_fase_b, pot_fase_b, ger_fase_b in zip(tensaogerador(subestacao, alimentador)[5], dq_fase_b, tensaogerador(subestacao, alimentador)[3]):
        #     # se a diferença de tensão for maior do que zero o gerador
        #     # aumenta a produção de reativo
        #     if dv_fase_b > 0:
        #         ger_fase_b.potencia_fase_b.imag = ger_fase_b.potencia_fase_b.imag - 3 * pot_fase_b[0]
        #     # se a diferença de tensão for menor do que zero o gerador
        #     # reduz a produção de reativo
        #     elif dv_fase_b < 0:
        #         ger_fase_b.potencia_fase_b.imag = ger_fase_b.potencia_fase_b.imag + 3 * pot_fase_b[0]
        #     # se a potência do gerador ultrapassou o seu limite superior
        #     # atribui-se o limite superior a potência reativa do gerador
        #     if abs(ger_fase_b.potencia_fase_b.imag) > abs(ger_fase_b.qmax):
        #         ger_fase_b.potencia_fase_b.imag = -ger_fase_b.qmax
        #     # se a potência do gerador ultrapassou o seu limite inferior
        #     # atribui-se o limite inferior a potência reativa do gerador
        #     elif abs(ger_fase_b.potencia_fase_b.imag) < abs(ger_fase_b.qmin):
        #         ger_fase_b.potencia_fase_b.imag = -ger_fase_b.qmin

        # for dv_fase_c, pot_fase_c, ger_fase_c in zip(tensaogerador(subestacao, alimentador)[8], dq_fase_c, tensaogerador(subestacao, alimentador)[6]):
        #     # se a diferença de tensão for maior do que zero o gerador
        #     # aumenta a produção de reativo
        #     if dv_fase_c > 0:
        #         ger_fase_c.potencia_fase_c.imag = ger_fase_c.potencia_fase_c.imag - 3 * pot_fase_c[0]
        #     # se a diferença de tensão for menor do que zero o gerador
        #     # reduz a produção de reativo
        #     elif dv_fase_c < 0:
        #         ger_fase_c.potencia_fase_c.imag = ger_fase_c.potencia_fase_b.imag + 3 * pot_fase_c[0]
        #     # se a potência do gerador ultrapassou o seu limite superior
        #     # atribui-se o limite superior a potência reativa do gerador
        #     if abs(ger_fase_c.potencia_fase_c.imag) > abs(ger_fase_c.qmax):
        #         ger_fase_c.potencia_fase_c.imag = -ger_fase_c.qmax
        #     # se a potência do gerador ultrapassou o seu limite inferior
        #     # atribui-se o limite inferior a potência reativa do gerador
        #     elif abs(ger_fase_c.potencia_fase_c.imag) < abs(ger_fase_c.qmin):
        #         ger_fase_c.potencia_fase_c.imag = -ger_fase_c.qmin
        #print dq_fase_a
        return dq_fase_a

def xii(subestacao, alimentador, no_):
        """ função que calcula a reatância de um gerador até o nó raiz """
        # variável que guarda os techos do alimentador
        trechos = alimentador.trechos.values()
        # variável que guarda o caminho do nó até o nó raiz
        caminho = alimentador.arvore_nos_de_carga.caminho_no_para_raiz(no_)[1]
        # faz uma lista do array caminho
        caminho = list(caminho)
        # faz uma lista em outra variável auxiliar
        caminho_2 = list(caminho)
        # lista que servirá para guardar os trechos
        tr = []
        reat = 0
        # for que percorre o caminho
        for no in caminho:
            # for que percorre os trechos
            for trecho in trechos:
                # se o n1 do trecho for igual ao nó atual
                if trecho.n1.nome == no:
                    # se não for uma chave
                    if type(trecho.n2) == NoDeCarga or type(trecho.n2) == Gerador:
                        # se o n2 ta no caminho e o n2 não for o próprio no
                        if trecho.n2.nome in caminho_2 and trecho.n2.nome != no:
                            # adiciona a reatancia do trecho
                            reat += (trecho.comprimento * trecho.condutor.xp)
                            # guarda o trecho
                            tr.append(trecho)
                    # se for uma chave
                    else:
                        # guarda o nó ontem existe a chave
                        no_1 = alimentador.nos_de_carga[no]
                        try:
                            # tenta pegar o próximo nó da iteração
                            no_2 = alimentador.nos_de_carga[caminho_2[1]]
                            # como se está removendo os nós o indice irá variar
                            # para tanto, se houver erro de indice ele continua
                        except IndexError:
                            continue
                        # cria um conjunto com as chaves do nó atual
                        set_1 = set(no_1.chaves)
                        # cria um conjunto com as chaves do nó da próxima
                        # interação
                        set_2 = set(no_2.chaves)
                        # se a interseção das chaves dos nós for
                        # diferente de vazio ele guarda a chave
                        if set_1.intersection(set_2) != set():
                            chave = set_1.intersection(set_2).pop()
                        else:
                            # se a interseção for vazia ele vai para a próxima
                            # iteração
                            continue
                        # caso a chave seja diferente do n2 vai para a próxima
                        # iteração
                        if chave != trecho.n2.nome:
                            continue
                        # percorre os trechos
                        for trech in trechos:
                            # se o n1 for a chave
                            if trech.n1.nome == chave:
                                # guarda o trecho
                                tr.append(trech)
                                # adiciona a reatancia do trecho
                                reat += (trech.comprimento * trech.condutor.xp)
                            # se o n2 for a chave
                            elif trech.n2.nome == chave:
                                # adiciona a reatancia do trecho
                                reat += (trech.comprimento * trech.condutor.xp)
                                # guarda o trecho
                                tr.append(trech)
                # realiza as mesmas lógicas quando o nó é n1
                elif trecho.n2.nome == no:
                    if type(trecho.n1) == NoDeCarga or type(trecho.n1) == Gerador:
                        if trecho.n1.nome in caminho and trecho.n1.nome != no:
                            tr.append(trecho)
                            reat += (trecho.comprimento * trecho.condutor.xp)
                    else:
                        no_1 = alimentador.nos_de_carga[no]

                        try:
                            no_2 = alimentador.nos_de_carga[caminho_2[1]]
                        except IndexError:
                            continue

                        no_2 = alimentador.nos_de_carga[caminho_2[1]]
                        set_1 = set(no_1.chaves)
                        set_2 = set(no_2.chaves)

                        if set_1.intersection(set_2) != set():
                            chave = set_1.intersection(set_2).pop()
                        else:
                            continue

                        if chave != trecho.n1.nome:
                            continue

                        for trech in trechos:
                            if trech.n1.nome == chave:
                                tr.append(trech)
                                reat += (trech.comprimento * trech.condutor.xp)
                            elif trech.n2.nome == chave:
                                tr.append(trech)
                                reat += (trech.comprimento * trech.condutor.xp)
            caminho_2.remove(no)

        return reat

def xij(subestacao, alimentador, no_1, no_2):
        """ função que calcula a reatância de um caminho compartilhado
        por dois geradores da rede """
        # guarda o caminho dos geradores até o nó raiz
        caminho_1 = alimentador.arvore_nos_de_carga.caminho_no_para_raiz(no_1)
        caminho_2 = alimentador.arvore_nos_de_carga.caminho_no_para_raiz(no_2)
        # variáveis auxiliares
        max_prof = 0
        no_max = None
        # faz for na lista de nos e na lista de profundidade
        for i, ix in zip(caminho_1[1, :], caminho_1[0, :]):
            for j, jx in zip(caminho_2[1, :], caminho_2[0, :]):
                # caso se encontro o nó de interseção das duas listas
                if i == j:
                    # se a profundidade for maior do que a máxima
                    if int(ix) > max_prof:
                        # atribui a max_prof a profundidade atual
                        max_prof = int(ix)
                        # atribui ao no_max o no de menor profundidade
                        no_max = i
        
        return xii(subestacao, alimentador, no_max), no_max            

def calcular_fluxo_de_carga(subestacao):

        trafos = subestacao.transformadores.keys()
        T1 = subestacao.transformadores[trafos[0]]

        # atribui a tensão de fase da barra da subestação a todos
        # os nós de carga da subestação
        f1 = Fasor(mod=T1.tensao_secundario.mod , ang=0.0, tipo=Fasor.Tensao)
        _atribuir_tensao_a_subestacao(subestacao, f1)

        for alimentador in subestacao.alimentadores.values():
            # atribui potência negativa para os geradores da rede
            atribuir_potencia(subestacao, alimentador)
            # chama o método para a realização do backward/forward

            fim = 0
            while fim == 0:

                max_iteracoes = 500         
                criterio_converg = 0.01
                converg = 1e6
                iter = 0                    # alteração feita por felipe 


                #print'================='
                #print'Varredura no alimentador {al}'.format(al=alimentador.nome)

                converg_nos_fase_a = dict()
                converg_nos_fase_b = dict()
                converg_nos_fase_c = dict()

                for no in alimentador.nos_de_carga.values():

                    converg_nos_fase_a[no.nome] = 1e6
                    converg_nos_fase_b[no.nome] = 1e6
                    converg_nos_fase_c[no.nome] = 1e6

                # testa se o máximo de iterações foi alcançada e a convergência
                while iter <= max_iteracoes and converg > criterio_converg:

                    iter += 1
                    #print'-------------------------'
                    #print'Iteração: {iter}'.format(iter=iter)
                    # dicionário que guarda o nome dos nós na chave a suas tensões nos valores
                    tensao_nos_fase_a = dict()
                    tensao_nos_fase_b = dict()
                    tensao_nos_fase_c = dict()
                    for no in alimentador.nos_de_carga.values():
                        tensao_nos_fase_a[no.nome] = Fasor(real=no.tensao_fase_a.real,
                                                           imag=no.tensao_fase_a.imag,
                                                           tipo=Fasor.Tensao)
                        tensao_nos_fase_b[no.nome] = Fasor(real=no.tensao_fase_b.real,
                                                           imag=no.tensao_fase_b.imag,
                                                           tipo=Fasor.Tensao)
                        tensao_nos_fase_c[no.nome] = Fasor(real=no.tensao_fase_c.real,
                                                           imag=no.tensao_fase_c.imag,
                                                           tipo=Fasor.Tensao)
                    # varre o alimentador calculado as potências e as tensões
                    _varrer_alimentador(subestacao, alimentador)
                    # faz a diferença entre os valores de tensões passados e valores de
                    # tensões atuais para verificar a convergência
                    for no in alimentador.nos_de_carga.values():
                        converg_nos_fase_a[no.nome] = abs(tensao_nos_fase_a[no.nome].mod - no.tensao_fase_a.mod)
                        converg_nos_fase_b[no.nome] = abs(tensao_nos_fase_b[no.nome].mod - no.tensao_fase_b.mod)
                        converg_nos_fase_c[no.nome] = abs(tensao_nos_fase_c[no.nome].mod - no.tensao_fase_c.mod)
                    
                    # toma o valor máximo de diferença de tensão para todos os nós da rede
                    converg_fase_a = max(converg_nos_fase_a.values())
                    converg_fase_b = max(converg_nos_fase_b.values())
                    converg_fase_c = max(converg_nos_fase_c.values())

                    converg = max(converg_fase_a, converg_fase_b, converg_fase_c)
                    #print 'converg: ', converg

                    if iter > max_iteracoes:

                        fim = 1
                        #print'Numero maximo de iteracoes atingidas'

                    else:
                        # armazena lista com os geradores, a quantidade deles e a
                        # matriz  com a diferença de tensão em cada um

                        convergaux = []
                        for no in alimentador.nos_de_carga.values():
                            dv = 0
                            if no.modelo == 'PV':
                                if no.ativo: # adicionado por felipe
                                    dv = abs(no.tensaogerador - float(no.tensao_fase_a.mod))
                                    if dv > no.dvtol:
                                        convergaux.append(no)
                                        ##print 'convergaux: ', convergaux
                                else:
                                    pass      
                       
                        if convergaux == []:
                            fim = 1
                            #print'CONVERGIU'
                        else:
                            # calculo do reativo para os geradores
                            reativo(subestacao, alimentador)                        

                    '''Parte do código escrita pelo Felipe: Solucao para o problema de loop infinito quando as maquinas atingiam o limite maximo de reativo'''
             		
                    """rotina para buscar os geradores conectados ao alimentador"""
                    gdlist = list()
                    for no in alimentador.nos_de_carga.values():
                    	if isinstance(no,Gerador):
                    		gdlist.append(no)

                    qlimits_count = 0 # variavel que armazena a quantidade de gds que ultrapassaram os limites de reativos
                    """rotina que procura dentre as gds do alimentador, se alguma já atingiu os limites de geracao de reativos"""
                    for gd in gdlist:
                        #print gd.nome, gd.potencia_fase_a.imag
                        if abs(gd.potencia_fase_a.imag) == abs(gd.qmax):
                            #print'O gerador ' + gd.nome + ' atingiu o máximo de potência reativa'
                            qlimits_count = qlimits_count + 1

                        if abs(gd.potencia_fase_a.imag) == abs(gd.qmin):
                            #print'O gerador ' + gd.nome + ' atingiu o mínimo de potência reativa'
                            qlimits_count = qlimits_count + 1

                    """verifica se todas as gds do alimentador já ultrapassaram os limites de geração de reativos"""
                    if qlimits_count == len(gdlist):
                        #print'Todos os geradores do alimentador ' + alimentador.nome + ' atingiram os limites de geracao de reativos' 
                        fim = 1
                        qlimits_count = 0
                        gdlist=list()
                        break

        correnteIED(subestacao) # adicionado por felipe

def _busca_trecho(subestacao, alimentador, n1, n2):
        """Função que busca trechos em um alimendador entre os nós/chaves
          n1 e n2"""
        # for pecorre os nos de carga do alimentador
        for no in alimentador.nos_de_carga.keys():

            # cria conjuntos das chaves ligadas ao no
            chaves_n1 = set(alimentador.nos_de_carga[n1].chaves)
            chaves_n2 = set(alimentador.nos_de_carga[n2].chaves)

            # verifica se existem chaves comuns aos nos
            chaves_intersec = chaves_n1.intersection(chaves_n2)

            if chaves_intersec != set():
                # verifica quais trechos estão ligados a chave
                # comum as nós.
                chave = chaves_intersec.pop()
                trechos_ch = []
                # identificação dos trechos requeridos
                for trecho in alimentador.trechos.values():
                    if trecho.n1.nome == chave:
                        if trecho.n2.nome == n1 or trecho.n2.nome == n2:
                            trechos_ch.append(trecho)
                    elif trecho.n2.nome == chave:
                        if trecho.n1.nome == n1 or trecho.n1.nome == n2:
                            trechos_ch.append(trecho)
                # caso o comprimento da lista seja dois, ou seja, há chave
                # entre dois ós de carga, a função retorna os trechos.
                if len(trechos_ch) == 2:
                    return trechos_ch
            else:
                # se não existirem chaves comuns, verifica qual trecho
                # tem os nos n1 e n2 como extremidade
                for trecho in alimentador.trechos.values():
                    if trecho.n1.nome == n1:
                        if trecho.n2.nome == n2:
                            return trecho
                    elif trecho.n1.nome == n2:
                        if trecho.n2.nome == n1:
                            return trecho

def _atribuir_tensao_a_subestacao(subestacao, tensao):
    """ Função que atribui tensão à subestação
     e a define para todos os nós de carga"""
    subestacao.tensao = tensao
    for alimentador in subestacao.alimentadores.values():
        for no in alimentador.nos_de_carga.values():
            no.tensao_fase_a = Fasor(real=tensao.real,
                                     imag=tensao.imag,
                                     tipo=Fasor.Tensao)
            no.tensao_fase_b = Fasor(real=tensao.real,
                                     imag=tensao.imag,
                                     tipo=Fasor.Tensao)
            no.tensao_fase_c = Fasor(real=tensao.real,
                                     imag=tensao.imag,
                                     tipo=Fasor.Tensao)


def _varrer_alimentador(subestacao, alimentador):
    """ Função que varre os alimentadores pelo
    método varredura direta/inversa"""

    # guarda os nós de carga na variável nos_alimentador
    nos_alimentador = alimentador.nos_de_carga.values()

    # guarda a rnp dos nós de carga na variável rnp_alimentador
    rnp_alimentador = alimentador.arvore_nos_de_carga.rnp

    # guarda a árvore de cada nós de carga
    arvore_nos_de_carga = alimentador.arvore_nos_de_carga.arvore

    # variáveis para o auxílio na determinação do nó mais profundo
    prof_max = 0

    # for percorre a rnp dos nós de carga tomando valores
    # em pares (profundidade, nó).
    for no_prof in rnp_alimentador.transpose():
        # pega os nomes dos nós de carga.
        nos_alimentador_nomes = [no.nome for no in nos_alimentador]

        # verifica se a profundidade do nó é maior do que a
        # profundidade máxima e se ele está na lista de nós do alimentador.
        if (int(no_prof[0]) > prof_max) \
           and (no_prof[1] in nos_alimentador_nomes):
            prof_max = int(no_prof[0])

    # prof recebe a profundidae máxima determinada
    prof = prof_max
    # seção do cálculo das potências partindo dos
    # nós com maiores profundidades até o nó raíz
    while prof >= 0:
        # guarda os nós com maiores profundidades.
        nos = [alimentador.nos_de_carga[no_prof[1]]
               for no_prof in rnp_alimentador.transpose() if
               int(no_prof[0]) == prof]

        # decrementodo da profundidade.
        prof -= 1

        # for que percorre os nós com a profundidade
        # armazenada na variável prof
        for no in nos:
            # zera as potências para que na próxima
            # iteração não ocorra acúmulo.
            no.potencia_eq_fase_a.real = 0.0
            no.potencia_eq_fase_b.real = 0.0
            no.potencia_eq_fase_c.real = 0.0

            no.potencia_eq_fase_a.imag = 0.0
            no.potencia_eq_fase_b.imag = 0.0
            no.potencia_eq_fase_c.imag = 0.0

            # armazena a árvore do nó de carga
            # armazenado na variável nó
            vizinhos = arvore_nos_de_carga[no.nome]

            # guarda os pares (profundidade, nó)
            no_prof = [no_prof for no_prof in rnp_alimentador.transpose()
                       if no_prof[1] == no.nome]
            vizinhos_jusante = list()

            # for que percorre a árvore de cada nó de carga
            for vizinho in vizinhos:
                # verifica quem é vizinho do nó desejado.
                vizinho_prof = [viz_prof for viz_prof in
                                rnp_alimentador.transpose()
                                if viz_prof[1] == vizinho]

                # verifica se a profundidade do vizinho é maior
                if int(vizinho_prof[0][0]) > int(no_prof[0][0]):
                    # armazena os vizinhos a jusante.
                    vizinhos_jusante.append(
                        alimentador.nos_de_carga[vizinho_prof[0][1]])

            # verifica se não há vizinho a jusante,
            # se não houverem o nó de carga analisado
            # é o último do ramo.
            if vizinhos_jusante == []:
                if no.modelo == 'PQ' or no.modelo == 'PV':

                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag

                elif no.modelo == 'I_const':

                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real * \
                        no.tensao_fase_a.mod / 13800
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real * \
                        no.tensao_fase_b.mod / 13800
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real * \
                        no.tensao_fase_c.mod / 13800

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag * \
                        no.tensao_fase_a.mod / 13800
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag * \
                        no.tensao_fase_b.mod / 13800
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag * \
                        no.tensao_fase_c.mod / 13800

                elif no.modelo == 'Z_const':

                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real * \
                        no.tensao_fase_a.mod ** 2 / 13800
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real * \
                        no.tensao_fase_b.mod ** 2 / 13800
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real * \
                        no.tensao_fase_c.mod ** 2 / 13800

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag * \
                        no.tensao_fase_a.mod ** 2 / 13800 ** 2
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag * \
                        no.tensao_fase_b.mod ** 2 / 13800 ** 2
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag * \
                        no.tensao_fase_c.mod ** 2 / 13800 ** 2

            else:
                # soma a potencia da carga associada ao nó atual
                if no.modelo == 'PQ' or no.modelo == 'PV':
                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag

                elif no.modelo == 'I_const':

                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real * \
                        no.tensao_fase_a.mod / 13800
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real * \
                        no.tensao_fase_b.mod / 13800
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real * \
                        no.tensao_fase_c.mod / 13800

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag * \
                        no.tensao_fase_a.mod / 13800
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag * \
                        no.tensao_fase_b.mod / 13800
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag * \
                        no.tensao_fase_c.mod / 13800

                elif no.modelo == 'Z_const':

                    no.potencia_eq_fase_a.real += no.potencia_fase_a.real * \
                        no.tensao_fase_a.mod ** 2 / 13800
                    no.potencia_eq_fase_b.real += no.potencia_fase_b.real * \
                        no.tensao_fase_b.mod ** 2 / 13800
                    no.potencia_eq_fase_c.real += no.potencia_fase_c.real * \
                        no.tensao_fase_c.mod ** 2 / 13800

                    no.potencia_eq_fase_a.imag += no.potencia_fase_a.imag * \
                        no.tensao_fase_a.mod ** 2 / 13800 ** 2
                    no.potencia_eq_fase_b.imag += no.potencia_fase_b.imag * \
                        no.tensao_fase_b.mod ** 2 / 13800 ** 2
                    no.potencia_eq_fase_c.imag += no.potencia_fase_c.imag * \
                        no.tensao_fase_c.mod ** 2 / 13800 ** 2
                # acrescenta à potência do nó atual
                # as potências dos nós a jusante
                for no_jus in vizinhos_jusante:
                    no.potencia_eq_fase_a.real += no_jus.potencia_eq_fase_a.\
                        real
                    no.potencia_eq_fase_b.real += no_jus.potencia_eq_fase_b.\
                        real
                    no.potencia_eq_fase_c.real += no_jus.potencia_eq_fase_c.\
                        real

                    no.potencia_eq_fase_a.imag += no_jus.potencia_eq_fase_a.\
                        imag
                    no.potencia_eq_fase_b.imag += no_jus.potencia_eq_fase_b.\
                        imag
                    no.potencia_eq_fase_c.imag += no_jus.potencia_eq_fase_c.\
                        imag

                    # chama a função busca_trecho para definir
                    # quais trechos estão entre o nó atual e o nó a jusante
                    trecho = _busca_trecho(subestacao,
                    					   alimentador,
                                           no.nome,
                                           no_jus.nome)
                    # se o trecho não for uma instancia da classe
                    # Trecho(quando há chave entre nós de cargas)
                    # a impedância é calculada    
                    if not isinstance(trecho, Trecho):
                        r1, x1 = trecho[0].calcula_impedancia()
                        r2, x2 = trecho[1].calcula_impedancia()
                        r, x = r1 + r2, x1 + x2
                    # se o trecho atual for uma instancia da classe trecho
                    else:
                        r, x = trecho.calcula_impedancia()
                        # calculo das potências dos nós de carga a jusante.
                no.potencia_eq_fase_a.real += r * (no_jus.potencia_eq_fase_a.mod ** 2) / \
                    no_jus.tensao_fase_a.mod ** 2
                no.potencia_eq_fase_b.real += r * (no_jus.potencia_eq_fase_b.mod ** 2) / \
                    no_jus.tensao_fase_b.mod ** 2
                no.potencia_eq_fase_c.real += r * (no_jus.potencia_eq_fase_c.mod ** 2) / \
                    no_jus.tensao_fase_c.mod ** 2

                no.potencia_eq_fase_a.imag += x * (no_jus.potencia_eq_fase_a.mod ** 2) / \
                    no_jus.tensao_fase_a.mod ** 2
                no.potencia_eq_fase_b.imag += x * (no_jus.potencia_eq_fase_b.mod ** 2) / \
                    no_jus.tensao_fase_b.mod ** 2
                no.potencia_eq_fase_c.imag += x * (no_jus.potencia_eq_fase_c.mod ** 2) / \
                    no_jus.tensao_fase_c.mod ** 2

    prof = 0
    # seção do cálculo de atualização das tensões
    while prof <= prof_max:
        # salva os nós de carga a montante
        nos = [alimentador.nos_de_carga[col_no_prof[1]]
               for col_no_prof in rnp_alimentador.transpose()
               if int(col_no_prof[0]) == prof + 1]
        # percorre os nós para guardar a árvore do nó requerido
        for no in nos:
            vizinhos = arvore_nos_de_carga[no.nome]
            # guarda os pares (profundidade,nó)
            no_prof = [col_no_prof
                       for col_no_prof in rnp_alimentador.transpose()
                       if col_no_prof[1] == no.nome]
            vizinhos_montante = list()
            # verifica quem é vizinho do nó desejado.
            for vizinho in vizinhos:
                vizinho_prof = [viz_prof
                                for viz_prof in rnp_alimentador.transpose()
                                if viz_prof[1] == vizinho]
                if int(vizinho_prof[0][0]) < int(no_prof[0][0]):
                    # armazena os vizinhos a montante.
                    vizinhos_montante.append(
                        alimentador.nos_de_carga[vizinho_prof[0][1]])
            # armazena o primeiro vizinho a montante
            no_mon = vizinhos_montante[0]
            trecho = _busca_trecho(subestacao, alimentador, no.nome, no_mon.nome)
            # se existir chave, soma a resistência dos dois trechos
            if not isinstance(trecho, Trecho):

                r1, x1 = trecho[0].calcula_impedancia()
                r2, x2 = trecho[1].calcula_impedancia()
                r, x = r1 + r2, x1 + x2
            # caso não exista, a resistência é a do próprio trecho
            else:
                r, x = trecho.calcula_impedancia()

            v_mon_fase_a = no_mon.tensao_fase_a.mod
            v_mon_fase_b = no_mon.tensao_fase_b.mod
            v_mon_fase_c = no_mon.tensao_fase_c.mod

            pa = no.potencia_eq_fase_a.real
            pb = no.potencia_eq_fase_b.real
            pc = no.potencia_eq_fase_c.real

            qa = no.potencia_eq_fase_a.imag
            qb = no.potencia_eq_fase_b.imag
            qc = no.potencia_eq_fase_c.imag

            # parcela de perdas
            pa += r * (no.potencia_eq_fase_a.mod ** 2) / no.tensao_fase_a.\
                mod ** 2
            pb += r * (no.potencia_eq_fase_b.mod ** 2) / no.tensao_fase_b.\
                mod ** 2
            pc += r * (no.potencia_eq_fase_c.mod ** 2) / no.tensao_fase_c.\
                mod ** 2

            qa += x * (no.potencia_eq_fase_a.mod ** 2) / no.tensao_fase_a.\
                mod ** 2
            qb += x * (no.potencia_eq_fase_b.mod ** 2) / no.tensao_fase_b.\
                mod ** 2
            qc += x * (no.potencia_eq_fase_c.mod ** 2) / no.tensao_fase_c.\
                mod ** 2

            v_jus_fase_a = v_mon_fase_a ** 2 - 2 * (r * pa + x * qa) + \
                (r ** 2 + x ** 2) * (pa ** 2 + qa ** 2) / v_mon_fase_a ** 2
            v_jus_fase_b = v_mon_fase_b ** 2 - 2 * (r * pb + x * qb) + \
                (r ** 2 + x ** 2) * (pb ** 2 + qb ** 2) / v_mon_fase_b ** 2
            v_jus_fase_c = v_mon_fase_c ** 2 - 2 * (r * pc + x * qc) + \
                (r ** 2 + x ** 2) * (pc ** 2 + qc ** 2) / v_mon_fase_c ** 2

            v_jus_fase_a = np.sqrt(v_jus_fase_a)
            v_jus_fase_b = np.sqrt(v_jus_fase_b)
            v_jus_fase_c = np.sqrt(v_jus_fase_c)

            k1a = (pa * x - qa * r) / v_mon_fase_a
            k1b = (pb * x - qb * r) / v_mon_fase_b
            k1c = (pc * x - qc * r) / v_mon_fase_c

            k2a = v_mon_fase_a - (pa * r - qa * x) / v_mon_fase_a
            k2b = v_mon_fase_b - (pb * r - qb * x) / v_mon_fase_b
            k2c = v_mon_fase_c - (pc * r - qc * x) / v_mon_fase_c

            ang_a = no_mon.tensao_fase_a.ang * np.pi / 180.0 - np.arctan \
                (k1a / k2a)
            ang_b = no_mon.tensao_fase_b.ang * np.pi / 180.0 - np.arctan \
                (k1b / k2b)
            ang_c = no_mon.tensao_fase_c.ang * np.pi / 180.0 - np.arctan \
                (k1c / k2c)

            no.tensao_fase_a.mod = v_jus_fase_a
            no.tensao_fase_b.mod = v_jus_fase_b
            no.tensao_fase_c.mod = v_jus_fase_c

            no.tensao_fase_a.ang = ang_a * 180.0 / np.pi
            no.tensao_fase_b.ang = ang_b * 180.0 / np.pi
            no.tensao_fase_c.ang = ang_c * 180.0 / np.pi

            # 'Tensao do no {nome}: {tens}'.format(nome=no.nome, tens=no.tensao.mod/1e3)

            # calcula o fluxo de corrente passante no trecho
            corrente_fase_a = no.tensao_fase_a.real - no_mon.tensao_fase_a.real
            corrente_fase_b = no.tensao_fase_b.real - no_mon.tensao_fase_b.real
            corrente_fase_c = no.tensao_fase_c.real - no_mon.tensao_fase_c.real

            corrente_fase_a += (no.tensao_fase_a.imag - no_mon.tensao_fase_a.imag) * 1.0j
            corrente_fase_b += (no.tensao_fase_b.imag - no_mon.tensao_fase_b.imag) * 1.0j
            corrente_fase_c += (no.tensao_fase_c.imag - no_mon.tensao_fase_c.imag) * 1.0j

            corrente_fase_a /= ((r + x * 1.0j) * np.sqrt(3) )
            corrente_fase_b /= ((r + x * 1.0j) * np.sqrt(3) ) 
            corrente_fase_c /= ((r + x * 1.0j) * np.sqrt(3) )
            # se houver chaves, ou seja, há dois trechos a mesma corrente
            # é atribuida
            if not isinstance(trecho, Trecho):
                trecho[0].fluxo_fase_a = Fasor(real=corrente_fase_a.real,
                                               imag=corrente_fase_a.imag,
                                               tipo=Fasor.Corrente)
                trecho[0].fluxo_fase_b = Fasor(real=corrente_fase_b.real,
                                               imag=corrente_fase_b.imag,
                                               tipo=Fasor.Corrente)
                trecho[0].fluxo_fase_c = Fasor(real=corrente_fase_c.real,
                                               imag=corrente_fase_c.imag,
                                               tipo=Fasor.Corrente)

                trecho[1].fluxo_fase_a = Fasor(real=corrente_fase_a.real,
                                               imag=corrente_fase_a.imag,
                                               tipo=Fasor.Corrente)
                trecho[1].fluxo_fase_b = Fasor(real=corrente_fase_b.real,
                                               imag=corrente_fase_b.imag,
                                               tipo=Fasor.Corrente)
                trecho[1].fluxo_fase_c = Fasor(real=corrente_fase_c.real,
                                               imag=corrente_fase_c.imag,
                                               tipo=Fasor.Corrente)
            else:
                trecho.fluxo_fase_a = Fasor(real=corrente_fase_a.real,
                                            imag=corrente_fase_a.imag,
                                            tipo=Fasor.Corrente)
                trecho.fluxo_fase_b = Fasor(real=corrente_fase_b.real,
                                            imag=corrente_fase_b.imag,
                                            tipo=Fasor.Corrente)
                trecho.fluxo_fase_c = Fasor(real=corrente_fase_c.real,
                                            imag=corrente_fase_c.imag,
                                            tipo=Fasor.Corrente)
        prof += 1

def correnteIED(subestacao): # adicionado por felipe

    for alimentador in subestacao.alimentadores.values():
        for chave in alimentador.chaves.values():

            for trecho in alimentador.trechos.values():

                if trecho.n1 == chave or trecho.n2 == chave:
                    chave.ied.corrente = trecho.fluxo_fase_a.mod
                    break



