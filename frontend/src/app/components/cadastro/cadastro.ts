import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService, RegistroData } from '../../services/auth';

@Component({
  selector: 'app-cadastro',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './cadastro.html',
  styleUrl: './cadastro.scss'
})
export class Cadastro {
  userData: RegistroData = {
    nome_completo: '',
    email: '',
    password: ''
  };

  errorMessage: string = '';
  loading: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    if (!this.userData.nome_completo || !this.userData.email || !this.userData.password) {
      this.errorMessage = 'Preencha todos os campos obrigatórios.';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService.registrar(this.userData).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/descricao']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || 'Erro ao realizar cadastro. Verifique os dados.';
      }
    });
  }
}
