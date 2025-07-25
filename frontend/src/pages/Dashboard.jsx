import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [veiculos, setVeiculos] = useState([]);

  const fetchVeiculos = async () => {
    try {
      const res = await axios.get("http://localhost:3000/api/veiculos/cars");
      setVeiculos(res.data);
    } catch (err) {
      console.error("Erro ao buscar veículos:", err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Deseja excluir este veículo?")) return;
    try {
      await axios.delete(`http://localhost:3000/api/veiculos/cars/${id}`);
      setVeiculos(veiculos.filter((v) => v.id_veiculo !== id));
    } catch (err) {
      console.error("Erro ao deletar:", err);
    }
  };

  useEffect(() => {
    fetchVeiculos();
  }, []);

  return (
    <div className="p-6 text-white bg-gray-900 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-teal-400">
        🚗 Lista de Veículos
      </h1>
      <table className="w-full bg-gray-800 rounded shadow">
        <thead>
          <tr className="text-left text-teal-300 border-b border-gray-700">
            <th className="p-2">Modelo</th>
            <th className="p-2">Marca</th>
            <th className="p-2">Ano</th>
            <th className="p-2">Placa</th>
            <th className="p-2">Cor</th>
            <th className="p-2">Ações</th>
          </tr>
        </thead>
        <tbody>
          {veiculos.map((v) => (
            <tr key={v.id_veiculo} className="border-b border-gray-700">
              <td className="p-2">{v.modelo}</td>
              <td className="p-2">{v.marca}</td>
              <td className="p-2">{v.anoVeiculo}</td>
              <td className="p-2">{v.placa}</td>
              <td className="p-2">{v.corVeiculo}</td>
              <td className="p-2 space-x-2">
                <button
                  className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
                  onClick={() => handleDelete(v.id_veiculo)}
                >
                  Excluir
                </button>
                <button
                  className="bg-yellow-500 hover:bg-yellow-600 px-3 py-1 rounded"
                  onClick={() => alert("TODO: Editar veículo")}
                >
                  Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
