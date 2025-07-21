import React, { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/login", { email, senha });
      localStorage.setItem("token", response.data.token);
      navigate("/dashboard");
    } catch (err) {
      setErro("Email ou senha inválidos");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-900 text-white">
      <form
        onSubmit={handleLogin}
        className="bg-gray-800 p-8 rounded-lg shadow-md w-80 space-y-4"
      >
        <h2 className="text-xl font-bold text-center text-teal-400">Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          className="w-full p-2 rounded bg-gray-700 border border-gray-600"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Senha"
          value={senha}
          className="w-full p-2 rounded bg-gray-700 border border-gray-600"
          onChange={(e) => setSenha(e.target.value)}
        />

        {erro && <p className="text-red-400 text-sm">{erro}</p>}

        <button
          type="submit"
          className="w-full bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 rounded"
        >
          Entrar
        </button>
      </form>
    </div>
  );
};

export default Login;
