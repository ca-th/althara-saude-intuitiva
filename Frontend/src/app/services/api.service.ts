// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Especialidade {
  id_especialidade: number;
  nome: string;
}

export interface Medico {
  id_medico: number;
  nome: string;
  id_especialidade: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  // Função que busca as especialidades
  getEspecialidades(): Observable<Especialidade[]> {
    return this.http.get<Especialidade[]>(`${this.apiUrl}/especialidades`);
  } // <-- A função termina aqui

  // A nova função começa aqui, no mesmo nível da anterior
  getMedicosPorEspecialidade(id: number): Observable<Medico[]> {
    return this.http.get<Medico[]>(`${this.apiUrl}/especialidades/${id}/medicos`);
  }
}
