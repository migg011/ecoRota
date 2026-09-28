import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-confirmar-descarte',
  imports: [FormsModule],
  templateUrl: './confirmar-descarte.html',
  styleUrl: './confirmar-descarte.scss'
})
export class ConfirmarDescarte implements OnInit {

  ecoponto = {
    nome: 'Ecoponto Centro',
    endereco: 'Rua Exemplo, 100',
    horario: '08:00 às 17:00'
  };

  confirmou = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const nome = this.route.snapshot.queryParamMap.get('nome');
    const endereco = this.route.snapshot.queryParamMap.get('endereco');
    const horario = this.route.snapshot.queryParamMap.get('horario');

    if (nome && endereco && horario) {
      this.ecoponto = {
        nome,
        endereco,
        horario
      };
    }
  }

  confirmarDescarte(): void {
    if (!this.confirmou) {
      return;
    }

    this.router.navigate(['/dashboard']);
  }

  voltarParaResultado(): void {
    this.router.navigate(['/resultado']);
  }
}
