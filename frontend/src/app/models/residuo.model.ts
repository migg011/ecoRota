export interface Destino {
  id: number;
  categoria: string;
  endereco: string;
  descricao: string;
}

export interface ClassificacaoResponse {
  categoria: string;
  destinos: Destino[];
}
