#! coding=utf-8

# Esta é a implementação do cálculo de curto circuito
# utilizando a estrutura de dados do pacote MyGrid

import numpy as np
from scipy import linalg
from random import randint
from mygrid.util import Fasor, Base
from mygrid.rede import Gerador, NoDeCarga
from mygrid.rede import Trecho
from mygrid.rnp import Arvore, Aresta
from mygrid.fluxo_de_carga.varred_dir_inv_gd import xij

def zno_noraiz(subestacao, alimentador, no_):

		""" função que calcula a impedancia de um nó até o nó raiz """
		
		# variável que guarda os techos do alimentador
		trechos = alimentador.trechos.values()
		# variável que guarda o caminho do nó até o nó raiz
		# print "teste"
		caminho = alimentador.arvore_nos_de_carga.caminho_no_para_raiz(no_)[1]
		# faz uma lista do array caminho
		caminho = list(caminho)
		# faz uma lista em outra variável auxiliar
		caminho_2 = list(caminho)
		# lista que servirá para guardar os trechos
		tr = []
		reat1 = 0
		res1 = 0
		reat0 = 0
		res0 = 0
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
							reat1 += (trecho.comprimento * trecho.condutor.xp)
							res1 += (trecho.comprimento * trecho.condutor.rp)
							
							
							reat0 += (trecho.comprimento * trecho.condutor.xz)
							res0 += (trecho.comprimento * trecho.condutor.rz)
							
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
								reat1 += (trech.comprimento * trech.condutor.xp)
								res1 += (trech.comprimento * trech.condutor.rp)
								
								
								reat0 += (trech.comprimento * trech.condutor.xz)
								res0 += (trech.comprimento * trech.condutor.rz)
								
								
							# se o n2 for a chave
							elif trech.n2.nome == chave:
								# adiciona a reatancia do trecho
								reat1 += (trech.comprimento * trech.condutor.xp)
								res1 += (trech.comprimento * trech.condutor.rp)
								
								
								reat0 += (trech.comprimento * trech.condutor.xz)
								res0 += (trech.comprimento * trech.condutor.rz)
								
								
								
								# guarda o trecho
								tr.append(trech)
				# realiza as mesmas lógicas quando o nó é n1
				elif trecho.n2.nome == no:
					if type(trecho.n1) == NoDeCarga or type(trecho.n1) == Gerador:
						if trecho.n1.nome in caminho and trecho.n1.nome != no:
							tr.append(trecho)
							reat1 += (trecho.comprimento * trecho.condutor.xp)
							res1 += (trecho.comprimento * trecho.condutor.rp)
							
							
							reat0 += (trecho.comprimento * trecho.condutor.xz)
							res0 += (trecho.comprimento * trecho.condutor.rz)
							
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
								
								reat1 += (trech.comprimento * trech.condutor.xp)
								res1 += (trech.comprimento * trech.condutor.rp)
								
								
								reat0 += (trech.comprimento * trech.condutor.xz)
								res0 += (trech.comprimento * trech.condutor.rz)
																
							elif trech.n2.nome == chave:
								tr.append(trech)
								reat1 += (trech.comprimento * trech.condutor.xp)
								res1 += (trech.comprimento * trech.condutor.rp)

								reat0 += (trech.comprimento * trech.condutor.xz)
								res0 += (trech.comprimento * trech.condutor.rz)

			caminho_2.remove(no)

		base2 = subestacao.tensaosaida**2 * subestacao.sbase**-1
		trafos = list()
		for trafo in subestacao.transformadores.values():
			for ali in trafo.alimentadores.values():
				if ali == alimentador:
					trafos.append(trafo)
				else:
					pass
		raux = 0.0
		xaux = 0.0
		zaux = 0.0 + 0.0j
		for trafo in trafos:
			raux = trafo.r1 * (subestacao.sbase / trafo.potencia.mod) * (trafo.tensao_primario.mod / subestacao.tensaoentrada) ** 2
			xaux = trafo.x1 * (subestacao.sbase / trafo.potencia.mod) * (trafo.tensao_primario.mod / subestacao.tensaoentrada) ** 2        	
			zaux += 1 * (raux + 1.0j * xaux) ** -1
		zaux = zaux**-1
		
		estrela = False
		for trafo in subestacao.transformadores.values():
			if trafo.ligacao_secundario == 'estrela_aterrado':
				estrela = True
			else:
				pass
		if estrela == True:
			r0pu = (res0 / base2) + zaux.real
			x0pu = (reat0 / base2) + zaux.imag

			r1pu = (res1 / base2) + zaux.real + subestacao.impedancia_equivalente_positiva.real
			x1pu = (reat1 / base2) + zaux.imag + subestacao.impedancia_equivalente_positiva.imag

			z1pu = (r1pu**2 + x1pu**2)**0.5
			z0pu = (r0pu**2 + x0pu**2)**0.5
		elif estrela == False:
			r1pu = (res1 / base2) + zaux.real + subestacao.impedancia_equivalente_positiva.real
			x1pu = (reat1 / base2) + zaux.imag + subestacao.impedancia_equivalente_positiva.imag
						
			r0pu = (res0 / base2) + zaux.real + subestacao.impedancia_equivalente_zero.real
			x0pu = (reat0 / base2) + zaux.imag + subestacao.impedancia_equivalente_zero.imag

			z1pu = (r1pu**2 + x1pu**2)**0.5
			z0pu = (r0pu**2 + x0pu**2)**0.5       

		return r0pu, x0pu, r1pu, x1pu, z0pu, z1pu

