import "primeicons/primeicons.css";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.css";
import "../../../../../index.css";
import ReactDOM from "react-dom";
import React from "react";

function MenuDemo() {
  return (
    <div>
      <div class="social__Container-snmkbf-0 kZbZeh">
        <header>
          <div class="box">
            <h2>Cadastrar Veículo</h2>
          </div>
        </header>

        <form action="">
          <div class="row">
            <div class="col">
              <input
                id="modelo"
                type="text"
                class="form-control"
                placeholder="Modelo Veículo"
                name="modelo"
              />
            </div>
            <div class="col">
              <input
                id="fabricante"
                type="text"
                class="form-control"
                placeholder="Fabricante"
                name="fabricante"
              />
            </div>
          </div>
          <div class="row">
            <div class="col">
              <input
                id="ano"
                type="datetime-local"
                class="form-control"
                placeholder="Ano Veículo"
                name="ano"
              />
            </div>
            <div class="col">
              <input
                id="placa"
                maxLength="7"
                type="number"
                class="form-control"
                placeholder="Placa"
                name="placa"
              />
            </div>
          </div>
          <div class="row">
            <div class="col">
              <input
                id="ano"
                type="text"
                class="form-control"
                placeholder="Tipo Combustível"
                name="ano"
              />
            </div>
            <div class="col">
              <input
                id="cor"
                type="text"
                class="form-control"
                placeholder="Cor Veículo"
                name="cor"
              />
            </div>
          </div>
          <div class="row">
            <div class="col">
              <button id="cancelar" type="submit" class="btn btn-danger">
                Cancelar
              </button>
            </div>
            <div class="col">
              <button id="update" type="button" class="btn btn-light">
                UpDate
              </button>
            </div>
            <div class="col">
              <button id="create" type="button" class="btn btn-primary">
                Cadastrar
              </button>
            </div>
          </div>
        </form>
      </div>
      <section class="social__Div-snmkbf-1 hmhymN">
        <footer>
          <p> &copy; 2022 Developer/ Programming Silas</p>
        </footer>
      </section>
    </div>
  );
}
const leftRootElement = document.getElementById("leftRoot");
ReactDOM.render(<MenuDemo />, leftRootElement);
