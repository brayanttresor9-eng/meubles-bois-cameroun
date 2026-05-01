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
        "stripe_price_id": "price_1REMPLACE_MOI_25K"
    },
    {
        "nom":"Banc Bassa + Étagères Kribi",
        "prix": 65000,
        "img":"https://i.imgur.com/6jjF1R5.jpeg",
        "desc":"Banc pin massif 120cm + 5 modules muraux",
        "stripe_price_id": "price_1REMPLACE_MOI_65K"
    },
    {
        "nom":"Table Haute Wouri",
        "prix": 85000,
        "img":"https://i.imgur.com/7AJZU2c.jpeg",
        "desc":"Table bar bois massif 140x70cm + style industriel",
        "stripe_price_id": "price_1REMPLACE_MOI_85K"
    },
]

if "panier" not in st.session_state: st.session_state.panier = []

st.title("Meubles Bois CMR 🪵")
st.caption("Fabrication artisanale Douala | Livraison 48h | *Photos non contractuelles")

cols = st.columns(3)
for i, m in enumerate(MEUBLES):
    with cols[i]:
        st.image(m["img"])
        st.subheader(m["nom"])
        st.write(f"**{m['prix']:,} FCFA**")
        st.caption(m["desc"])
        if st.button(f"Ajouter au panier", key=m['nom']):
            st.session_state.panier.append(m)
            st.toast(f"{m['nom']} ajouté ✅")

st.divider()
st.subheader(f"🛒 Panier : {len(st.session_state.panier)} article(s)")

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

st.write(f"**Total : {total + livraison:,} FCFA**")

if st.button("PAYER MAINTENANT", type="primary", disabled=total==0):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        st.link_button("👉 Aller au paiement sécurisé", session.url)
    except Exception as e:
        st.error(f"Erreur: {e}. Crée tes price_id Stripe d'abord.")
