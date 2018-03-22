# coding=utf-8
from terminaltables import AsciiTable
import numpy as np
from random import randint
from rnp import Arvore, Aresta
from util import Fasor, Base


class Setor(Arvore):
    def __init__(self, nome, vizinhos, nos_de_carga, prioridade=0):
        assert isinstance(nome, str), 'O parâmetro nome da classe' \
                                      'Setor deve ser do tipo string'
        assert isinstance(vizinhos, list), 'O parâmetro vizinhos da classe' \
                                           ' Setor deve ser do tipo list'
        assert isinstance(nos_de_carga, list), 'O parâmetro nos_de_carga da classsse' \
                                               'Setor deve ser do tipo list'
        assert (prioridade >= 0 and prioridade <= 10), 'O valo de prioridade' \
                                                       'deve estar entre 0-10'

        # assert isinstance(prioridade, int), 'O parâmetro Prioridade da classe' \
        #                                    'Setor deve ser do tipo int'
        self.nome = nome
        self.prioridade = prioridade
        self.vizinhos = vizinhos

        self.rnp_associadas = {i: None for i in self.vizinhos}

        self.nos_de_carga = dict()
        for no in nos_de_carga:
            no.setor = self.nome
            self.nos_de_carga[no.nome] = no

        self.no_de_ligacao = None

        arvore_de_setor = self._gera_arvore_do_setor()
        super(Setor, self).__init__(arvore_de_setor, str)

    def _gera_arvore_do_setor(self):
        arvore_do_setor = dict()
        # for percorre os nós de carga do setor
        for i, j in self.nos_de_carga.iteritems():
            # print '%-12s vizinhos %s' % (str(j), j.vizinhos)
            vizinhos = list()
            # for percorre os vizinhos do nó de carga
            for k in j.vizinhos:
                # condição só considera vizinho o nó de carga que está
                # no mesmo setor que o nó de carga analisado
                if k in self.nos_de_carga.keys():
                    vizinhos.append(k)
            arvore_do_setor[i] = vizinhos

        return arvore_do_setor

    def calcular_potencia(self):

        potencia_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        potencia_fase_b = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        potencia_fase_c = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        for no in self.nos_de_carga.values():
            potencia_fase_a = potencia_fase_a + no.potencia_fase_a
            potencia_fase_b = potencia_fase_b + no.potencia_fase_b
            potencia_fase_c = potencia_fase_c + no.potencia_fase_c

        return potencia_fase_a, potencia_fase_b, potencia_fase_c

    def __str__(self):
        return 'Setor: ' + self.nome


class NoDeCarga(object):
    def __init__(self,
                 nome,
                 vizinhos,
                 #conexao,
                 modelo,
                 potencia_fase_a=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 potencia_fase_b=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 potencia_fase_c=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 tensao_fase_a=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 tensao_fase_b=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 tensao_fase_c=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 chaves=None):
        assert isinstance(nome, str), 'O parâmetro nome da classe NoDeCarga' \
                                      ' deve ser do tipo string'
        assert isinstance(vizinhos, list), 'O parâmetro vizinhos da classe' \
                                           ' Barra deve ser do tipo string'

        self.nome = nome
        self.vizinhos = vizinhos
        #self.conexao = conexao
        self.modelo = modelo
        self.potencia_fase_a = potencia_fase_a
        self.potencia_fase_b = potencia_fase_b
        self.potencia_fase_c = potencia_fase_c
        self.potencia_eq_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.potencia_eq_fase_b = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.potencia_eq_fase_c = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.tensao_fase_a = tensao_fase_a
        self.tensao_fase_b = tensao_fase_b
        self.tensao_fase_c = tensao_fase_c

        if chaves is not None:
            assert isinstance(chaves, list), 'O parâmetro chaves da classe NoDeCarga' \
                                             ' deve ser do tipo list'
            self.chaves = chaves
        else:
            self.chaves = list()

        self.setor = None

    def __str__(self):
        return 'No de Carga: ' + self.nome


