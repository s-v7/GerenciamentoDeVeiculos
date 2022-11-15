/*****************Sistema Gestão de Veículos ************************* */

import "primeicons/primeicons.css";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.css";
import ReactDOM from "react-dom";
import React, { useEffect, useRef, useState } from "react";
import { Toast } from "primereact/toast";
import { Menubar } from "primereact/menubar";
import { InputText } from "primereact/inputtext";
import api from "../service/api";
import "../../index.css";

const MenuDemo = () => {
  const toast = useRef(null);
  const [e, setApi] = useState("");

  useEffect(() => {
    api
      .get("/cars")
      .then((response) => setApi(response.data))
      .catch((err) => {
        console.error(`Ops! Ocorreu um erro${err}`);
      });
  }, []);

  const elementos = [
    {
      label: "Cadastra Veículo",
      icon: "pi pi-fw pi-car ",
      items: [
        {
          label: "New Categoria",
          icon: "pi pi-fw pi-plus",
          items: [
            {
              label: "Carros",
              icon: "pi pi-fw pi-car",
              items: [
                {
                  label: "Novos",
                  icon: "pi pi-fw pi-car",
                  command: (event) => {
                    event.originalEvent =
                      "../../pages/CadastrarVeiculos/CarrosNovos/createCarros.js";
                  },
                },
                {
                  label: "Semi-Novos",
                  icon: "pi pi-fw pi-car",
                },
              ],
            },
            {
              label: "Motos",
              icon: "pi pi-fw pi-moto",
              items: [
                {
                  label: "Novas",
                  icon: "pi pi-fw pi-car",
                  command: (event) => {
                    window.location.hash =
                      "../../pages/CadastrarVeiculos/CarrosNovos/createMotos.js";
                  },
                },
                {
                  label: "Semi-Novas",
                  icon: "pi pi-fw pi-car",
                },
              ],
            },
            {
              label: "Caminhões",
              icon: "pi pi-fw pi-car",
              items: [
                {
                  label: "Novos",
                  icon: "pi pi-fw pi-car",
                  command: (event) => {
                    event.location =
                      "../../pages/CadastrarVeiculos/CarrosNovos/createCaminhoes.js";
                  },
                },
                {
                  label: "Semi-Novos",
                  icon: "pi pi-fw pi-car",
                  command: (event) => {
                    event.target =
                      "../../pages/CadastrarVeiculos/CarrosNovos/createCarrosSemiNovos.html";
                  },
                },
              ],
            },
          ],
        },
        {
          label: "Icons",
          icon: "pi pi-fw pi-google",
          items: [
            { label: "Linkedin", icon: " pi pi-linkedin" },
            { label: "GitHub", icon: "pi pi-github" },
            { label: "Telegram", icon: " pi pi-telegram" },
            { label: "Facebook", icon: "pi pi-facebook" },
            { label: "Twitter", icon: "pi pi-twitter" },
            { label: "Whattsapp", icon: "pi pi-whatsapp" },
            { label: "Youtube", icon: "pi pi-youtube" },
            { label: "Instagram", icon: "pi pi-instagram" },
          ],
        },
        {
          separator: true,
        },
      ],
    },
    {
      label: "Lista de Veículos",
      icon: "pi pi-fw pi-list",
      items: [
        {
          label: "Novos",
          icon: "pi pi-fw pi-align-left",
          command: (event) => {
            event.target =
              "../pages/ListaDeVeiculos/VeiculosNovos/listaVeiculosNovos";
          },
        },
        {
          label: "Semi-Novos",
          icon: "pi pi-fw pi-align-right",
          command: (event) => {
            event.target =
              "../pages/ListaDeVeiculos/VeiculosNovos/listaVeiculosSemiNovos";
          },
        },
      ],
    },
    {
      label: "Controle De Veículos",
      icon: "pi pi-fw pi-calendar",
      items: [
        {
          label: "Rotas",
          icon: "pi pi-fw pi-pencil",
          items: [
            {
              label: "leftRoot",
              icon: "pi pi-fw pi-calendar-plus",
              url: "https://reactjs.org/",
            },
            {
              label: "rigthRoot",
              icon: "pi pi-fw pi-calendar-minus",
              command: (event) => {
                window.placeholder = "Silas";
              },
            },
          ],
        },
        {
          label: "ControleDeGastos",
          icon: "pi pi-fw pi-calendar-times",
          items: [
            {
              label: "Orçamentos",
              icon: "pi pi-fw pi-calendar-minus",
            },
          ],
        },
        {
          label: "Veículos em Manutenção",
          icon: "pi pi-fw pi-align-center",
          items: [
            {
              label: "Orçamentos",
              icon: "pi pi-fw pi-calendar-minus",
            },
          ],
        },
      ],
    },
    {
      label: "Users",
      icon: "pi pi-fw pi-user",
      items: [
        {
          label: "Novo",
          icon: "pi pi-fw pi-user-plus",
        },
        {
          label: "Excluir",
          icon: "pi pi-fw pi-user-minus",
        },
        {
          label: "Search",
          icon: "pi pi-fw pi-users",
          items: [
            {
              label: "Filter",
              icon: "pi pi-fw pi-filter",
              items: [
                {
                  label: "Print",
                  icon: "pi pi-fw pi-print",
                },
              ],
            },
            {
              icon: "pi pi-fw pi-bars",
              label: "List",
            },
          ],
        },
      ],
    },
  ];
  const end = (
    <InputText placeholder="Search" type="text" onClick={() => setApi("")} />
  );
  return (
    <div>
      <Toast ref={toast}></Toast>
      <header>
        <div className="card">
          <Menubar
            model={elementos}
            onClick={() => setApi(elementos.items)}
            end={end}
          />
        </div>
      </header>
      <div class="box-content">
        <section>
          <nav>
            <ul>
              <div class="container p-3 my-3 bg-dark text-#">
                <h1>Gestão de Veículos </h1>
                <p>S-v7</p>
              </div>
            </ul>
          </nav>
          <article>
            <h1>Florianópolis</h1>
            <p>Descrição: 0</p>
            <p>Descrição: 1</p>
          </article>
        </section>
      </div>
      <footer>
        <p>Footer</p>
      </footer>
    </div>
  );
};
const rootElement = document.getElementById("root");
ReactDOM.render(<MenuDemo />, rootElement);
