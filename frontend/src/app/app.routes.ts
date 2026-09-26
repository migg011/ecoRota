import { Routes } from '@angular/router';

import { Home } from './components/home/home';
import { Login } from './components/login/login';
import { Cadastro } from './components/cadastro/cadastro';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: Login
  },
  {
    path: 'cadastro',
    component: Cadastro
  },
  {
    path: 'home',
    component: Home
  }
];