def zno_no(subestacao, alimentador, no1, no2):
		""" função que calcula a impedancia de um nó até o nó raiz """
		# variável que guarda os techos do alimentador
		# pega as resistências, reatâncias e impedâncias para o nó1
		raiz = alimentador.arvore_nos_de_carga.raiz
		if no1 == raiz:
			return zno_noraiz(subestacao, alimentador, no2)
		elif no2 == raiz:
			return zno_noraiz(subestacao, alimentador, no1)

		else:
			
			r0no1 = zno_noraiz(subestacao, alimentador, no1)[0]
			x0no1 = zno_noraiz(subestacao, alimentador, no1)[1]

			r1no1 = zno_noraiz(subestacao, alimentador, no1)[2]
			x1no1 = zno_noraiz(subestacao, alimentador, no1)[3]

			z0no1 = zno_noraiz(subestacao, alimentador, no1)[4]
			z1no1 = zno_noraiz(subestacao, alimentador, no1)[5]

			# pega as resistências, reatâncias e impedâncias para o nó2
			r0no2 = zno_noraiz(subestacao, alimentador, no2)[0]
			x0no2 = zno_noraiz(subestacao, alimentador, no2)[1]

			r1no2 = zno_noraiz(subestacao, alimentador, no2)[2]
			x1no2 = zno_noraiz(subestacao, alimentador, no2)[3]

			z0no2 = zno_noraiz(subestacao, alimentador, no2)[4]
			z1no2 = zno_noraiz(subestacao, alimentador, no2)[5]

			# pega o nó comum entre o caminho do nó1 e o nó2
			nocomum = xij(subestacao, alimentador, no1, no2)[1]

			# calcula as resistências, reatâncias e impedâncias para o nó comum
			r0nocomum = zno_noraiz(subestacao, alimentador, nocomum)[0]
			x0nocomum = zno_noraiz(subestacao, alimentador, nocomum)[1]

			r1nocomum = zno_noraiz(subestacao, alimentador, nocomum)[2]
			x1nocomum = zno_noraiz(subestacao, alimentador, nocomum)[3]

			z0nocomum = zno_noraiz(subestacao, alimentador, nocomum)[4]
			z1nocomum = zno_noraiz(subestacao, alimentador, nocomum)[5]

			if nocomum == no1:

				r0pu = r0no2 - r0nocomum
				x0pu = x0no2 - x0nocomum

				r1pu = r1no2 - r1nocomum
				x1pu = x1no2 - x1nocomum

				z0pu = z0no2 - z0nocomum
				z1pu = z0no2 - z0nocomum

			elif nocomum == no2:

				r0pu = r0no1 - r0nocomum
				x0pu = x0no1 - x0nocomum

				r1pu = r1no1 - r1nocomum
				x1pu = x1no1 - x1nocomum

				z0pu = z0no1 - z0nocomum
				z1pu = z0no1 - z0nocomum

			else:
				r0pu = r0no1 + r0no2 - 2 * r0nocomum
				x0pu = x0no1 + x0no2 - 2 * x0nocomum

				r1pu = r1no1 + r1no2 - 2 * r1nocomum
				x1pu = x1no1 + x1no2 - 2 * x1nocomum

				z0pu = z0no1 + z0no2 - 2 * z0nocomum
				z1pu = z0no1 + z1no2 - 2 * z0nocomum


			return r0pu, x0pu, r1pu, x1pu, z0pu, z1pu   

