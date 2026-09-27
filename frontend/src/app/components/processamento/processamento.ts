import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-processamento',
  imports: [],
  templateUrl: './processamento.html',
  styleUrl: './processamento.scss'
})
export class Processamento implements OnInit {

  descricao = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.descricao = this.route.snapshot.queryParamMap.get('descricao') ?? '';

    setTimeout(() => {
      this.router.navigate(['/resultado'], {
        queryParams: {
          descricao: this.descricao
        }
      });
    }, 2000);
  }
}
