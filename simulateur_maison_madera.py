import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulateur Concerts - Maison Madera", page_icon="🎤", layout="wide")

# ==================== STYLING ====================
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .section-header {background-color: #1F4E79; color: white; padding: 10px; border-radius: 8px; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.title("🎤 Simulateur Concerts Privés - Maison Madera")
st.caption("Outil de simulation et d'aide à la négociation | Version Prototype Web")

# ==================== SECTION 1: INFORMATIONS ====================
st.markdown("### 1. Informations sur l'événement")

col1, col2, col3 = st.columns(3)
with col1:
    artiste = st.text_input("Artiste / DJ", value="Daraa J")
with col2:
    date_event = st.text_input("Date de l'événement", value="15/07/2026")
with col3:
    restaurant = st.text_input("Restaurant", value="Maison Madera")

# ==================== SECTION 2: CATÉGORIES DE BILLETS ====================
st.markdown("### 2. Catégories de Billets / Packages")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Entrée Simple")
    nb_simple = st.number_input("Nombre de billets", min_value=0, value=80, step=5, key="nb_simple")
    prix_simple = st.number_input("Prix unitaire (FCFA)", min_value=0, value=15000, step=1000, key="prix_simple")

with col2:
    st.subheader("Dîner + Concert")
    nb_standard = st.number_input("Nombre de billets", min_value=0, value=170, step=5, key="nb_standard")
    prix_standard = st.number_input("Prix unitaire (FCFA)", min_value=0, value=25000, step=1000, key="prix_standard")

with col3:
    st.subheader("Dîner + Concert VIP")
    nb_vip = st.number_input("Nombre de billets", min_value=0, value=50, step=5, key="nb_vip")
    prix_vip = st.number_input("Prix unitaire (FCFA)", min_value=0, value=39340, step=1000, key="prix_vip")

# Calculs
ca_simple = nb_simple * prix_simple
ca_standard = nb_standard * prix_standard
ca_vip = nb_vip * prix_vip
ca_total = ca_simple + ca_standard + ca_vip
total_participants = nb_simple + nb_standard + nb_vip

# ==================== SECTION 3: COÛTS ====================
st.markdown("### 3. Coûts de l'Événement")

col1, col2 = st.columns(2)

with col1:
    cachet = st.number_input("Cachet Artiste (FCFA)", min_value=0, value=2500000, step=50000, key="cachet")
    food = st.number_input("Food & Drink (FCFA)", min_value=0, value=1000000, step=50000, key="food")
    sono = st.number_input("Sono & Technique (FCFA)", min_value=0, value=900000, step=50000, key="sono")

with col2:
    chaises = st.number_input("Chaises / Mobilier (FCFA)", min_value=0, value=300000, step=10000, key="chaises")
    hotesses = st.number_input("Hôtesses (FCFA)", min_value=0, value=100000, step=10000, key="hotesses")
    serveurs = st.number_input("Serveurs extra (FCFA)", min_value=0, value=60000, step=5000, key="serveurs")
    bracelets = st.number_input("Bracelets & Contrôle (FCFA)", min_value=0, value=120000, step=10000, key="bracelets")

cout_total = cachet + food + sono + chaises + hotesses + serveurs + bracelets
cout_fixe = cachet + sono + chaises + hotesses + serveurs
cout_variable = food + bracelets

# ==================== RÉSULTATS ====================
st.markdown("### 4. Résultats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Chiffre d'Affaires", f"{ca_total:,.0f} FCFA")
with col2:
    st.metric("Coûts Totaux", f"{cout_total:,.0f} FCFA")
with col3:
    marge_brute = ca_total - cout_total
    st.metric("Marge Brute", f"{marge_brute:,.0f} FCFA")
with col4:
    taux_commission = 0.30
    commission = round(marge_brute * taux_commission)
    benefice = marge_brute - commission
    st.metric("Bénéfice Net", f"{benefice:,.0f} FCFA", delta=f"{benefice/ca_total*100:.1f}% du CA")

# ==================== SCÉNARIOS ====================
st.markdown("### 5. Analyse de Scénarios Comparatifs")

col1, col2, col3 = st.columns(3)

variation_conserv = st.slider("Variation Conservateur", 0.5, 1.0, 0.75, 0.05, key="var_cons")
variation_base = 1.0
variation_opti = st.slider("Variation Optimiste", 1.0, 1.5, 1.20, 0.05, key="var_opti")

def calcul_scenario(variation):
    ca_sc = ca_total * variation
    var_cost_sc = cout_variable * variation
    fixed_cost_sc = cout_fixe
    total_cost_sc = fixed_cost_sc + var_cost_sc
    marge_sc = ca_sc - total_cost_sc
    comm_sc = round(marge_sc * taux_commission)
    benef_sc = marge_sc - comm_sc
    return ca_sc, total_cost_sc, marge_sc, comm_sc, benef_sc

ca_c, cost_c, marge_c, comm_c, benef_c = calcul_scenario(variation_conserv)
ca_b, cost_b, marge_b, comm_b, benef_b = calcul_scenario(variation_base)
ca_o, cost_o, marge_o, comm_o, benef_o = calcul_scenario(variation_opti)

scenario_data = {
    "Indicateur": ["Participants", "CA (FCFA)", "Coûts Totaux", "Marge Brute", "Commission", "Bénéfice Net"],
    "Conservateur": [int(total_participants * variation_conserv), f"{ca_c:,.0f}", f"{cost_c:,.0f}", f"{marge_c:,.0f}", f"{comm_c:,.0f}", f"{benef_c:,.0f}"],
    "Base": [total_participants, f"{ca_b:,.0f}", f"{cost_b:,.0f}", f"{marge_b:,.0f}", f"{comm_b:,.0f}", f"{benef_b:,.0f}"],
    "Optimiste": [int(total_participants * variation_opti), f"{ca_o:,.0f}", f"{cost_o:,.0f}", f"{marge_o:,.0f}", f"{comm_o:,.0f}", f"{benef_o:,.0f}"]
}

df_scenario = pd.DataFrame(scenario_data)
st.dataframe(df_scenario, use_container_width=True, hide_index=True)

# ==================== NÉGOCIATION ====================
st.markdown("### 6. Outil d'Aide à la Négociation")

objectif = st.number_input("Objectif de Bénéfice Net souhaité (FCFA)", min_value=0, value=1500000, step=100000)

if benefice >= objectif:
    st.success(f"✅ Objectif atteint ! Vous pouvez négocier une réduction du cachet jusqu'à environ {max(0, cachet - (ca_total - (objectif / 0.7) - cout_fixe)):,.0f} FCFA.")
else:
    st.warning(f"⚠️ Pour atteindre {objectif:,.0f} FCFA de bénéfice, il faudrait réduire le cachet ou augmenter le CA.")

st.caption("Prototype Web - Basé sur le simulateur Excel développé pour Maison Madera")