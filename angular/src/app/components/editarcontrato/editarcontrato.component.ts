import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { usuarios } from 'src/app/models/usuarios.model';
import { WebService } from 'src/app/services/web.service';

@Component({
  selector: 'app-editarcontrato',
  templateUrl: './editarcontrato.component.html',
  styleUrls: ['./editarcontrato.component.css']
})
export class EditarcontratoComponent implements OnInit {

  usuarios?: usuarios[];
  usuariosbuscar?: usuarios[];
  //usuario: usuarios = new usuarios();
  contratoslug:any;
  submitted=false;
  cedulabuscar:any;
  usuario: usuarios = {
    contrato: this.route.snapshot.paramMap.get("contrato")
  };
  constructor(private route:ActivatedRoute, private webservice: WebService) { this.contratoslug=this.route.snapshot.paramMap.get("contrato")}
  
  ngOnInit(): void {
    //console.log(this.route.snapshot.paramMap.get("contrato"))
    this.seleccion(this.contratoslug)
  }

  seleccion(contratoseleccionado:any): void {

    this.webservice.seleccionarcontrato(contratoseleccionado)
    .subscribe(
      data => {
        this.usuarios = data;
        console.log(data);
      },
      error => {
        console.log(error);
      }); 
    }

  nuevousuario(): void {
    this.submitted = false;
    this.usuario = new usuarios()
  }
  guardarusuario() {
    this.webservice.agregarusuario(this.usuario)
    .subscribe(
      data => {
        console.log(data);
        this.submitted = true;
      },
      error => {
        console.log(error);
      });
    this.usuario = {
      contrato: this.contratoslug
    };
  }

  removerusuario(cedulausuario:any){
    this.webservice.eliminarusuario(cedulausuario)
    .subscribe(
      data => {
        cedulausuario = data;
        console.log(data);
      },
      error => {
        console.log(error);
      }); 
    
    // this.seleccion(this.contratoslug)
  }

  buscaruser(cedulausuario:any) {

    this.webservice.buscarusuario(cedulausuario)

    .subscribe(
    data => {
      this.usuariosbuscar = data;
      console.log(data);
    },
    error => {
      console.log(error);
    });
  }
  onSubmit() {
    this.guardarusuario();
    this.seleccion(this.contratoslug);
  }
  onSubmit2() {
    this.seleccion(this.contratoslug);
  }
  // onSubmit3() {
  //   this.buscaruser(this.cedulabuscar);
  // }
}