class Gerador(object):
    def __init__(self,
                 nome,
                 ativo,
                 vizinhos,
                 interface_rede,
                 #maquina,
                 modelo,
                 conexao,
                 qmin,
                 qmax,
                 tensaogerador,
                 dvtol,
                 x0=0.0j,
                 x1=0.0j,
                 x2=0.0j,
                 xsubt=0.0j,
                 xsobrer=0.0,
                 potencia_nominal=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia), # adicionado por felipe
                 #potencia_fase_a=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 #potencia_fase_b=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 #potencia_fase_c=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 tensao_fase_a=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 tensao_fase_b=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 tensao_fase_c=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 chaves=None):

        self.nome = nome
        self.ativo = ativo
        self.vizinhos = vizinhos
        #self.potencia_fase_a = potencia_fase_a
        #self.potencia_fase_b = potencia_fase_b
        #self.potencia_fase_c = potencia_fase_c

        self.potencia_nominal = potencia_nominal

        if self.ativo: # adicionado por felipe

            self.potencia_fase_a = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)
            self.potencia_fase_b = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)
            self.potencia_fase_c = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)

        else: 

            self.potencia_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
            self.potencia_fase_b = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
            self.potencia_fase_c = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)

        self.dvtol = dvtol
        self.potencia_eq_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.potencia_eq_fase_b = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.potencia_eq_fase_c = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        self.tensao_fase_a = tensao_fase_a
        self.tensao_fase_b = tensao_fase_b
        self.tensao_fase_c = tensao_fase_c
        self.interface_rede = interface_rede
        #self.maquina = maquina
        self.modelo = modelo
        self.conexao = conexao
        self.qmin = qmin
        self.qmax = qmax
        self.tensaogerador = tensaogerador
        self.corrente_nominal = 1

        if self.interface_rede == 'INVERSOR':
          self.corrente_curto = 2 * self.corrente_nominal
          self.x1 = 1
        elif self.interface_rede == 'SINCRONO':
          self.xsobrer = xsobrer
          self.xsubt = xsubt
          self.x0 = x0
          self.r0 = self.x0 * (self.xsobrer) ** -1
          self.x1 = xsubt
          self.r1 = self.x1 * (self.xsobrer) ** -1
          self.x2 = x2
          self.r2 = self.x2 * (self.xsobrer) ** -1    

        assert isinstance(interface_rede, str), 'O parâmetro interface_rede deve' \
                                             'ser do tipo str'
        # assert isinstance(maquina, str), 'O parâmetro maquina deve' \
        #                                  'ser do tipo str'
        assert isinstance(modelo, str), 'O parâmetro modelo deve' \
                                        'ser do tipo str'
        if chaves is not None:
            assert isinstance(chaves, list), 'O parâmetro chaves da classe NoDeCarga' \
                                             ' deve ser do tipo list'
            self.chaves = chaves
        else:
            self.chaves = list()

        self.setor = None

    def __repr__(self):
        return 'Gerador: {nome}'.format(nome=self.nome)

    def ativaGD(self): # adicionado por felipe

        if self.ativo:

            pass

        else:

            self.ativo = True

            self.potencia_fase_a = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)
            self.potencia_fase_b = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)
            self.potencia_fase_c = Fasor(real=self.potencia_nominal.real, imag=self.potencia_nominal.imag, tipo=Fasor.Potencia)

    def desativaGD(self): # adicionado por felipe

        if self.ativo:
            
            self.ativo = False

            self.potencia_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
            self.potencia_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
            self.potencia_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)

        else:

            pass    


class Barramento(NoDeCarga):
    def __init__(self,
                 nome,
                 vizinhos,
                 potencia=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                 tensao=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                 chaves=None):
        super(Barramento, self).__init__(nome,
                                         vizinhos,
                                         potencia=Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia),
                                         tensao=Fasor(real=0.0, imag=0.0, tipo=Fasor.Tensao),
                                         chaves=None)


