import os
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
import streamlit as st
from experta import *
from groq import Groq
from dotenv import load_dotenv

# variáveis de ambiente
load_dotenv()

#  cliente da Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Problema(Fact):
    """Fato representando um problema relatado pelo usuário"""
    descricao = Field(str, mandatory=True)

class SistemaSuporte(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultado = None 

    @Rule(Problema(descricao=MATCH.descricao))
    def diagnosticar_problema(self, descricao):
        descricao_lower = descricao.lower()

        if "internet" in descricao_lower or "sem conexão" in descricao_lower or "rede" in descricao_lower:
            self.resultado = (
                "🌐 Parece um problema de conexão com a Internet.\n"
                "💡 Verifique se o cabo de rede está bem conectado ao computador e ao roteador.\n"
                "🔁 Reinicie o roteador e o computador.\n"
                "📶 Caso use Wi-Fi, teste em outro dispositivo para ver se a rede está funcionando."
            )

        elif "computador não liga" in descricao_lower or "pc não liga" in descricao_lower or "não liga" in descricao_lower:
            self.resultado = (
                "⚡ O computador não está ligando.\n"
                "💡 Confira se o cabo de energia está conectado corretamente e se há energia no estabilizador ou nobreak.\n"
                "🔋 Teste em outra tomada. Se possível, desconecte periféricos e tente novamente.\n"
                "🧰 Caso continue sem ligar, pode ser problema na fonte ou placa-mãe."
            )

        elif "lento" in descricao_lower or "travando" in descricao_lower or "demorado" in descricao_lower:
            self.resultado = (
                "🐢 O sistema está lento.\n"
                "💡 Abra o Gerenciador de Tarefas (Ctrl + Shift + Esc) e verifique o uso de CPU, RAM e Disco.\n"
                "🧹 Feche programas que não estão em uso e desinstale aplicativos desnecessários.\n"
                "⚙️ Execute uma verificação de vírus e limpe arquivos temporários."
            )

        elif "impressora" in descricao_lower or "imprimir" in descricao_lower:
            self.resultado = (
                "🖨️ Problema com a impressora detectado.\n"
                "💡 Verifique se a impressora está ligada, conectada ao computador (USB/Wi-Fi) e com papel.\n"
                "📄 Veja se há documentos presos na fila de impressão.\n"
                "🔁 Se necessário, reinstale o driver ou reinicie a impressora."
            )

        elif "wifi" in descricao_lower or "wi-fi" in descricao_lower:
            self.resultado = (
                "📶 Problema de conexão Wi-Fi.\n"
                "💡 Desconecte e reconecte à rede. Reinicie o roteador.\n"
                "📱 Teste em outro dispositivo para confirmar se a rede está funcionando.\n"
                "🔧 Se apenas o seu computador não conecta, atualize os drivers de rede."
            )

        elif "tela preta" in descricao_lower or "sem imagem" in descricao_lower or "monitor" in descricao_lower:
            self.resultado = (
                "🖥️ Tela sem imagem detectada.\n"
                "💡 Verifique se o cabo de vídeo (HDMI, VGA, DisplayPort) está firme nas conexões.\n"
                "⚡ Veja se o monitor está ligado e configurado na entrada correta.\n"
                "🧰 Caso o PC ligue mas sem vídeo, pode haver problema na memória RAM ou placa de vídeo."
            )

        elif "erro" in descricao_lower or "aplicativo" in descricao_lower or "programa" in descricao_lower or "software" in descricao_lower:
            self.resultado = (
                "💻 Erro de software detectado.\n"
                "💡 Tente reiniciar o aplicativo e o computador.\n"
                "🔄 Verifique se há atualizações pendentes do programa.\n"
                "🧩 Se o problema persistir, reinstale o software ou execute como administrador."
            )

        elif "som" in descricao_lower or "áudio" in descricao_lower or "audio" in descricao_lower:
            self.resultado = (
                "🔊 Problema de som identificado.\n"
                "💡 Verifique se o volume não está no mudo e se as saídas de áudio estão corretas (caixas de som, fones, HDMI, etc).\n"
                "🎧 Confira se os cabos estão conectados e atualize os drivers de áudio.\n"
                "🧰 No Gerenciador de Dispositivos, veja se há erros no dispositivo de som."
            )

        elif "mouse" in descricao_lower or "teclado" in descricao_lower or "periférico" in descricao_lower:
            self.resultado = (
                "🖱️ Problema com periféricos detectado.\n"
                "💡 Desconecte e reconecte o mouse/teclado. Tente em outra porta USB.\n"
                "🔋 Se for sem fio, troque as pilhas ou recarregue o dispositivo.\n"
                "🧩 Teste em outro computador para descartar falha de hardware."
            )

        elif "tela azul" in descricao_lower or "blue screen" in descricao_lower or "bsod" in descricao_lower:
            self.resultado = (
                "💀 Tela azul detectada.\n"
                "💡 Isso geralmente indica falha de driver, memória RAM ou disco.\n"
                "🧰 Atualize todos os drivers, execute o 'Verificador de Memória do Windows' e verifique o disco com 'chkdsk /f'."
            )

        elif "hd" in descricao_lower or "disco" in descricao_lower or "armazenamento" in descricao_lower:
            self.resultado = (
                "💾 Problema de disco identificado.\n"
                "💡 Verifique se o HD/SSD aparece no BIOS.\n"
                "🧰 Execute o comando 'chkdsk /f' para procurar erros e faça backup dos dados.\n"
                "⚠️ Se houver ruídos no HD, substitua o disco o quanto antes."
            )

        elif "driver" in descricao_lower or "dispositivo" in descricao_lower:
            self.resultado = (
                "🧩 Problema de driver detectado.\n"
                "💡 Abra o Gerenciador de Dispositivos e veja se há algum ícone de alerta.\n"
                "🔄 Reinstale ou atualize o driver manualmente.\n"
                "💽 Se for de vídeo, áudio ou rede, baixe o driver mais recente no site do fabricante."
            )

        else:
            self.resultado = None  # Chama a API da Groq se não houver correspondência


# ----- Função de consulta à Groq -----
def consultar_groq(descricao):
    try:
        resposta = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": f"Um usuário relatou: {descricao}. Analise o caso e sugira uma possível causa e solução técnica."
                }
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False  # evita erro de streaming
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erro ao consultar a IA: {e}"


# ----- Interface com Streamlit -----
st.set_page_config(page_title="Assistente de Suporte Técnico", page_icon="💻", layout="centered")

st.title("💻 Bem-vindo ao Assistente de Suporte Técnico!")
st.write("Descreva o problema técnico e receba uma sugestão de diagnóstico.")

# Campo de entrada
descricao = st.text_area("Digite o problema aqui:", placeholder="Ex: Meu computador não liga...")

# Botão Diagnosticar
if st.button("Diagnosticar"):
    if descricao.strip() == "":
        st.warning("⚠️ Por favor, descreva o problema antes de diagnosticar.")
    else:
        # Executa o motor de regras
        engine = SistemaSuporte()
        engine.reset()
        engine.declare(Problema(descricao=descricao))
        engine.run()

        # Se o sistema não encontrou regra, chama a IA
        if engine.resultado:
            st.success(engine.resultado)
        else:
            with st.spinner("Consultando IA da Groq..."):
                resposta_ia = consultar_groq(descricao)
            st.info(resposta_ia)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Jandir C. Basegio e João Pedro Soares • Sistema Especialista com Experta (PyKnow) + Streamlit + API Groq")