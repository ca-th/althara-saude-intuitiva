// No seu arquivo: src/main.ts

import 'zone.js'; // <-- ADICIONE ESTA LINHA DE VOLTA, NO TOPO

import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
