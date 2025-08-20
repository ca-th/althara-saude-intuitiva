import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContatoComponent } from './contato/contato.component';
import { AboutComponent } from './components/about/about.component';

export const routes: Routes = [
  {
    path: 'contato',
    loadComponent: () => import('./contato/contato.component').then(m => m.ContatoComponent)
  },
  {
    path: '',
    component: HomeComponent
  },
  {
     path: 'sobre-nos',        // A URL que o usuário vai ver no navegador
    component: AboutComponent // O componente que será exibido nessa URL
  },
  {
    path: '**',
    redirectTo: '',
    pathMatch: 'full'
  }
];
