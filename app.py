import os
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
import streamlit as st
from experta import *
from groq import Groq
from dotenv import load_dotenv
import re

# Variáveis de ambiente
load_dotenv()

# Cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


#  Regras

REGRAS = [
    (
        r"internet|sem conexão|rede|sem internet",
        " Problema de conexão com a Internet.\n"
        "- Verifique cabos e reinicie o roteador.\n"
        "- Teste a conexão em outro dispositivo.\n"
        "- Confira se as luzes do roteador estão verdes."
    ),
    (
        r"computador não liga|pc não liga|não liga|pc não inicia|computador não funciona",
        " Seu computador não está ligando.\n"
        "- Verifique cabo de energia e tomada.\n"
        "- Teste outra tomada.\n"
        "- Pode ser fonte ou placa-mãe.\n"
        "- Se souber, faça teste de fonte com jumper."
    ),
    (
        r"lento|travando|demorado|demorando|travado",
        " Sistema lento detectado.\n"
        "- Abra o Gerenciador de Tarefas.\n"
        "- Verifique uso de CPU/RAM/Disco.\n"
        "- Feche programas desnecessários.\n"
        "- Execute verificação de vírus."
    ),
    (
        r"impressora|imprimir|não imprime|impressão",
        " Problema com a impressora.\n"
        "- Veja se está ligada e com papel.\n"
        "- Verifique fila de impressão.\n"
        "- Reinicie impressora e spooler."
    ),
    (
        r"wifi|wi-fi| Wifi não conecta| sem sinal Wifi",
        "  Problema com Wi-Fi.\n"
        "- Verifique se a senha está correta\n"
        "- Reconecte à rede.\n"
        "- Reinicie o roteador.\n"
        "- Atualize drivers de rede."
    ),
    (
        r"tela preta|sem imagem|monitor",
        "- Tela sem imagem.\n"
        "- Cheque o cabo HDMI/VGA.\n"
        "- Veja se o monitor está na entrada correta.\n"
        "- Pode ser memória RAM ou placa de vídeo."
    ),
    (
        r"erro|aplicativo|programa|software",
        "- Erro de software.\n"
        "- Reinicie o app.\n"
        "- Atualize ou reinstale o programa."
    ),
    (
        r"som|áudio|audio",
        "- Problema de áudio.\n"
        "- Verifique se não está no mudo.\n"
        "- Teste outras saídas.\n"
        "- Atualize drivers de áudio."
    ),
    (
        r"mouse|teclado|periférico",
        "- Problema em periféricos.\n"
        "- Troque porta USB.\n"
        "- Teste em outro PC.\n"
        "- Troque pilhas no caso de sem fio."
    ),
    (
        r"tela azul|blue screen|bsod",
        "- Tela azul detectada.\n"
        "- Atualize drivers.\n"
        "- Teste memória.\n"
        "- Execute CHKDSK."
    ),
    (
        r"hd|disco|armazenamento",
        "- Problema no disco.\n"
        "- Execute CHKDSK.\n"
        "- Veja se aparece no BIOS.\n"
        "- Faça backup urgente."
    ),
    (
        r"driver|dispositivo",
        "- Problema de driver.\n"
        "- Verifique gerenciador de dispositivos.\n"
        "- Reinstale ou atualize driver."
    ),
]


#  Uso das regras
class Problema(Fact):
    descricao = Field(str, mandatory=True)

class SistemaSuporte(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultado = None

    @Rule(Problema(descricao=MATCH.descricao))
    def diagnosticar(self, descricao):

        desc = descricao.lower()

        # Procura em regras simplificadas
        for padrao, resposta in REGRAS:
            if re.search(padrao, desc):
                self.resultado = resposta
                return

        # Se nada encontrado -> IA
        self.resultado = None

# CONSULTA API GROQ
def consultar_groq(descricao):
    try:
        resposta = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": f"Usuário relatou: {descricao}. Diagnostique e dê solução."}],
            temperature=1,
            max_completion_tokens=2048
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erro ao consultar IA: {e}"



# STREAMLIT
st.set_page_config(page_title="Assistente Técnico", page_icon="💻")

st.title("💻 Assistente de Suporte Técnico")
st.write("Descreva o problema e receba um diagnóstico.")

# chama a sessão do histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

descricao = st.text_area("Digite o problema:", placeholder="Ex: Meu computador não liga...")

if st.button("Diagnosticar"):
    if descricao.strip() == "":
        st.warning("⚠️ Digite um problema.")
    else:
        engine = SistemaSuporte()
        engine.reset()
        engine.declare(Problema(descricao=descricao))
        engine.run()

        if engine.resultado:
            resposta = engine.resultado
            st.success(resposta)
        else:
            with st.spinner("Consultando IA da Groq..."):
                resposta = consultar_groq(descricao)
            st.info(resposta)

        # Salvar no histórico
        st.session_state.historico.append(("🧑 Usuário", descricao))
        st.session_state.historico.append(("🤖 Assistente", resposta))


# mostrar histórico
st.markdown("---")
st.subheader("📜 Histórico do Chat")

for autor, texto in st.session_state.historico:
    st.markdown(f"**{autor}:**<br>{texto}<br><br>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Desenvolvido por Jandir C. Basegio e João Pedro Soares • Sistema Especialista + Streamlit + Groq")
