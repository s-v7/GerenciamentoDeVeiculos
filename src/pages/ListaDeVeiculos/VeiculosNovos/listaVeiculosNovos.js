import "primeicons/primeicons.css";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.css";
import "../../../index.css";
import ReactDOM from "react-dom";
import React, { useState, useEffect } from "react";
import api from "./services/api";

const DataTableSizeDemo = () => {
  const [e, setApi] = useState("");
  useEffect(() => {
    api
      .get("/api/cars")
      .then((response) => setApi(response.data))
      .catch((err) => {
        console.error("ops! ocorreu um erro" + err);
      });
  }, []);
  return (
    <div>
      <div className="box-content">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <div className=".table-sm">
                <th scope="row">Lista de Veículos</th>
                <tr>
                  <th scope="col">Código</th>
                  <th scope="col">Title</th>
                  <th scope="col">Brand</th>
                  <th scope="col">Preço</th>
                  <th scope="col">Ano</th>
                  <th scope="col">Manutenção</th>
                </tr>
                <tr>
                  <td>"63286c1b94a4c4001c3e16bf"</td>
                  <td>"Civic sedan"</td>
                  <td>"Honda"</td>
                  <td>2020</td>
                  <td>"160.000,00"</td>
                </tr>

                <tr>
                  <td>"63286c1b94a4c4001c3e16bf"</td>
                  <td>"Civic sedan"</td>
                  <td>"Honda"</td>
                  <td>2020</td>
                  <td>"160.000,00"</td>
                </tr>

                <tr>
                  <td>"63286c1b94a4c4001c3e16bf"</td>
                  <td>"Civic sedan"</td>
                  <td>"Honda"</td>
                  <td>2020</td>
                  <td>"160.000,00"</td>
                </tr>
              </div>
            </thead>
          </table>
        </div>
      </div>
      <tbody>
        <div class="footer">
          <a href="/delReq/{{id_user}}">
            <button type="submit" class="btn btn-success">
              Editar
            </button>
          </a>
          <a href="/editForm/{{id_user}}">
            <button type="submit" class="btn btn-danger">
              Apagar
            </button>
          </a>
        </div>
      </tbody>
    </div>
  );
};
const rootElement = document.getElementById("root");
ReactDOM.render(<DataTableSizeDemo />, rootElement);
