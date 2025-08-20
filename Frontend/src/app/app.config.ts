// No seu arquivo: src/app/app.config.ts

// 1. IMPORTE O 'provideZoneChangeDetection'
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    // 2. ADICIONE-O AQUI (A ORDEM NÃO IMPORTA)
    provideZoneChangeDetection({ eventCoalescing: true }),

    provideRouter(
      routes,
      withInMemoryScrolling({ scrollPositionRestoration: 'top' })
    ),
    provideAnimations(),
    provideHttpClient()
  ]
};