class Subestacao(object):
    def __init__(self, 
                 nome,
                 alimentadores,
                 transformadores,
                 sbase,
                 tensaoentrada=0.0,
                 tensaosaida=0.0,
                 impedancia_equivalente_positiva=0.0+0.0j,
                 impedancia_equivalente_zero=0.0+0.0j,
                 resistencia_contato=0):
        assert isinstance(nome, str), 'O parâmetro nome da classe Subestacao ' \
                                      'deve ser do tipo str'
        assert isinstance(alimentadores, list), 'O parâmetro alimentadores da classe ' \
                                                'deve ser do tipo list'

        assert isinstance(transformadores, list), 'O parâmetro alimentadores da classe ' \
                                                  'deve ser do tipo list'
        self.nome = nome

        self.alimentadores = dict()
        for alimentador in alimentadores:
            self.alimentadores[alimentador.nome] = alimentador

        self.transformadores = dict()
        for transformador in transformadores:
            self.transformadores[transformador.nome] = transformador

        self.impedancia_equivalente_positiva = impedancia_equivalente_positiva
        self.impedancia_equivalente_zero = impedancia_equivalente_zero
        self.tensaosaida = tensaosaida
        self.tensaoentrada = tensaoentrada
        self.resistencia_contato = resistencia_contato
        self.sbase = sbase


class Trecho(Aresta):
    def __init__(self,
                 nome,
                 n1,
                 n2,
                 #local,
                 #config_tr,
                 fluxo_fase_a=None,
                 fluxo_fase_b=None,
                 fluxo_fase_c=None,
                 condutor=None,
                 comprimento=None,
                 resistenciacontato=100):
        assert isinstance(nome, str), 'O parâmetro nome da classe Trecho ' \
                                      'deve ser do tipo str'
        assert isinstance(n1, NoDeCarga) or isinstance(n1, Chave) or isinstance(n1, Gerador), 'O parâmetro n1 da classe Trecho ' \
                                                                                              'deve ser do tipo No de carga ' \
                                                                                              'ou do tipo Chave'
        assert isinstance(n2, NoDeCarga) or isinstance(n2, Chave) or isinstance(n2, Gerador), 'O parâmetro n2 da classe Trecho ' \
                                                                                              'deve ser do tipo No de carga ' \
                                                                                              'ou do tipo Chave'
        super(Trecho, self).__init__(nome)
        self.n1 = n1
        self.n2 = n2
        self.no_montante = None
        self.no_jusante = None
        #self.config_tr = config_tr
        #self.local = local
        self.condutor = condutor
        self.comprimento = comprimento
        self.impedancia_positiva = (self.condutor.rp + self.condutor.xp * 1j) * self.comprimento
        self.impedancia_zero = (self.condutor.rz + self.condutor.xz * 1j) * self.comprimento
        #self.resistencia_contato = resistenciacontato

        if fluxo_fase_a is None:
            self.fluxo_fase_a = Fasor(real=0.0, imag=0.0, tipo=Fasor.Corrente)
        else:
            self.fluxo_fase_a = fluxo_fase_a

        if fluxo_fase_a is None:
            self.fluxo_fase_b = Fasor(real=0.0, imag=0.0, tipo=Fasor.Corrente)
        else:
            self.fluxo_fase_b = fluxo_fase_b

        if fluxo_fase_a is None:
            self.fluxo_fase_c = Fasor(real=0.0, imag=0.0, tipo=Fasor.Corrente)
        else:
            self.fluxo_fase_c = fluxo_fase_c

        # if local == 'aereo':
        #     if config_tr == 'ID-500':
        #         self.d_12 = 2.5
        #         self.d_23 = 4.5
        #         self.d_13 = 7
        #         self.d_fn = 4
        #         self.d_np = 0.5
        #         self.d_ns = 24
        #         self.d_fs = 28

        #     elif config_tr == 'ID-505':
        #         self.d_12 = 7
        #         self.d_fn = 4
        #         self.d_np = 0.5
        #         self.d_ns = 24
        #         self.d_fs = 28

        #     elif config_tr == 'ID-510':
        #         self.d_fn = 5
        #         self.d_np = 0.5
        #         self.d_ns = 24
        #         self.d_fs = 29

        # elif local == 'subterraneo':
        #     if config_tr == 'ID-515':
        #         self.d_12 = 0.1524
        #         self.d_23 = 0.1524
        #         self.d_13 = 0.3048

        #     if config_tr == 'ID-520':
        #         self.d_12 = 0.0254

    # def carson(self):
    #     if self.condutor.xp != 0:
    #         if self.config_tr == 'ID-505':
    #             return 'id-505'
    #         elif self.config_tr == 'ID-510':
    #             return 'id-510'
    #         elif self.config_tr == 'ID-515':
    #             return 'id-515'

    def calcula_impedancia(self):
        return (self.comprimento * self.condutor.rp,
                self.comprimento * self.condutor.xp)
   
    def __repr__(self):
        return 'Trecho: %s' % self.nome


