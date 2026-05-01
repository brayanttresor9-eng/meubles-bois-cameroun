import streamlit as st
import stripe

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

st.set_page_config(page_title="Meubles Bois CMR", page_icon="🪵", layout="wide")

MEUBLES = [
    {
        "nom":"Tabouret Haut Douala",
        "prix": 25000,
        "img":"https://i.imgur.com/ducfiUU.jpeg",
        "desc":"Tabouret bar bois massif H75cm. Assise galbée.",
        "stripe_price_id": "price_1TS5EvDmScq27Uw6UJMqZJOR"
    },
    {
        "nom":"Banc Bassa + Étagères Kribi",
        "prix": 45000,
        "img":"https://i.imgur.com/6jjF1R5.jpeg",
        "desc":"Banc pin massif 120cm + 5 modules muraux",
        "stripe_price_id": "price_1TS5I3DmScq27Uw6uF2hgRd7"
    },
    {
        "nom":"Table Haute Wouri",
        "prix": 65000,
        "img":"https://i.imgur.com/7AJZU2c.jpeg",
        "desc":"Table bar bois massif 140x70cm + style industriel",
        "stripe_price_id": "price_1TS5KGDmScq27Uw6pmLmDU2T" # NOUVEAU PRICE PONCTUEL
    },
]

if "panier" not in st.session_state:
    st.session_state.panier = []

st.title("Meubles Bois CMR 🪵")
st.caption("Fabrication artisanale Douala | Livraison 48h | Paiement sécurisé Stripe")

cols = st.columns(3)
for i, m in enumerate(MEUBLES):
    with cols[i]:
        st.image(m["img"], use_container_width=True)
        st.subheader(m["nom"])
        st.write(f"**{m['prix']:,} FCFA**")
        st.caption(m["desc"])
        if st.button(f"Ajouter au panier", key=f"add_{i}"):
            if m not in st.session_state.panier:
                st.session_state.panier.append(m)
                st.toast(f"{m['nom']} ajouté ✅")
                st.rerun()
            else:
                st.toast("Déjà dans le panier!")

st.divider()
col1, col2 = st.columns([3,1])
with col1:
    st.subheader(f"🛒 Panier : {len(st.session_state.panier)} article(s)")
with col2:
    if st.button("Vider le panier", disabled=len(st.session_state.panier)==0, key="clear"):
        st.session_state.panier = []
        st.rerun()

line_items = []
total = 0
for item in st.session_state.panier:
    st.write(f"- {item['nom']} : {item['prix']:,} FCFA")
    total += item['prix']
    line_items.append({"price": item["stripe_price_id"], "quantity": 1})

livraison = 5000 if total > 0 else 0
if livraison > 0:
    line_items.append({
        "price_data": {"currency": "xaf", "product_data": {"name": "Livraison Douala"}, "unit_amount": 500000},
        "quantity": 1,
    })

st.write(f"**Sous-total : {total:,} FCFA**")
st.write(f"**Livraison : {livraison:,} FCFA**")
st.write(f"### Total : {total + livraison:,} FCFA")

if st.button("PAYER MAINTENANT", type="primary", disabled=total==0, key="pay"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://meubles-bois-cameroun-gfxtrfzsmamnnjk2xzabk.streamlit.app?success=true',
            cancel_url='https://meubles-bois-cameroun-gfxtrfzsmamnnjk2xzabk.streamlit.app',
        )
        st.link_button("👉 Aller au paiement sécurisé", session.url)
    except Exception as e:
        st.error(f"Erreur Stripe: {e}")

if st.query_params.get("success"):
    st.balloons()
    st.success("Paiement réussi! On te contacte sous 24h pour la livraison 🍀")
    st.session_state.panier = []
