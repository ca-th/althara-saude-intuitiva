import { inject } from '@angular/core';
import { CanActivateFn, Router, UrlTree } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state): boolean | UrlTree => {
  const authService = inject(AuthService);
  const router = inject(Router);


  if (authService.isLoggedIn()) {
    return true; // usuário logado, permite o acesso.
  }

  return router.createUrlTree(['/login']);
};
