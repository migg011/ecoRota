import { Routes } from '@angular/router';

import { Home } from './components/home/home';
import { Login } from './components/login/login';
import { Cadastro } from './components/cadastro/cadastro';
import { DescricaoResiduo } from './components/descricao-residuo/descricao-residuo';
import { Processamento } from './components/processamento/processamento';
import { Resultado } from './components/resultado/resultado';
import { ConfirmarDescarte } from './components/confirmar-descarte/confirmar-descarte';
import { Dashboard } from './components/dashboard/dashboard';

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
  },
  {
    path: 'descricao',
    component: DescricaoResiduo
  },
  {
    path: 'processamento',
    component: Processamento
  },
  {
    path: 'resultado',
    component: Resultado
  },
  {
    path: 'confirmar-descarte',
    component: ConfirmarDescarte
  },
  {
    path: 'dashboard',
    component: Dashboard
  }
];
