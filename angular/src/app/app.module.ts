import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AgregarcontratoComponent } from './components/agregarcontrato/agregarcontrato.component';
import { EditarcontratoComponent } from './components/editarcontrato/editarcontrato.component';
import { EditarusuarioComponent } from './components/editarusuario/editarusuario.component';
import { InteraccionesComponent } from './components/interacciones/interacciones.component';
import { SeleccionarcontratoComponent } from './components/seleccionarcontrato/seleccionarcontrato.component';
import { IndexComponent } from './components/index/index.component';

@NgModule({
  declarations: [
    AppComponent,
    AgregarcontratoComponent,
    EditarcontratoComponent,
    EditarusuarioComponent,
    InteraccionesComponent,
    SeleccionarcontratoComponent,
    IndexComponent
  ],
  imports: [
    FormsModule,
    HttpClientModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
