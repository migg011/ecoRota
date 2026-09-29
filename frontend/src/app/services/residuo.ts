import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ClassificacaoResponse } from '../models/residuo.model';

@Injectable({
  providedIn: 'root'
})
export class ResiduoService {

  private readonly apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  classificarResiduo(descricao: string): Observable<ClassificacaoResponse> {
    return this.http.post<ClassificacaoResponse>(
      `${this.apiUrl}/classificar/`,
      {
        descricao: descricao
      }
    );
  }
}
