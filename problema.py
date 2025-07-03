import copy
from typing import List, Tuple, Optional

class EstadoPuzzle:
    def __init__(self, tabuleiro: List[List[int]], tamanho: int, pai=None, acao: str = "", custo_g: int = 0):
        self.tabuleiro = tabuleiro
        self.tamanho = tamanho
        self.pai = pai
        self.acao = acao
        self.custo_g = custo_g
        self.pos_vazio = self._encontrar_posicao_vazio()
        self.hash_estado = self._calcular_hash()
    
    def _encontrar_posicao_vazio(self) -> Tuple[int, int]:
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.tabuleiro[i][j] == 0:
                    return (i, j)
        return None
    
    def _calcular_hash(self) -> str:
        return str([item for linha in self.tabuleiro for item in linha])
    
    def eh_objetivo(self, objetivo: List[List[int]]) -> bool:
        return self.tabuleiro == objetivo
    
    def obter_acoes_possiveis(self) -> List[str]:
        linha_vazio, col_vazio = self.pos_vazio
        acoes = []
        
        if linha_vazio > 0:
            acoes.append("CIMA")
        if linha_vazio < self.tamanho - 1:
            acoes.append("BAIXO")
        if col_vazio > 0:
            acoes.append("ESQUERDA")
        if col_vazio < self.tamanho - 1:
            acoes.append("DIREITA")
        
        return acoes
    
    def aplicar_acao(self, acao: str) -> 'EstadoPuzzle':
        novo_tabuleiro = copy.deepcopy(self.tabuleiro)
        linha_vazio, col_vazio = self.pos_vazio
        
        if acao == "CIMA":
            novo_tabuleiro[linha_vazio][col_vazio] = novo_tabuleiro[linha_vazio - 1][col_vazio]
            novo_tabuleiro[linha_vazio - 1][col_vazio] = 0
        elif acao == "BAIXO":
            novo_tabuleiro[linha_vazio][col_vazio] = novo_tabuleiro[linha_vazio + 1][col_vazio]
            novo_tabuleiro[linha_vazio + 1][col_vazio] = 0
        elif acao == "ESQUERDA":
            novo_tabuleiro[linha_vazio][col_vazio] = novo_tabuleiro[linha_vazio][col_vazio - 1]
            novo_tabuleiro[linha_vazio][col_vazio - 1] = 0
        elif acao == "DIREITA":
            novo_tabuleiro[linha_vazio][col_vazio] = novo_tabuleiro[linha_vazio][col_vazio + 1]
            novo_tabuleiro[linha_vazio][col_vazio + 1] = 0
        
        return EstadoPuzzle(novo_tabuleiro, self.tamanho, self, acao, self.custo_g + 1)
    
    def __str__(self) -> str:
        resultado = ""
        for linha in self.tabuleiro:
            resultado += " ".join(f"{num:2}" if num != 0 else "  " for num in linha) + "\n"
        return resultado
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, EstadoPuzzle):
            return False
        return self.hash_estado == other.hash_estado
    
    def __hash__(self) -> int:
        return hash(self.hash_estado)

class ProblemaPuzzle:
    def __init__(self, estado_inicial: List[List[int]], tipo_puzzle: int = 8):
        self.tipo_puzzle = tipo_puzzle
        self.tamanho = int((tipo_puzzle + 1) ** 0.5)
        self.estado_inicial = EstadoPuzzle(estado_inicial, self.tamanho)
        self.estado_objetivo = self._gerar_estado_objetivo()
        
        if not self._configuracao_valida(estado_inicial):
            raise ValueError("Configuração inicial inválida para o puzzle")
    
    def _gerar_estado_objetivo(self) -> List[List[int]]:
        objetivo = []
        numero = 1
        
        for i in range(self.tamanho):
            linha = []
            for j in range(self.tamanho):
                if i == self.tamanho - 1 and j == self.tamanho - 1:
                    linha.append(0)
                else:
                    linha.append(numero)
                    numero += 1
            objetivo.append(linha)
        
        return objetivo
    
    def _configuracao_valida(self, tabuleiro: List[List[int]]) -> bool:
        if len(tabuleiro) != self.tamanho:
            return False
        
        for linha in tabuleiro:
            if len(linha) != self.tamanho:
                return False
        
        numeros = set()
        for linha in tabuleiro:
            for num in linha:
                numeros.add(num)
        
        esperados = set(range(self.tipo_puzzle + 1))
        return numeros == esperados
    
    def eh_solucionavel(self) -> bool:
        lista = []
        pos_vazio = 0
        
        for i, linha in enumerate(self.estado_inicial.tabuleiro):
            for j, num in enumerate(linha):
                if num == 0:
                    pos_vazio = i
                else:
                    lista.append(num)
        
        inversoes = 0
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i] > lista[j]:
                    inversoes += 1
        
        if self.tamanho % 2 == 1:
            return inversoes % 2 == 0
        else:
            if (self.tamanho - pos_vazio) % 2 == 1:
                return inversoes % 2 == 0
            else:
                return inversoes % 2 == 1
    
    def obter_sucessores(self, estado: EstadoPuzzle) -> List[EstadoPuzzle]:
        sucessores = []
        acoes_possiveis = estado.obter_acoes_possiveis()
        
        for acao in acoes_possiveis:
            novo_estado = estado.aplicar_acao(acao)
            sucessores.append(novo_estado)
        
        return sucessores
    
    def reconstruir_caminho(self, estado_final: EstadoPuzzle) -> List[EstadoPuzzle]:
        caminho = []
        estado_atual = estado_final
        
        while estado_atual is not None:
            caminho.append(estado_atual)
            estado_atual = estado_atual.pai
        
        return list(reversed(caminho))
    
    def imprimir_solucao(self, caminho: List[EstadoPuzzle], tempo_execucao: float, nos_expandidos: int, nos_gerados: int) -> None:
        print(f"\n{'='*50}\nSOLUÇÃO ENCONTRADA\n{'='*50}")
        print(f"\nPassos: {len(caminho) - 1}, Tempo: {tempo_execucao:.4f}s, Nós expandidos: {nos_expandidos}, Nós gerados: {nos_gerados}")
        
        print("\nSequência de movimentos:")
        for i, estado in enumerate(caminho):
            if i == 0:
                print(f"Estado inicial:")
            else:
                print(f"Passo {i} - Ação: {estado.acao}")
            print(estado)
            print("-" * 20)
    
    @staticmethod
    def criar_puzzle_exemplo(tipo: int) -> List[List[int]]:
        if tipo == 8:
            # Puzzle 8 com exatamente 20 passos para solução
            return [[7, 2, 4], [5, 0, 6], [8, 3, 1]]  
        elif tipo == 15:
            # Puzzle 15 com aproximadamente 15+ passos
            return [
                [2, 3, 4, 8],
                [1, 6, 0, 12], 
                [5, 10, 7, 11],
                [9, 13, 14, 15]
            ]  
        elif tipo == 24:
            # Puzzle 24 com aproximadamente 18+ passos
            return [
                [1, 2, 3, 9, 4],
                [6, 7, 8, 5, 10],
                [11, 12, 13, 14, 15],
                [16, 17, 0, 18, 19],
                [21, 22, 23, 24, 20]
            ]
        else:
            raise ValueError("Tipo de puzzle não suportado")
