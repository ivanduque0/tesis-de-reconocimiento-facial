import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AgregarcontratoComponent } from './components/agregarcontrato/agregarcontrato.component';
import { EditarcontratoComponent } from './components/editarcontrato/editarcontrato.component';
import { EditarusuarioComponent } from './components/editarusuario/editarusuario.component';
import { InteraccionesComponent } from './components/interacciones/interacciones.component';
import { SeleccionarcontratoComponent } from './components/seleccionarcontrato/seleccionarcontrato.component';
import { IndexComponent } from './components/index/index.component';

const routes: Routes = [

  { path: '', redirectTo: 'inicio', pathMatch: 'full' },
  { path: 'inicio', component: IndexComponent },
  { path: 'agregarcontrato', component: AgregarcontratoComponent },
  { path: 'seleccionarcontrato', component: SeleccionarcontratoComponent },
  { path: 'seleccionarcontrato/:contrato', component: EditarcontratoComponent },
  { path: 'editarusuarios/:cedula', component: EditarusuarioComponent },
  { path: 'interacciones', component: InteraccionesComponent }


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
