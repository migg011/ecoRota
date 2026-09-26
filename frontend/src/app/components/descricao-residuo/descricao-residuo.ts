import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-descricao-residuo',
  imports: [FormsModule, RouterLink],
  templateUrl: './descricao-residuo.html',
  styleUrl: './descricao-residuo.scss'
})
export class DescricaoResiduo {

  descricao = '';
  enviado = false;

  analisarResiduo(): void {
    if (this.descricao.trim() === '') {
      return;
    }

    this.enviado = true;

    console.log('Descrição enviada:', this.descricao);
  }
}
