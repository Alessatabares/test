import streamlit as st
import json
import os

st.title("🧠 Árboles de Decisión en Neurología Aguda")

# 📁 Automatically list all JSON files in the folder
json_files = [f for f in os.listdir() if f.endswith(".json")]

# 🔽 User selects one
selected_file = st.selectbox("📂 Selecciona un algoritmo para visualizar:", json_files)

# 📖 Load the file
try:
    with open(selected_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🌐 Section: Condition
    st.header(f"🩺 Condición: {data.get('condition', 'Sin título')}")

    # 📚 Section: Guidelines
    st.subheader("📚 Fuente de la guía")
    source = data.get("guideline_source", {})
    st.markdown(f"**Título:** {source.get('title', '')}")
    st.markdown(f"**Autores:** {source.get('authors', '')}")
    st.markdown(f"**Año:** {source.get('year', '')}")
    st.markdown(f"[Ver enlace original]({source.get('url', '')})")

    # 👀 Section: Presentation patterns
    st.subheader("👁️‍🗨️ Presentación clínica")
    patterns = data.get("presentation_patterns", {})
    typical = patterns.get("typical", {})
    atypical = patterns.get("atypical", {})

    st.markdown("### 🔹 Típica")
    st.markdown(f"- **Descripción:** {typical.get('description', '')}")
    st.markdown(f"- **Manejo inicial:** {typical.get('management', '')}")

    st.markdown("### 🔸 Atípica")
    st.markdown(f"- **Descripción:** {atypical.get('description', '')}")
    st.markdown(f"- **Manejo inicial:** {atypical.get('management', '')}")

    # Show key additional assessments if they exist
    extra = atypical.get("key_additional_assessments", [])
    if extra:
        st.markdown("🔍 Evaluaciones adicionales:")
        for item in extra:
            st.markdown(f"- {item}")

    # 🧪 Section: Inputs
    st.subheader("🧪 Variables clínicas evaluadas")
    for group in data.get("input_groups", []):
        st.markdown(f"#### ➤ Grupo: {group.get('group', '')}")
        for item in group.get("inputs", []):
            st.markdown(f"- **{item.get('label', '')}**")
            st.markdown(f"  ↳ {item.get('tag_explanation', '')}")
            st.markdown(f"  🔗 Valor agrupado: {item.get('cluster_value', '')}")

    # 🔬 Section: Lógica diagnóstica
    st.subheader("🔬 Lógica diagnóstica")
    logic = data.get("diagnosis_logic", {})
    for cluster in logic.get("clustered_findings", []):
        st.markdown(f"- 🔗 Cluster: {', '.join(cluster)}")
    st.markdown(f"✅ Mínimo requerido: **{logic.get('minimum_required', '?')} hallazgos**")

    # 🔄 Section: Diagnósticos diferenciales
    st.subheader("🧠 Diagnóstico diferencial")
    for ddx in data.get("differential_diagnosis", []):
        st.markdown(f"- **{ddx.get('condition')}**")
        for k in ddx.get("key_exclusion_findings", []):
            st.markdown(f"  - {k}")

    # 💊 Section: Plan terapéutico
    st.subheader("💊 Plan terapéutico")
    for key, val in data.get("plan", {}).items():
        st.markdown(f"- **{key.replace('_', ' ').capitalize()}:** {val.get('tratamiento')}")

except Exception as e:
    st.error(f"❌ Error al cargar o interpretar el archivo: {e}")
