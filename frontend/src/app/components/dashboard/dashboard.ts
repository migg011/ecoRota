import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard {

  registros = [
    {
      id: 1,
      residuo: 'Televisão quebrada',
      categoria: 'Eletrônico',
      ecoponto: 'Ecoponto Centro',
      data: '28/09/2026',
      status: 'Intenção confirmada'
    },
    {
      id: 2,
      residuo: 'Caixas de papelão',
      categoria: 'Reciclável',
      ecoponto: 'Ecoponto Zona Norte',
      data: '27/09/2026',
      status: 'Intenção confirmada'
    },
    {
      id: 3,
      residuo: 'Pilhas usadas',
      categoria: 'Resíduo especial',
      ecoponto: 'Ecoponto Zona Sul',
      data: '25/09/2026',
      status: 'Intenção confirmada'
    }
  ];
}
