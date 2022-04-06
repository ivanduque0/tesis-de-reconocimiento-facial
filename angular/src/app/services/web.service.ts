import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { contratos } from '../models/contratos.model';
import { fotos } from '../models/fotos.model';
import { usuarios } from '../models/usuarios.model';
import { horariospermitidos } from '../models/horariospermitidos.model';
import { interacciones } from '../models/interacciones.model';
const baseUrl = 'http://localhost:1010';

@Injectable({
  providedIn: 'root'
})
export class WebService {

  private baaseUrl = 'http://localhost:1010';

  constructor(private http: HttpClient) { }

  getAllcontratos(): Observable<contratos[]> {
    return this.http.get<contratos[]>(baseUrl+"/agregarcontratosapi/")
  }
  
  agregarusuario(usuario:Object): Observable<Object> {
    return this.http.post(`${this.baaseUrl}/editcontrato/agregarusuario/`,usuario)
  }

  eliminarusuario(usuario:Object): Observable<Object> {
    return this.http.delete(`${this.baaseUrl}/editcontrato/eliminarusuario/${usuario}/`)
  }
  
  buscarusuario(usuario:Object): Observable<usuarios[]> {
    return this.http.get<usuarios[]>(`${this.baaseUrl}/editcontrato/buscarusuario/${usuario}/`,usuario)
  }
  crearcontrato(contrato:Object): Observable<Object> {
    return this.http.post(`${this.baaseUrl}/agregarcontratosapi/`,contrato)
  }
  eliminarcontrato(contrato:any): Observable<any> {
    return this.http.delete(`${this.baaseUrl}/removercontratosapi/${contrato}/`)
  }
  seleccionarcontrato(contrato:any): Observable<any> {
    return this.http.post(`${this.baaseUrl}/seleccionarcontrato/${contrato}/`,contrato)
  }

  agregarhorarios(horarios:Object, usuario:any): Observable<Object> {
    return this.http.post(`${this.baaseUrl}/editusuario/horarios/${usuario}/`,horarios)
  }

  eliminarhorarios(horarioid:any): Observable<any> {
    return this.http.delete(`${this.baaseUrl}/editusuario/horarios/${horarioid}/`)
  }
  obtenerhorarios(usuario:Object): Observable<horariospermitidos[]> {
    return this.http.get<horariospermitidos[]>(`${this.baaseUrl}/editusuario/horarios/${usuario}/`,usuario)
  }

  agregarfoto(usuario:Object): Observable<Object> {
    return this.http.post(`${this.baaseUrl}/editusuario/foto/${usuario}/`,usuario)
  }

  obtenerfoto(usuario:Object): Observable<horariospermitidos[]> {
    return this.http.get<fotos[]>(`${this.baaseUrl}/editusuario/foto/${usuario}/`,usuario)
  }


}