class Alimentador(Arvore):
    def __init__(self, nome, setores, trechos, chaves):
        assert isinstance(nome, str), 'O parâmetro nome da classe Alimentador' \
                                      'deve ser do tipo string'
        assert isinstance(setores, list), 'O parâmetro setores da classe' \
                                          'Alimentador deve ser do tipo list'
        assert isinstance(chaves, list), 'O parâmetro chaves da classe' \
                                         'Alimentador deve ser do tipo list'
        self.nome = nome

        self.setores = dict()
        for setor in setores:
            self.setores[setor.nome] = setor

        self.chaves = dict()
        for chave in chaves:
            self.chaves[chave.nome] = chave

        self.nos_de_carga = dict()
        for setor in setores:
            for no in setor.nos_de_carga.values():
                self.nos_de_carga[no.nome] = no

        self.trechos = dict()
        for trecho in trechos:
            self.trechos[trecho.nome] = trecho

        for setor in self.setores.values():
            # print 'Setor: ', setor.nome
            setores_vizinhos = list()
            for chave in self.chaves.values():
                if chave.n1 is setor:
                    setores_vizinhos.append(chave.n2)
                elif chave.n2 is setor:
                    setores_vizinhos.append(chave.n1)

            for setor_vizinho in setores_vizinhos:
                # print 'Setor Vizinho: ', setor_vizinho.nome
                nos_de_ligacao = list()
                for i in setor.nos_de_carga.values():
                    for j in setor_vizinho.nos_de_carga.values():
                        if i.nome in j.vizinhos:
                            nos_de_ligacao.append((j, i))

                for no in nos_de_ligacao:
                    setor.ordenar(no[1].nome)
                    setor.rnp_associadas[setor_vizinho.nome] = (no[0],
                                                                setor.rnp)
                    # print 'RNP: ', setor.rnp

        _arvore_da_rede = self._gera_arvore_da_rede()

        super(Alimentador, self).__init__(_arvore_da_rede, str)

    def ordenar(self, raiz):
        super(Alimentador, self).ordenar(raiz)

        for setor in self.setores.values():
            caminho = self.caminho_no_para_raiz(setor.nome)
            if setor.nome != raiz:
                setor_jusante = caminho[1, 1]
                setor.rnp = setor.rnp_associadas[setor_jusante][1]

    def _gera_arvore_da_rede(self):

        arvore_da_rede = {i: list() for i in self.setores.keys()}

        for chave in self.chaves.values():
            if chave.n1.nome in self.setores.keys() and chave.estado == 1:
                arvore_da_rede[chave.n1.nome].append(chave.n2.nome)
            if chave.n2.nome in self.setores.keys() and chave.estado == 1:
                arvore_da_rede[chave.n2.nome].append(chave.n1.nome)

        return arvore_da_rede

    def gerar_arvore_nos_de_carga(self):

        # define os nós de carga do setor raiz da subestação como os primeiros
        # nós de carga a povoarem a arvore nós de carga e a rnp nós de carga
        setor_raiz = self.setores[self.rnp[1][0]]
        self.arvore_nos_de_carga = Arvore(arvore=setor_raiz._gera_arvore_do_setor(),
                                          dtype=str)
        self.arvore_nos_de_carga.ordenar(raiz=setor_raiz.rnp[1][0])

        # define as listas visitados e pilha, necessárias ao
        # processo recursivo de visita
        # dos setores da subestação
        visitados = []
        pilha = []

        # inicia o processo iterativo de visita dos setores
        # em busca de seus respectivos nós de carga
        self._gerar_arvore_nos_de_carga(setor_raiz, visitados, pilha)

    def _gerar_arvore_nos_de_carga(self, setor, visitados, pilha):

        # atualiza as listas de recursão
        visitados.append(setor.nome)
        pilha.append(setor.nome)

        # for percorre os setores vizinhos ao setor atual
        # que ainda não tenham sido visitados
        vizinhos = setor.vizinhos
        for i in vizinhos:

            # esta condição testa se existe uma ligação
            # entre os setores de uma mesma subestação, mas
            # que possuem uma chave normalmente aberta entre eles.
            # caso isto seja constatado o laço for é interrompido.
            if i not in visitados and i in self.setores.keys():
                for c in self.chaves.values():
                    if c.n1.nome == setor.nome and c.n2.nome == i:
                        if c.estado == 1:
                            break
                        else:
                            pass
                    elif c.n2.nome == setor.nome and c.n1.nome == i:
                        if c.estado == 1:
                            break
                        else:
                            pass
                else:
                    continue
                prox = i
                setor_vizinho = self.setores[i]
                no_insersao, rnp_insersao = setor_vizinho.rnp_associadas[setor.nome]
                arvore_insersao = setor_vizinho._gera_arvore_do_setor()

                setor_vizinho.no_de_ligacao = no_insersao

                setor_vizinho.rnp = rnp_insersao

                self.arvore_nos_de_carga.inserir_ramo(no_insersao.nome,
                                                      (rnp_insersao,
                                                       arvore_insersao),
                                                      no_raiz=rnp_insersao[1, 0]
                                                      )
                break
            else:
                continue
        else:
            pilha.pop()
            if pilha:
                anter = pilha.pop()
                return self._gerar_arvore_nos_de_carga(self.setores[anter],
                                                       visitados, pilha)
            else:
                return
        return self._gerar_arvore_nos_de_carga(self.setores[prox],
                                               visitados,
                                               pilha)

    def atualizar_arvore_da_rede(self):
        _arvore_da_rede = self._gera_arvore_da_rede()
        self.arvore = _arvore_da_rede

    def gerar_trechos_da_rede(self):

        self.trechos = dict()

        j = 0
        for i in range(1, np.size(self.arvore_nos_de_carga.rnp, axis=1)):
            prof_1 = int(self.arvore_nos_de_carga.rnp[0, i])
            prof_2 = int(self.arvore_nos_de_carga.rnp[0, j])

            while abs(prof_1 - prof_2) is not 1:
                if abs(prof_1 - prof_2) == 0:
                    j -= 1
                elif abs(prof_1 - prof_2) == 2:
                    j = i - 1
                prof_2 = int(self.arvore_nos_de_carga.rnp[0, j])
            else:
                n_1 = str(self.arvore_nos_de_carga.rnp[1, j])
                n_2 = str(self.arvore_nos_de_carga.rnp[1, i])
                setor_1 = None
                setor_2 = None
                # print 'Trecho: ' + n_1 + '-' + n_2

                # verifica quais os nós de carga existentes nas extremidades do trecho
                # e se existe uma chave no trecho

                for setor in self.setores.values():
                    if n_1 in setor.nos_de_carga.keys():
                        setor_1 = setor
                    if n_2 in setor.nos_de_carga.keys():
                        setor_2 = setor

                    if setor_1 is not None and setor_2 is not None:
                        break
                else:
                    if setor_1 is None:
                        n = n_1
                    else:
                        n = n_2
                    for setor in self.setores.values():
                        if n in setor.nos_de_carga.keys() and np.size(setor.rnp, axis=1) == 1:
                            if setor_1 is None:
                                setor_1 = setor
                            else:
                                setor_2 = setor
                            break

                if setor_1 != setor_2:
                    for chave in self.chaves.values():
                        if chave.n1 in (setor_1, setor_2) and chave.n2 in (setor_1, setor_2):
                            self.trechos[n_1 + n_2] = Trecho(nome=n_1 + n_2,
                                                             n1=self.nos_de_carga[n_1],
                                                             n2=self.nos_de_carga[n_2],
                                                             chave=chave)
                else:
                    self.trechos[n_1 + n_2] = Trecho(nome=n_1 + n_2,
                                                     n1=self.nos_de_carga[n_1],
                                                     n2=self.nos_de_carga[n_2])

    def calcular_potencia(self):
        potencia = Fasor(real=0.0, imag=0.0, tipo=Fasor.Potencia)
        for no in self.nos_de_carga.values():
            potencia = potencia + no.potencia_fase_a

        return potencia

    def podar(self, no, alterar_rnp=False):
        poda = super(Alimentador, self).podar(no, alterar_rnp)
        rnp_setores = poda[0]
        arvore_setores = poda[1]

        if alterar_rnp:
            # for povoa dicionario com setores podados
            setores = dict()
            for i in rnp_setores[1, :]:
                setor = self.setores.pop(i)
                setores[setor.nome] = setor

            # for povoa dicionario com nos de carga podados
            nos_de_carga = dict()
            for setor in setores.values():
                for j in setor.nos_de_carga.values():
                    if j.nome in self.nos_de_carga.keys():
                        no_de_carga = self.nos_de_carga.pop(j.nome)
                        nos_de_carga[no_de_carga.nome] = no_de_carga

            # for atualiza a lista de nós de carga da subestação
            # excluindo os nós de carga podados
            for setor in self.setores.values():
                for no_de_carga in setor.nos_de_carga.values():
                    self.nos_de_carga[no_de_carga.nome] = no_de_carga
                    if no_de_carga.nome in nos_de_carga.keys():
                        nos_de_carga.pop(no_de_carga.nome)

            # poda o ramo na arvore da subetação
            poda = self.arvore_nos_de_carga.podar(setores[no].rnp[1, 0], alterar_rnp=alterar_rnp)
            rnp_nos_de_carga = poda[0]
            arvore_nos_de_carga = poda[1]

            # for povoa dicionario de chaves que estao nos trechos podados
            # e retira do dicionario de chaves da arvore que esta sofrendo a poda
            # as chaves que não fazem fronteira com os trechos remanescentes
            chaves = dict()
            for chave in self.chaves.values():
                if chave.n1.nome in setores.keys():
                    if not chave.n2.nome in self.setores.keys():
                        chaves[chave.nome] = self.chaves.pop(chave.nome)
                    else:
                        chave.estado = 0
                        chaves[chave.nome] = chave
                elif chave.n2.nome in setores.keys():
                    if not chave.n1.nome in self.setores.keys():
                        chaves[chave.nome] = self.chaves.pop(chave.nome)
                    else:
                        chave.estado = 0
                        chaves[chave.nome] = chave

            # for poda os trechos dos setores podados e povoa o dicionario trechos
            # para que possa ser repassado juntamente com os outros dados da poda
            trechos = dict()
            for no in rnp_nos_de_carga[1, :]:
                for trecho in self.trechos.values():
                    if trecho.n1.nome == no or trecho.n2.nome == no:
                        trechos[trecho.nome] = self.trechos.pop(trecho.nome)

            return (setores, arvore_setores, rnp_setores,
                    nos_de_carga, arvore_nos_de_carga, rnp_nos_de_carga,
                    chaves, trechos)
        else:
            return rnp_setores

    def inserir_ramo(self, no, poda, no_raiz=None):

        (setores, arvore_setores, rnp_setores,
         nos_de_carga, arvore_nos_de_carga, rnp_nos_de_carga,
         chaves, trechos) = poda

        # atualiza setores do alimentador
        self.setores.update(setores)

        # atualiza os nos de carga do alimentador
        self.nos_de_carga.update(nos_de_carga)

        # atualiza as chaves do alimentador
        self.chaves.update(chaves)

        # atualiza os trechos do alimentador
        self.trechos.update(trechos)

        if no_raiz is None:
            setor_inserir = setores[rnp_setores[1, 0]]
        else:
            setor_inserir = setores[no_raiz]

        setor_insersao = self.setores[no]

        # for identifica se existe alguma chave que permita a inserção do ramo na arvore
        # da subestação que ira receber a inserção.
        chaves_de_lig = dict()
        # for percorre os nos de carga do setor de insersão
        for i in self.setores[setor_insersao.nome].nos_de_carga.values():
            # for percorre as chaves associadas ao no de carga
            for j in i.chaves:
                # for percorre os nos de carga do setor raiz do ramo a ser inserido
                for w in setores[setor_inserir.nome].nos_de_carga.values():
                    # se a chave pertence aos nos de carga i e w então é uma chave de ligação
                    if j in w.chaves:
                        chaves_de_lig[j] = (i, w)

        if not chaves_de_lig:
            print 'A insersao não foi possível pois nenhuma chave de fronteira foi encontrada!'
            return

        i = randint(0, len(chaves_de_lig) - 1)
        n1, n2 = chaves_de_lig[chaves_de_lig.keys()[i]]

        self.chaves[chaves_de_lig.keys()[i]].estado = 1

        if setor_inserir.nome == setores[rnp_setores[1, 0]].nome:
            super(Alimentador, self).inserir_ramo(no, (rnp_setores, arvore_setores))
        else:
            super(Alimentador, self).inserir_ramo(no, (rnp_setores, arvore_setores), no_raiz)


        # atualiza a arvore de setores do alimentador
        self.atualizar_arvore_da_rede()

        # atualiza a arvore de nos de carga do alimentador
        self.gerar_arvore_nos_de_carga()


