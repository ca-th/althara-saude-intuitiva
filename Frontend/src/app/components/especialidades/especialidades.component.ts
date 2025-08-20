// No arquivo: src/app/components/especialidades/especialidades.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
// Importamos Medico também
import { ApiService, Especialidade, Medico } from '../../services/api.service';

@Component({
  selector: 'app-especialidades',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './especialidades.component.html',
  styleUrls: ['./especialidades.component.css']
})
export class EspecialidadesComponent implements OnInit {

  especialidades: Especialidade[] = [];

  // Novas propriedades para controlar o que é exibido
  especialidadeSelecionadaId: number | null = null;
  medicosDaEspecialidade: Medico[] = [];
  isLoadingMedicos = false;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getEspecialidades().subscribe(dados => {
      this.especialidades = dados;
    });
  }

  // Nova função que será chamada pelo clique
  onEspecialidadeClick(especialidade: Especialidade): void {
    // Se o usuário clicar no mesmo card que já está aberto, feche-o
    if (this.especialidadeSelecionadaId === especialidade.id_especialidade) {
      this.especialidadeSelecionadaId = null;
      this.medicosDaEspecialidade = [];
      return;
    }

    this.isLoadingMedicos = true;
    this.especialidadeSelecionadaId = especialidade.id_especialidade;
    this.medicosDaEspecialidade = []; // Limpa a lista anterior

    this.apiService.getMedicosPorEspecialidade(especialidade.id_especialidade)
      .subscribe(medicos => {
        this.medicosDaEspecialidade = medicos;
        this.isLoadingMedicos = false;
      });
  }
}
