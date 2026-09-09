import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "../components/layout/Layout";
import { DashboardPage } from "../modules/dashboard/DashboardPage";
import { EmpresasPage } from "../modules/empresas/EmpresasPage";
import { EmpresaDetailPage } from "../modules/empresas/EmpresaDetailPage";
import { CertidoesPage } from "../modules/certidoes/CertidoesPage";
import { PendenciasPage } from "../modules/pendencias/PendenciasPage";
import { AutomacoesPage } from "../modules/automacoes/AutomacoesPage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/empresas" element={<EmpresasPage />} />
          <Route path="/empresas/:id" element={<EmpresaDetailPage />} />
          <Route path="/certidoes" element={<CertidoesPage />} />
          <Route path="/pendencias" element={<PendenciasPage />} />
          <Route path="/automacoes" element={<AutomacoesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}