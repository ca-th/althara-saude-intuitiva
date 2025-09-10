import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContatoComponent } from './contato/contato.component';
import { AboutComponent } from './components/about/about.component';
import { CadastroComponent } from './pages/cadastro/cadastro.component';
import { LoginComponent } from './pages/login/login.component';
import { AreaPacienteComponent } from './pages/area-paciente/area-paciente.component';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [

  { path: '', component: HomeComponent },
  { path: 'sobre-nos', component: AboutComponent },
  { path: 'contato', component: ContatoComponent },

  //  autenticação
  { path: 'cadastro', component: CadastroComponent },
  { path: 'login', component: LoginComponent },


  {
    path: 'area-paciente',
    component: AreaPacienteComponent,
    canActivate: [authGuard]
  },


  { path: '**', redirectTo: '', pathMatch: 'full' }
];