def zchave_noraiz(subestacao, alimentador, ch):
	"""função que calcula as impedância da chave até a subestação"""
	r1ch = 0
	x1ch = 0
	r0ch = 0
	x0ch = 0
	for trafo in subestacao.transformadores.values():
		base2 = trafo.tensao_secundario.mod**2 * trafo.potencia.mod**-1

	for trecho in alimentador.trechos.values():

		if trecho.n2.nome == ch:
			
			r1ch += trecho.comprimento * trecho.condutor.rp
			r1chpu = r1ch / base2
			x1ch += trecho.comprimento * trecho.condutor.xp
			x1chpu = x1ch/ base2
			
			r0ch += trecho.comprimento * trecho.condutor.rz
			r0chpu = r0ch / base2 
			x0ch += trecho.comprimento * trecho.condutor.xz
			x0chpu = x0ch / base2
			
			r0chpu += zno_noraiz(subestacao, alimentador, trecho.n1.nome)[0]
			x0chpu += zno_noraiz(subestacao, alimentador, trecho.n1.nome)[1]

			r1chpu += zno_noraiz(subestacao, alimentador, trecho.n1.nome)[2]
			x1chpu += zno_noraiz(subestacao, alimentador, trecho.n1.nome)[3]
			break
	
	for trafo in subestacao.transformadores.values():
			
			z1trafopu = trafo.z1 / base2
			z0trafopu = z1trafopu
			r1trafopu = trafo.z1.real / base2
			x1trafopu = trafo.z1.imag / base2
			r0trafopu = r1trafopu
			x0trafopu = x1trafopu


	r1chpu += r1trafopu + subestacao.impedancia_equivalente_positiva.real
	x1chpu += x1trafopu + subestacao.impedancia_equivalente_positiva.imag
	z1chpu = (r1chpu ** 2 + x1chpu ** 2) ** 0.5

	r0chpu += r0trafopu + subestacao.impedancia_equivalente_zero.real
	x0chpu += x0trafopu + subestacao.impedancia_equivalente_zero.imag
	z0chpu = (r0chpu ** 2 + x0chpu ** 2) ** 0.5
	return z0chpu, z1chpu, r0chpu, x0chpu, r1chpu, x1chpu

