import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Page Config with Zephyr Theme styling
st.set_page_config(page_title="BioNexus AI: Bioinformatics Hub", layout="wide")

# Custom CSS for Full Uniform Zephyr Background & Containers
st.markdown("""
    <style>
    /* Main app and content containers background */
    .stApp, section[data-testid="stMain"], .block-container {
        background-color: #eef8fb !important;
        color: #1d3557;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #d7ecf3 !important;
    }
    /* Metric Card styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #bde0fe;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 119, 182, 0.08);
    }
    div[data-testid="stMetric"] label {
        color: #457b9d !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0077b6 !important;
    }
    /* Headers */
    h1, h2, h3 {
        color: #03045e !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 BioNexus AI")
st.markdown("### Multi-Omics Species, Gene & Microbe Relationship Explorer")

# Sidebar for Biological Filters
st.sidebar.header("Biological Parameters")
interaction_domain = st.sidebar.selectbox("Select Domain Focus", ["All", "Host-Microbiome", "Gene-Species", "Symbiotic Co-occurrence"])
confidence_threshold = st.sidebar.slider("Minimum Interaction Confidence", 0.5, 0.95, 0.75)

# Pure Biological Dataset (Genetics, Taxonomy, & Microbes)
@st.cache_data
def load_bio_database():
    return pd.DataFrame({
        'Source_Node': ['Homo sapiens', 'Mus musculus', 'TP53', 'BRCA1', 'Gut Microbiome A', 'Arabidopsis thaliana', 'Rhizobium leguminosarum'],
        'Target_Node': ['Gut Microbiome A', 'Gut Microbiome B', 'Transcription Factor X', 'DNA Repair Complex', 'Short-Chain Fatty Acid Pathway', 'Nitrogenase Gene nifH', 'Legume Root Cortex'],
        'Domain': ['Host-Microbiome', 'Host-Microbiome', 'Gene-Species', 'Gene-Species', 'Symbiotic Co-occurrence', 'Gene-Species', 'Symbiotic Co-occurrence'],
        'Interaction_Type': ['Metabolic Symbiosis', 'Commensalism', 'Gene Regulation', 'Structural Association', 'Cross-Feeding', 'Genomic Integration', 'Endosymbiosis'],
        'Confidence_Score': [0.92, 0.88, 0.95, 0.91, 0.84, 0.89, 0.96]
    })

df = load_bio_database()

# Filter dataset
filtered_df = df[df['Confidence_Score'] >= confidence_threshold]
if interaction_domain != "All":
    filtered_df = filtered_df[filtered_df['Domain'] == interaction_domain]

# Main Dashboard Layout (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Active Biological Nodes", len(set(filtered_df['Source_Node']).union(set(filtered_df['Target_Node']))))
col2.metric("Mapped Interactions", len(filtered_df))
col3.metric("Avg. Confidence Score", f"{filtered_df['Confidence_Score'].mean()*100:.1f}%" if not filtered_df.empty else "0%")

st.markdown("---")

# Data Table Display
st.subheader("📊 Biological Interaction Dataset")
st.dataframe(filtered_df, use_container_width=True)

# Network Visualization with Zephyr Theme Plot
st.subheader("🕸️ Genomic & Microbial Interaction Graph")
if filtered_df.empty:
    st.warning("No interactions match the selected confidence threshold. Try lowering it in the sidebar.")
else:
    # Set matching zephyr background for Matplotlib plot
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#eef8fb')
    ax.set_facecolor('#eef8fb')
    
    # Build NetworkX graph
    G = nx.from_pandas_edgelist(filtered_df, 'Source_Node', 'Target_Node', edge_attr=['Interaction_Type', 'Confidence_Score'])

    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color='#90e0ef', 
        node_size=3500, 
        ax=ax, 
        font_size=8, 
        font_weight='bold', 
        font_color='#03045e',
        edge_color='#0077b6'
    )
    edge_labels = {(row['Source_Node'], row['Target_Node']): row['Interaction_Type'] for _, row in filtered_df.iterrows()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='#0077b6')

    st.pyplot(fig)
