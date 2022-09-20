import axios from "axios";

const api = axios.create({
  // baseURL: "https://api.github.com"
  baseURL: "http://api-test.bhut.com.br:3000"
});
export default api;
