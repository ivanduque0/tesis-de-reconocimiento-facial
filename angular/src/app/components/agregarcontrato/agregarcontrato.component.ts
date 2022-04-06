import { Component, OnInit } from '@angular/core';
import { contratos } from 'src/app/models/contratos.model';
import { WebService } from 'src/app/services/web.service';

@Component({
  selector: 'app-agregarcontrato',
  templateUrl: './agregarcontrato.component.html',
  styleUrls: ['./agregarcontrato.component.css']
})
export class AgregarcontratoComponent implements OnInit {

  contrato: contratos = new contratos();
  submitted=false;
  contratos?: contratos[];
  currentindex = -1;

  constructor(private webservice: WebService) { }

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

  removercontrato(contratooo:any){
    this.webservice.eliminarcontrato(contratooo)
    .subscribe(
      data => {
        contratooo = data;
        console.log(data);
      },
      error => {
        console.log(error);
      }); 
  }

  nuevocontrato(): void {
    this.submitted = false;
    this.contrato = new contratos()
  }

  guardarcontrato() {
    this.webservice.crearcontrato(this.contrato)
    .subscribe(
      data => {
        console.log(data);
        this.submitted = true;
      },
      error => {
        console.log(error);
      });
    this.contrato = new contratos();
  }

  
  onSubmit() {
    this.guardarcontrato();
    this.retrievecontratos();
  }


  onSubmit2() {
    this.retrievecontratos();
  }

}