def zchave_no(subestacao, alimentador, ch, no):
	"""função que calcula as impedância da chave até a subestação"""
	r1cha = 0
	x1cha = 0
	r0cha = 0
	x0cha = 0

	r1chb = 0
	x1chb = 0
	r0chb = 0
	x0chb = 0
	for trafo in subestacao.transformadores.values():
		base2 = trafo.tensao_secundario.mod**2 * trafo.potencia.mod**-1

	for trecho in alimentador.trechos.values():
		if trecho.n2.nome == ch:

			r1cha += trecho.comprimento * trecho.condutor.rp
			r1chpua = r1cha / base2
			x1cha += trecho.comprimento * trecho.condutor.xp
			x1chpua = x1cha / base2

			r0cha += trecho.comprimento * trecho.condutor.rz
			r0chpua = r0cha / base2 
			x0cha += trecho.comprimento * trecho.condutor.xz
			x0chpua = x0cha / base2

			r0chpua += zno_no(subestacao, alimentador, trecho.n1.nome, no)[0]
			x0chpua += zno_no(subestacao, alimentador, trecho.n1.nome, no)[1]

			r1chpua += zno_no(subestacao, alimentador, trecho.n1.nome, no)[2]
			x1chpua += zno_no(subestacao, alimentador, trecho.n1.nome, no)[3]

		elif trecho.n1.nome == ch:
			r1chb += trecho.comprimento * trecho.condutor.rp
			r1chpub = r1chb / base2
			x1chb += trecho.comprimento * trecho.condutor.xp
			x1chpub = x1chb / base2

			r0chb += trecho.comprimento * trecho.condutor.rz
			r0chpub = r0chb / base2
			x0chb += trecho.comprimento * trecho.condutor.xz
			x0chpub = x0chb / base2

			r0chpub += zno_no(subestacao, alimentador, trecho.n2.nome, no)[0]
			x0chpub += zno_no(subestacao, alimentador, trecho.n2.nome, no)[1]

			r1chpub += zno_no(subestacao, alimentador, trecho.n2.nome, no)[2]
			x1chpub += zno_no(subestacao, alimentador, trecho.n2.nome, no)[3]
			
	if r1chpua > r1chpub:
		r1chpua = r1chpub
	elif r1chpua < r1chpub:
		pass

	for trafo in subestacao.transformadores.values():

			z1trafopu = trafo.impedancia.mod / base2
			z0trafopu = z1trafopu
			r1trafopu = trafo.impedancia.real / base2
			x1trafopu = trafo.impedancia.imag / base2
			r0trafopu = r1trafopu
			x0trafopu = x1trafopu

	r1chpua += r1trafopu + subestacao.impedancia_equivalente_positiva.real
	x1chpua += x1trafopu + subestacao.impedancia_equivalente_positiva.imag
	z1chpua = (r1chpua ** 2 + x1chpua ** 2) ** 0.5

	r0chpua += r0trafopu + subestacao.impedancia_equivalente_zero.real
	x0chpua += x0trafopu + subestacao.impedancia_equivalente_zero.imag
	z0chpua = (r0chpua ** 2 + x0chpua ** 2) ** 0.5
	return z0chpua, z1chpua, r0chpua, x0chpua, r1chpua, x1chpua, r1chpua, r1chpub

def curto3f_geracao(subestacao, alimentador, ponto):

	ibase = subestacao.sbase / (np.sqrt(3) * subestacao.tensaosaida)
	ccgeracao = 0
	# print "debug curto3f_geracao: ponto = ", ponto.nome
	# print "debug curto3f_geracao: ", alimentador.nos_de_carga.keys()

	for no in alimentador.nos_de_carga.values():

		# print no.nome, ponto.nome, no.nome == ponto.nome, type(ponto), type(no)
		if no.nome == ponto.nome:
			
			ccgeracao = (1 / zno_noraiz(subestacao, alimentador, no.nome)[5]) * ibase

	if ccgeracao == 0:

		ccgeracao = 1 / zchave_noraiz(subestacao, alimentador, ponto.nome)[1]

	return ccgeracao

def curto3f_gd(subestacao, ponto, gd):

	#loop verifica se o ponto pertence a subestacao 

	if all(alimentador.nos_de_carga.has_key(ponto.nome) == False for alimentador in subestacao.alimentadores.values()):

		print ponto.nome + ' nao pertence a subestacao ' + subestacao.nome
		
		return 0.0
	
	else:

		pass



	ali1 = None
	ali2 = None
	x1 = 0.0
	r1 = 0.0
	ccgd = 0.0
	ibase = subestacao.sbase / (np.sqrt(3) * subestacao.tensaosaida)

	if gd.ativo: # adicionado por felipe

		# loop verifica se os alimentadores do ponto e da gd
		for alimentador in subestacao.alimentadores.values():
			for no in alimentador.nos_de_carga.values():
				if no.nome == ponto.nome:
					ali1 = alimentador # alimentador que contem o no
				elif no.nome == gd.nome:
					ali2 = alimentador # alimentador que contem a gd
				else:
					pass

		if ali1 == ali2: # loop para o caso de o no e a gd estarem no mesmo alimentador

			if gd.interface_rede == 'INVERSOR':

				vprefger = gd.x1 * gd.corrente_curto               
				x1gd = gd.x1 * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[2]
				x1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[3]
				z1 = (r1 ** 2 + (x1+x1gd) ** 2) ** 0.5
				ccgd = (vprefger / z1) * ibase

			elif gd.interface_rede == 'SINCRONO':

				z1gd = (gd.r1 + 1.0j * gd.x1) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[2]
				x1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[3]
				z1 = ((r1 + z1gd.real) ** 2 + (x1 + z1gd.imag) ** 2) ** 0.5
				ccgd = (1 / z1) * ibase

		else: # loop para a gd e o no em pontos distintos

			if gd.interface_rede == 'INVERSOR':

				vprefger = gd.x1 * gd.corrente_curto
				x1gd = gd.x1 * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_noraiz(subestacao, ali1, ponto.nome)[2] 
				r1 += zno_noraiz(subestacao, ali2, gd.nome)[2]
				x1 = zno_noraiz(subestacao, ali2, gd.nome)[3]
				x1 += zno_noraiz(subestacao, ali1, ponto.nome)[3]
				z1 = (r1 ** 2 + (x1+x1gd) ** 2) ** 0.5
				ccgd = (vprefger / z1) * ibase

			elif gd.interface_rede == 'SINCRONO': 

				z1gd = (gd.r1 + 1.0j * gd.x1) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_noraiz(subestacao, ali1, ponto.nome)[2]
				r1 += zno_noraiz(subestacao, ali2, gd.nome)[2]
				x1 = zno_noraiz(subestacao, ali2, gd.nome)[3]
				x1 = zno_noraiz(subestacao, ali2, gd.nome)[3]
				z1 = ((r1 + z1gd.real) ** 2 + (x1 + z1gd.imag) ** 2) ** 0.5
				ccgd = (1 / z1) * ibase         

	else:
		ccgd=0.0
	return ccgd

