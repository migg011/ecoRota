import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

@Component({
  selector: 'app-resultado',
  imports: [RouterLink],
  templateUrl: './resultado.html',
  styleUrl: './resultado.scss'
})
export class Resultado implements OnInit {

  descricao = '';

  categoria = 'Eletrônico';

  ecopontos = [
    {
      id: 1,
      nome: 'Ecoponto Centro',
      endereco: 'Rua Exemplo, 100',
      horario: '08:00 às 17:00'
    },
    {
      id: 2,
      nome: 'Ecoponto Zona Norte',
      endereco: 'Av. Exemplo, 500',
      horario: '08:00 às 18:00'
    }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.descricao =
      this.route.snapshot.queryParamMap.get('descricao') ?? '';
  }
}
