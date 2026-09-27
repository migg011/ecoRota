import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-descricao-residuo',
  imports: [FormsModule, RouterLink],
  templateUrl: './descricao-residuo.html',
  styleUrl: './descricao-residuo.scss'
})
export class DescricaoResiduo {

  descricao = '';

  constructor(private router: Router) {}

  analisarResiduo(): void {

    if (this.descricao.trim() === '') {
      return;
    }

    this.router.navigate(['/processamento'], {
      queryParams: {
        descricao: this.descricao.trim()
      }
    });
  }
}