def curto3f_total(subestacao, alimentador, ponto, gd):
	cctotal = 0
	cctotal += curto3f_geracao(subestacao, alimentador, ponto)
	cctotal += curto3f_gd(subestacao, ponto, gd)
	#cctotal += curto3f_gd(subestacao, alimentador, ponto)

	return cctotal

def curto2f_geracao(subestacao, alimentador, ponto):
	
	return curto3f_geracao(subestacao, alimentador, ponto) * np.sqrt(3) * 2 ** -1

def curto2f_gd(subestacao, alimentador, ponto): # a contribuicao da gd nao foi cancelada neste caso	
	contribgd = list()
	curtogd = list()
	ccgdtotal = 0.0
	x1 = 0.0
	x0 = 0.0
	r1 = 0.0
	r0 = 0.0
	ibase = subestacao.sbase / (np.sqrt(3) * subestacao.tensaosaida) 
	for ger in alimentador.nos_de_carga.values():
		if type(ger) == Gerador:
			if ger.interface_rede == 'INVERSOR':
				vprefger = ger.x1 * ger.corrente_curto                
				x1gd = ger.x1 * (subestacao.sbase / ger.potencia_fase_a.mod) * (ger.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_no(subestacao, alimentador, ponto.nome, ger.nome)[2]
				x1 = zno_no(subestacao, alimentador, ponto.nome, ger.nome)[3]
				z1 = (r1 ** 2 + (x1+x1gd) ** 2) ** 0.5
				ccgd = (vprefger / z1) * ibase               

			elif ger.interface_rede == 'SINCRONO':
				
				z1gd = (ger.r1 + 1.0j * ger.x1) * (subestacao.sbase / ger.potencia_fase_a.mod) * (ger.tensaogerador/subestacao.tensaosaida) ** 2
				z2gd = (ger.r2 + 1.0j * ger.x2) * (subestacao.sbase / ger.potencia_fase_a.mod) * (ger.tensaogerador/subestacao.tensaosaida) ** 2
				
				r1 = zno_no(subestacao, alimentador, ponto.nome, ger.nome)[2]
				x1 = zno_no(subestacao, alimentador, ponto.nome, ger.nome)[3]

				r2 = r1
				x2 = x1

				den = (r1 + z1gd.real) + 1.0j * (x1 + z1gd.imag)
				den += (r2 + z2gd.real) + 1.0j * (x2 + z2gd.imag)
				den = abs(den)
				
				ccgd = (np.sqrt(3) / den)  * ibase
			curtogd.append(ccgd)
			contribgd.append('A contribuicao do gerador %s e: %f A' %(ger.nome, ccgd))
	
	for curto in curtogd:
		ccgdtotal += curto

	return contribgd, ccgdtotal, curtogd

def curto1f_geracao(subestacao, alimentador, ponto):

	ibase = subestacao.sbase / (np.sqrt(3) * subestacao.tensaosaida)
	ccgeracao = 0

	for no in alimentador.nos_de_carga.values():

		if no.nome == ponto.nome:

			r0 = zno_noraiz(subestacao, alimentador, no.nome)[0]
			x0 = zno_noraiz(subestacao, alimentador, no.nome)[1]
			r1 = zno_noraiz(subestacao, alimentador, no.nome)[2]
			x1 = zno_noraiz(subestacao, alimentador, no.nome)[3]

			ccgeracao = (3 / abs(2 *(r1 + x1 * 1.0j) + (r0 + x0 * 1.0j))) * ibase

	if ccgeracao == 0:
		ccgeracao = 1 / zchave_noraiz(subestacao, alimentador, ponto.nome)[1]
	return ccgeracao

def curto1f_gd(subestacao, ponto, gd):
	ali1 = None
	ali2 = None
	x1 = 0.0
	r1 = 0.0
	r2 = 0.0
	x2 = 0.0
	x0 = 0.0
	r0 = 0.0
	den = 0.0
	ccgd = 0.0
	ibase = subestacao.sbase / (np.sqrt(3) * subestacao.tensaosaida)
	if gd.ativo:
		for alimentador in subestacao.alimentadores.values():
			for no in alimentador.nos_de_carga.values():
				if no.nome == ponto.nome:
					ali1 = alimentador
				elif no.nome == gd.nome:
					ali2 = alimentador
				else:
					pass

		if ali1 == ali2:
			if gd.interface_rede == 'INVERSOR':
				vprefger = gd.x1 * gd.corrente_curto                
				x1gd = gd.x1 * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[2]
				x1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[3]
				z1 = (r1 ** 2 + (x1+x1gd) ** 2) ** 0.5
				ccgd = (vprefger / z1) * ibase
			elif gd.interface_rede == 'SINCRONO':
				z1gd = (gd.r1 + 1.0j * gd.x1) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				z2gd = (gd.r2 + 1.0j * gd.x2) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				z0gd = (gd.r0 + 1.0j * gd.x0) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				
				r1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[2]
				x1 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[3]
				
				r0 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[0]
				x0 = zno_no(subestacao, ali1, ponto.nome, gd.nome)[1]

				r2 = r1
				x2 = x1

				den = (z1gd.real + r1) + 1.0j * (z1gd.imag + x1)
				den += (z0gd.real + r0) + 1.0j * (z0gd.imag + x0)
				den += (z2gd.real + r2) + 1.0j * (z2gd.imag + x2)
				den = abs(den)
				
				ccgd = (3 / den) * ibase
		else:
			if gd.interface_rede == 'INVERSOR':
				vprefger = gd.x1 * gd.corrente_curto
				x1gd = gd.x1 * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				r1 = zno_noraiz(subestacao, ali1, ponto.nome)[2] 
				r1 += zno_noraiz(subestacao, ali2, gd.nome)[2]
				x1 = zno_noraiz(subestacao, ali2, gd.nome)[3]
				x1 += zno_noraiz(subestacao, ali1, ponto.nome)[3]
				z1 = (r1 ** 2 + (x1+x1gd) ** 2) ** 0.5
				ccgd = (vprefger / z1) * ibase
			elif gd.interface_rede == 'SINCRONO': 
				z1gd = (gd.r1 + 1.0j * gd.x1) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				z2gd = (gd.r2 + 1.0j * gd.x2) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				z0gd = (gd.r0 + 1.0j * gd.x0) * (subestacao.sbase / gd.potencia_fase_a.mod) * (gd.tensaogerador/subestacao.tensaosaida) ** 2
				
				r1 = zno_noraiz(subestacao, ali1, ponto.nome)[2]
				r1 += zno_noraiz(subestacao, ali2, gd.nome)[2]
				x1 = zno_noraiz(subestacao, ali2, gd.nome)[3]
				x1 += zno_noraiz(subestacao, ali1, ponto.nome)[3]
				r2 = r1
				x2 = x1

				den = (z1gd.real + r1) + 1.0j * (z1gd.imag + x1)
				den += (z0gd.real + r0) + 1.0j * (z0gd.imag + x0)
				den += (z2gd.real + r2) + 1.0j * (z2gd.imag + x2)
				den = abs(den)
				
				ccgd = (3 / den) * ibase 
	else:

		ccgd=0.0            
				
	return ccgd



