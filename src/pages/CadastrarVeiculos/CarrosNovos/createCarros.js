import "primeicons/primeicons.css";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.css";
import "../../../index.css";
import ReactDOM from "react-dom";
import React from "react";

function MenuDemo() {
  return (
    <div>
      <header>
        <div class="box">
          <h2>Cadastrar Veículo</h2>
        </div>
      </header>
      <form action="">
        <div class="row">
          <div class="col">
            <input
              type="text"
              class="form-control"
              id="modelo"
              placeholder="Modelo Veículo"
              name="modelo"
            />
          </div>
          <div class="col">
            <input
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
              type="datetime-local"
              class="form-control"
              id="ano"
              placeholder="Ano Veículo"
              name="ano"
            />
          </div>
          <div class="col">
            <input
              maxLength="7"
              type="number"
              class="form-control"
              id="placa"
              placeholder="Placa"
              name="placa"
            />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <input
              type="text"
              class="form-control"
              id="ano"
              placeholder="Tipo Combustível"
              name="ano"
            />
          </div>
          <div class="col">
            <input
              type="text"
              class="form-control"
              id="cor"
              placeholder="Cor Veículo"
              name="cor"
            />
          </div>
        </div>
        <div class="form-group form-check">
          <label class="form-check-label">
            <input class="form-check-input" type="checkbox" Remember me />
          </label>
        </div>
        <div class="row">
          <div class="col">
            <button type="submit" class="btn btn-danger">
              Cancelar
            </button>
          </div>
          <div class="col">
            <button type="button" class="btn btn-outline-success">
              Cadastrar
            </button>
          </div>
        </div>
      </form>
      <footer>
        <p>Programador/Desenvolvedor Full Stack Silas Vasconcelos</p>
      </footer>
    </div>
  );
}

const leftRootElement = document.getElementById("leftRoot");
ReactDOM.render(<MenuDemo />, leftRootElement);
