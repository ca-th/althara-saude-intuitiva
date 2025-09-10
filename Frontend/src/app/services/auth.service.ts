import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

// dados de cadastro
export interface UserCreateData {
  nome: string;
  email: string;
  password: string;
}

// sucesso do cadastro/perfil
export interface User {
  id_usuario: number;
  nome: string;
  email: string;
}

// resposta do login
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000';
  private tokenKey = 'auth_token';

  constructor(private http: HttpClient) { }

  /**
   * Envia os dados de um novo usuário para a API para registro.
   * @param userData Os dados do usuário a serem cadastrados.
   * @returns Um Observable com os dados do usuário criado.
   */
  cadastrar(userData: UserCreateData): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/usuarios/`, userData);
  }

  /**
   * Envia as credenciais do usuário para a API para autenticação.
   * @param credentials Objeto com 'username' (email) e 'password'.
   * @returns Um Observable com a resposta do token.
   */
  login(credentials: any): Observable<TokenResponse> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
    // dados como um formulário (form data)
    const body = `username=${encodeURIComponent(credentials.username)}&password=${encodeURIComponent(credentials.password)}`;

    return this.http.post<TokenResponse>(`${this.apiUrl}/login`, body, { headers }).pipe(
      tap(response => {

        if (response.access_token) {
          localStorage.setItem(this.tokenKey, response.access_token);
        }
      })
    );
  }

  /**

   * @returns `true` se o token existir, caso contrário `false`.
   */
  public isLoggedIn(): boolean {
    const token = localStorage.getItem(this.tokenKey);

    return !!token;
  }


  public logout(): void {
    localStorage.removeItem(this.tokenKey);

  }
}
