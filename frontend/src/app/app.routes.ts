import { Routes } from '@angular/router';

import { Home } from './components/home/home';
import { Login } from './components/login/login';
import { Cadastro } from './components/cadastro/cadastro';
import { DescricaoResiduo } from './components/descricao-residuo/descricao-residuo';
import { Processamento } from './components/processamento/processamento';
import { Resultado } from './components/resultado/resultado';
import { ConfirmarDescarte } from './components/confirmar-descarte/confirmar-descarte';
import { Dashboard } from './components/dashboard/dashboard';
import {authGuard} from './guards/auth_guards';

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
    component: Cadastro,
  },
  {
    path: 'home',
    component: Home
  },
  {
    path: 'descricao',
    component: DescricaoResiduo,
    canActivate: [authGuard]
  },
  {
    path: 'processamento',
    component: Processamento,
    canActivate: [authGuard]
  },
  {
    path: 'resultado',
    component: Resultado,
    canActivate: [authGuard]
  },
  {
    path: 'confirmar-descarte',
    component: ConfirmarDescarte,
    canActivate: [authGuard]
  },
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  }
];