class Chave(Aresta):
    def __init__(self, nome, ied, estado=1):
        assert estado == 1 or estado == 0, 'O parâmetro estado deve ser um inteiro de valor 1 ou 0'
        super(Chave, self).__init__(nome)
        self.estado = estado
        self.ied = ied

    def __str__(self):
        if self.n1 is not None and self.n2 is not None:
            return 'Chave: %s - n1: %s, n2: %s' % (self.nome, self.n1.nome, self.n2.nome)
        else:
            return 'Chave: %s' % self.nome


class Transformador(object):
    def __init__(self,
                 nome,
                 alimentadores,
                 ligacao_primario,
                 ligacao_secundario,
                 tensao_primario,
                 tensao_secundario,
                 potencia,
                 z1,
                 xsobrer):
        assert isinstance(nome, str), 'O parâmetro nome deve ser do tipo str'
        assert isinstance(tensao_secundario, Fasor), 'O parâmetro tensao_secundario deve ser do tipo Fasor'
        assert isinstance(tensao_primario, Fasor), 'O parâmetro tensao_primario deve ser do tipo Fasor'
        assert isinstance(potencia, Fasor), 'O parâmetro potencia deve ser do tipo Fasor'

        self.alimentadores = dict()
        for alimentador in alimentadores:
            self.alimentadores[alimentador.nome] = alimentador

        self.nome = nome
        self.ligacao_primario = ligacao_primario
        self.ligacao_secundario = ligacao_secundario
        self.tensao_primario = tensao_primario
        self.tensao_secundario = tensao_secundario
        self.potencia = potencia
        self.z1 = z1
        self.xsobrer = xsobrer
        self.r1 = np.sqrt((self.z1)**2 / (1 + self.xsobrer**2))
        self.x1 = self.r1 * self.xsobrer


class Condutor(object):
    def __init__(self, 
                #tamanho, 
                nome, 
                rp, 
                xp, 
                rz, 
                xz, 
                #d_ext, 
                #raio_m_g, 
                #d_iso, 
                #d_tela, 
                ampacidade):
        #self.tamanho = tamanho
        self.nome = nome
        self.rp = float(rp)
        self.xp = float(xp)
        self.rz = float(rz)
        self.xz = float(xz)
        #self.d_ext = float(d_ext)  # diâmetro externo
        #self.raio_m_g = float(raio_m_g)  # raio médio geométrico
        #self.d_iso = float(d_iso)
        #self.d_tela = float(d_tela)
        self.ampacidade = float(ampacidade)


if __name__ == '__main__':
    pass
