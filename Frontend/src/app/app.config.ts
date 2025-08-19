import { ApplicationConfig } from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http'; // Importante para a API

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      // Garante que a rolagem seja restaurada ao topo em novas páginas
      withInMemoryScrolling({ scrollPositionRestoration: 'top' })
    ),
    // Necessário para as animações do Angular, como @fadeIn
    provideAnimations(),
    // Necessário para fazer chamadas à sua API (backend)
    provideHttpClient()
  ]
};
