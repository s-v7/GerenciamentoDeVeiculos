/*****************Sistema Gestão de Veículos ************************* */

import "primeicons/primeicons.css";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.css";
import "primeflex/primeflex.css";
import { Toast } from "primereact/toast";
import ReactDOM from "react-dom";
import { Menubar } from "primereact/menubar";
import { InputText } from "primereact/inputtext";
import React, { useRef, useState } from "react";

import "./index.css";
import Link from "next/link";

const MenuDemo = () => {
  const toast = useRef(null);
  const [e, setApi] = useState("");

  const elementos = [
    {
      label: "Cadastrar Veículo",
      icon: "pi pi-fw pi- ",
      items: [
        {
          label: "New Categoria",
          icon: "pi pi-fw pi-plus",
          items: [
            {
              label: "Carros",
              icon: "pi pi-fw pi-car",
            },
            {
              label: "Motos",
              icon: "pi pi-fw pi-moto",
            },
            {
              label: "Caminhões",
              icon: "pi pi-fw pi-car",
            },
          ],
        },
        {
          separator: true,
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
                // window.placeholder = "Silas";
              },
            },
          ],
        },
        {
          label: "Controllers the Gastos",
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
      label: "Lavação De Veículos",
      icon: "pi pi-fw pi-user",
      items: [
        {
          label: "NovoCliente",
          icon: "pi pi-fw pi-user-plus",
        },
        {
          label: "Controle Entrada/Saída",
          icon: "pi pi-fw pi-users",
          items: [
            {
              label: "Gastos",
              icon: "pi pi-fw pi-filter",
              items: [
                {
                  label: "Água",
                  icon: "pi pi-fw pi-print",
                },
                { label: "Energia", icon: "pi pi-fw" },
                {
                  label: "Materiais de Limpeza Ambiente",
                  icon: "pi pi-fw pi-print",
                },
                {
                  label: "Materiais de Limpeza Veículos",
                  icon: "pi pi-fw pi-print",
                },
              ],
            },
          ],
        },
      ],
    },
    {
      label: "Listas De Veículos",
      icon: "pi pi-fw pi-list",
      items: [
        {
          label: "Carros",
          icon: "pi pi-fw pi-align-left",
          command: (event) => {
            event.target =
              "../pages/ListaDeVeiculos/VeiculosNovos/listaVeiculosNovos";
          },
        },
        {
          label: "Motos",
          icon: "pi pi-fw pi-align-right",
          command: (event) => {
            <a href="../pages/ListaDeVeiculos/VeiculosNovos/listaVeiculosSemiNovos" />;
          },
        },
        {
          label: "Caminhões",
          icon: "pi pi-fw",
          command: (e) => {},
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
      <Menubar
        model={elementos}
        onClick={() => setApi(elementos.items)}
        end={end}
      />
      <div class="intro__Container-t6zelt-0 fVRacF">
        <div class="downarrow__Div-wpkbq-0 csGZZd">
          <div class="downarrow__Line-wpkbq-1 byozZi out">
            <nav>
              <ul>
                <li>
                  <Link href="https://google.com">
                    <a>Home</a>
                  </Link>
                </li>
                <h1>Silas</h1>
                <h2>Gestão de Veículos</h2>
              </ul>
            </nav>
            <h1>O seu sistema favorito ...</h1>
            <p>
              Bootstrap is the most popular HTML, CSS, and JS framework for
              developing responsive, mobile-first projects on the web.
            </p>
            <p>↓</p>
          </div>
        </div>
      </div>
      <section class="projects__PreviousWork-sc-18cc2t5-2 gEPFHP">
        <p>This is some text.</p>
        <p>This is another text.</p>
      </section>
      <div class="social__Container-snmkbf-0 kZbZeh">
        <h2>Internet</h2>
        <section class="social__Div-snmkbf-1 hmhymN">
          <p> &copy; 2022 Silas</p>
          <a
            aria-label="Twitter"
            href="https://twitter.com/SilasV7"
            rel="noopener noreferrer"
          >
            <img
              alt="Twitter"
              src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMjRweCIgaGVpZ2h0PSIyMHB4IiB2aWV3Qm94PSIwIDAgMjQgMjAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDUyLjYgKDY3NDkxKSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT50d2l0dGVyPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IlBhZ2UtMSIgc3Ryb2tlPSJub25lIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgICAgICAgPGcgaWQ9InR3aXR0ZXIiIGZpbGw9IiM3Nzc3NzciPgogICAgICAgICAgICA8cGF0aCBkPSJNMjMuOTU0LDIuNTY5IEMyMy4wNjksMi45NTggMjIuMTI0LDMuMjIzIDIxLjEyOSwzLjM0NCBDMjIuMTQzLDIuNzMzIDIyLjkyMywxLjc3IDIzLjI5MiwwLjYyMSBDMjIuMzQxLDEuMTc2IDIxLjI4NywxLjU4IDIwLjE2NSwxLjgwNSBDMTkuMjY5LDAuODQ2IDE3Ljk5MiwwLjI0NiAxNi41NzQsMC4yNDYgQzEzLjg1NywwLjI0NiAxMS42NTQsMi40NDkgMTEuNjU0LDUuMTYzIEMxMS42NTQsNS41NTMgMTEuNjk5LDUuOTI4IDExLjc4MSw2LjI4NyBDNy42OTEsNi4wOTQgNC4wNjYsNC4xMyAxLjY0LDEuMTYxIEMxLjIxMywxLjg4MyAwLjk3NCwyLjcyMiAwLjk3NCwzLjYzNiBDMC45NzQsNS4zNDYgMS44NDQsNi44NDkgMy4xNjIsNy43MzIgQzIuMzU1LDcuNzA2IDEuNTk2LDcuNDg0IDAuOTM0LDcuMTE2IEwwLjkzNCw3LjE3NyBDMC45MzQsOS41NjIgMi42MjcsMTEuNTUxIDQuODgsMTIuMDA0IEM0LjQ2NywxMi4xMTUgNC4wMzEsMTIuMTc1IDMuNTg0LDEyLjE3NSBDMy4yNywxMi4xNzUgMi45NjksMTIuMTQ1IDIuNjY4LDEyLjA4OSBDMy4yOTksMTQuMDQyIDUuMTEzLDE1LjQ2NiA3LjI3MiwxNS41MDYgQzUuNTkyLDE2LjgyNSAzLjQ2MywxNy42MTEgMS4xNywxNy42MTEgQzAuNzgsMTcuNjExIDAuMzkxLDE3LjU4OCAxLjc3NjM1Njg0ZS0xNSwxNy41NDQgQzIuMTg5LDE4LjkzOCA0Ljc2OCwxOS43NTMgNy41NTcsMTkuNzUzIEMxNi42MTEsMTkuNzUzIDIxLjU1NiwxMi4yNTcgMjEuNTU2LDUuNzY3IEMyMS41NTYsNS41NTggMjEuNTU2LDUuMzQ3IDIxLjU0MSw1LjEzNyBDMjIuNTAyLDQuNDQ4IDIzLjM0MSwzLjU3NyAyNC4wMDEsMi41ODkgTDIzLjk1NCwyLjU2OSBaIiBpZD0iUGF0aCI+PC9wYXRoPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+"
            />
          </a>
          <a
            aria-label="Telegram"
            href="https://sv-7/sv-7"
            rel="noopener noreferrer"
          >
            <img
              alt="Telegram"
              src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMjRweCIgaGVpZ2h0PSIyMnB4IiB2aWV3Qm94PSIwIDAgMjQgMjIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDUyLjYgKDY3NDkxKSAtIGh0dHA6Ly93d3cuYm9oZW1pYW5jb2RpbmcuY29tL3NrZXRjaCAtLT4KICAgIDx0aXRsZT50ZWxlZ3JhbTwvdGl0bGU+CiAgICA8ZGVzYz5DcmVhdGVkIHdpdGggU2tldGNoLjwvZGVzYz4KICAgIDxnIGlkPSJQYWdlLTEiIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJ0ZWxlZ3JhbSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEuMDAwMDAwLCAwLjAwMDAwMCkiIGZpbGw9IiM3Nzc3NzciPgogICAgICAgICAgICA8cGF0aCBkPSJNMjQuOTEsMi43OSBMMjEuMywxOS44NCBDMjEuMDUsMjEuMDUgMjAuMzIsMjEuMzQgMTkuMywyMC43OCBMMTMuOCwxNi43MSBMMTEuMTQsMTkuMjggQzEwLjg0LDE5LjU4IDEwLjU5LDE5Ljg0IDEwLjA0LDE5Ljg0IEM5LjMyLDE5Ljg0IDkuNDQsMTkuNTcgOS4yLDE4Ljg5IEw3LjMsMTIuNyBMMS44NSwxMSBDMC42NywxMC42NSAwLjY2LDkuODQgMi4xMSw5LjI1IEwyMy4zNywxLjA1IEMyNC4zNCwwLjYyIDI1LjI3LDEuMjkgMjQuOSwyLjc4IEwyNC45MSwyLjc5IFoiIGlkPSJQYXRoIj48L3BhdGg+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4="
            />
          </a>
        </section>
      </div>
    </div>
  );
};

const rootElement = document.getElementById("root");
ReactDOM.render(<MenuDemo />, rootElement);
