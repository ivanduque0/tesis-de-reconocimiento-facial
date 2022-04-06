import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { fotos } from 'src/app/models/fotos.model';
import { horariospermitidos } from 'src/app/models/horariospermitidos.model';
import { usuarios } from 'src/app/models/usuarios.model';
import { WebService } from 'src/app/services/web.service';

@Component({
  selector: 'app-editarusuario',
  templateUrl: './editarusuario.component.html',
  styleUrls: ['./editarusuario.component.css']
})
export class EditarusuarioComponent implements OnInit {
  diaseleccionado:any = null;
  entradaseleccionada:any = null;
  salidaseleccionada:any = null;
  submitted = false;
  horarios?: horariospermitidos[];
  usuarioslug:any = this.route.snapshot.paramMap.get("cedula");
  horariosagregar: horariospermitidos = {
    cedula: Number(this.usuarioslug),
    dia: this.diaseleccionado,
    entrada: this.entradaseleccionada,
    salida: this.salidaseleccionada

  }
  foto?: fotos[];
  nombre:any;
  diasdelasemana:string[] = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
  usuario?: usuarios[];
  constructor(private route:ActivatedRoute, private webservice: WebService) { 
    this.usuarioslug=this.route.snapshot.paramMap.get("cedula")
  }
  
  ngOnInit(): void {
    //console.log(this.usuarioslug)
    this.obtenerhorarios()
    this.obtenerusuario(this.usuarioslug)
    
  }

  obtenerhorarios() {

    this.webservice.obtenerhorarios(this.usuarioslug)
    .subscribe(
      data => {
        this.horarios = data;
        console.log(data);
      },
      error => {
        console.log(error);
      }); 
    }
  
  obtenerusuario(usuarioo:any) {
    this.webservice.buscarusuario(usuarioo)
    .subscribe(
      data => {
        this.usuario = data;
        console.log(data);
      },
      error => {
        console.log(error);
      });
    
  }
  
  nuevohorario(): void {
    this.submitted = false;
    this.horariosagregar = {
      cedula: Number(this.usuarioslug),
      dia: this.diaseleccionado,
      entrada: this.entradaseleccionada,
      salida: this.salidaseleccionada
    }
  }

  guardarhorario() {
    this.webservice.agregarhorarios(this.horariosagregar, this.usuarioslug)
    .subscribe(
      data => {
        console.log(data);
        this.submitted = true;
      },
      error => {
        console.log(error);
      });
      
  }

  removerhorario(horarioid:any): void {
    this.webservice.eliminarhorarios(horarioid)
    .subscribe(
      data => {
        console.log(data);
      },
      error => {
        console.log(error);
      }); 
    this.obtenerhorarios();

  }

  

  onSubmit() {
    this.guardarhorario();
    this.obtenerhorarios();
    this.diaseleccionado = null;
    this.entradaseleccionada = null;
    this.salidaseleccionada = null;
    this.nuevohorario();

  }
}
