import { Component, OnInit } from '@angular/core';
import { contratos } from 'src/app/models/contratos.model';
import { usuarios } from 'src/app/models/usuarios.model';
import { WebService } from 'src/app/services/web.service';
@Component({
  selector: 'app-seleccionarcontrato',
  templateUrl: './seleccionarcontrato.component.html',
  styleUrls: ['./seleccionarcontrato.component.css']
})
export class SeleccionarcontratoComponent implements OnInit {
  contratoseleccionado:any = null;
  contratos?: contratos[];
  usuarios?: usuarios[];
  currentindex = -1;
  constructor(private webservice: WebService) {  }
  ngOnInit(): void {
    this.retrievecontratos();
  }

  retrievecontratos(): void {
    this.webservice.getAllcontratos()
      .subscribe(
        data => {
          this.contratos = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });  
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
}