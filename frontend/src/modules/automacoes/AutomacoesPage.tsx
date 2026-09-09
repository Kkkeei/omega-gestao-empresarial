import {useEffect,useState} from "react";
import {Bot,PlayCircle,RefreshCw,AlertTriangle} from "lucide-react";
import {listarExecucoes} from "../../services/api/automacoes";
import {consultarTodasCertidoesEstaduais} from "../../services/api/certidoes";
import {Loading} from "../../components/ui/Loading";

export function AutomacoesPage(){
  const [execucoes,setExecucoes]=useState<any[]>([]);
  const [loading,setLoading]=useState(true);
  const [rodando,setRodando]=useState(false);
  const [erro,setErro]=useState("");
  const [resultado,setResultado]=useState<any>(null);

  const load=async()=>{setLoading(true);setErro("");try{setExecucoes((await listarExecucoes()).execucoes)}catch(x){setErro(x instanceof Error?x.message:"Erro ao carregar execuções.")}finally{setLoading(false)}};
  useEffect(()=>{load()},[]);

  async function executarCertidoes(){
    setRodando(true);setErro("");setResultado(null);
    try{const r=await consultarTodasCertidoesEstaduais();setResultado(r);await load()}
    catch(x){setErro(x instanceof Error?x.message:"Não foi possível executar as certidões estaduais.")}
    finally{setRodando(false)}
  }

  return <div className="page">
    <div className="page-heading"><div><span className="eyebrow">AUTOMAÇÃO</span><h2>Automações</h2><p>Execuções reais do ÔMEGA, incluindo consultas oficiais da SEFAZ-PE.</p></div><button className="button secondary" onClick={load} disabled={loading||rodando}><RefreshCw size={15}/> Atualizar</button></div>
    {erro&&<div className="form-error"><AlertTriangle size={14}/> {erro}</div>}
    <div className="panel automation-run"><div><span className="eyebrow">SEFAZ-PE / E-FISCO</span><h3>Certidão Estadual em lote</h3><p>Executa a mesma automação real para todas as empresas ativas. Cada empresa é gravada separadamente e uma falha não interrompe o lote.</p></div><button className="button primary" onClick={executarCertidoes} disabled={rodando}>{rodando?<><RefreshCw size={15}/> Processando...</>:<><PlayCircle size={15}/> Consultar todas as empresas</>}</button></div>
    {rodando&&<Loading text="Consultando as empresas ativas na SEFAZ-PE. Aguarde a conclusão do lote..."/>}
    {!rodando&&resultado&&<div className="panel"><div className="panel-header"><div><span className="eyebrow">ÚLTIMO LOTE</span><h3>Resultado</h3></div></div><div className="details cert-result-details"><div><span>Total</span><strong>{resultado.resumo.total}</strong></div><div><span>Registradas</span><strong>{resultado.resumo.consultas_registradas}</strong></div><div><span>Regulares</span><strong>{resultado.resumo.regular}</strong></div><div><span>Irregulares</span><strong>{resultado.resumo.irregular}</strong></div><div><span>Erros</span><strong>{resultado.resumo.erro}</strong></div></div></div>}
    <div className="panel table-panel"><div className="table-meta"><span>{execucoes.length} execução(ões)</span><span>Histórico persistido no banco</span></div>{loading?<Loading text="Carregando execuções..."/>:execucoes.length===0?<div className="empty"><Bot size={36}/><strong>Nenhuma execução registrada</strong><span>As consultas realizadas aparecerão aqui.</span></div>:<div className="table-wrap"><table><thead><tr><th>Data</th><th>Empresa</th><th>Tipo</th><th>Status</th><th>Origem</th><th>Mensagem</th></tr></thead><tbody>{execucoes.map(x=><tr key={x.id}><td>{x.inicio||"—"}</td><td>{x.empresa_id?`Empresa #${x.empresa_id}`:"—"}</td><td>{x.tipo||"—"}</td><td>{x.status||"—"}</td><td>{x.origem||"—"}</td><td>{x.mensagem||"—"}</td></tr>)}</tbody></table></div>}</div>
  </div>
}
