import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Aziz Quick-Shop", layout="wide")

# --- CUSTOM "VISUAL" CSS ---
st.markdown("""
    <style>
    /* Big Green Buttons for "Add to Cart" */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        background-color: #2e7d32 !important;
        color: white !important;
        font-size: 20px !important;
        height: 60px;
        font-weight: bold;
    }
    /* Heart Button for Wishlist */
    .wishlist-btn {
        background: none;
        border: none;
        color: #ff1744;
        font-size: 30px;
        cursor: pointer;
    }
    /* Product Card */
    .product-box {
        border: 2px solid #f0f0f0;
        padding: 10px;
        border-radius: 20px;
        text-align: center;
        background-color: white;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .product-box img {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    h3 { color: #333; font-size: 1.5rem !important; margin: 5px 0px; }
    .price { color: #2e7d32; font-weight: 900; font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- INVENTORY (Your Shop Items) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "name": "Milk (Doodh)", "price": 30, "cat": "🥛 Milk", "img": "https://images.unsplash.com/photo-1563636619-e9108b4c196c?w=400"},
        {"name": "Bread", "price": 40, "cat": "🍞 Bakery", "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
        {"name": "Tomato (Tamatar)", "price": 20, "cat": "🍅 Vegetables", "img": "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?w=400"},
        {"name": "Parle-G", "price": 10, "cat": "🍪 Biscuits", "img": "https://m.media-amazon.com/images/I/51pSiz9O6jL.jpg"},
    ]

# --- SESSION STATE (The Brain of the App) ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'wishlist' not in st.session_state: st.session_state.wishlist = []

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>🍎 AZIZ QUICK-SHOP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>FAST DELIVERY IN SOLAPUR</p>", unsafe_allow_html=True)

# --- CATEGORY BAR (Visual Icons) ---
cats = ["🏠 All", "🍅 Vegetables", "🥛 Milk", "🍪 Biscuits", "🍞 Bakery"]
selected_cat = st.radio("", cats, horizontal=True)

st.divider()

# --- DISPLAY ITEMS ---
cols = st.columns(2) # Two items per row on mobile
for idx, item in enumerate(st.session_state.inventory):
    # Filter by category
    if selected_cat == "🏠 All" or item['cat'] in selected_cat:
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="product-box">
                    <img src="{item['img']}" width="100%">
                    <h3>{item['name']}</h3>
                    <p class="price">₹{item['price']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns([4, 1])
            with c1:
                if st.button(f"🛒 ADD TO CART", key=f"add_{idx}"):
                    st.session_state.cart.append(item)
                    st.toast(f"Added {item['name']}")
            with c2:
                if st.button("❤️", key=f"wish_{idx}"):
                    st.session_state.wishlist.append(item)
                    st.toast("Saved to Favorites")

# --- SHOPPING BASKET SIDEBAR ---
with st.sidebar:
    st.markdown("## 🛍️ Your Basket")
    if not st.session_state.cart:
        st.write("Your basket is empty. Add items!")
    else:
        total = 0
        for i, cart_item in enumerate(st.session_state.cart):
            st.write(f"✅ {cart_item['name']} - ₹{cart_item['price']}")
            total += cart_item['price']
        
        st.markdown(f"### Total Bill: ₹{total}")
        
        if st.button("❌ Empty Basket"):
            st.session_state.cart = []
            st.rerun()

    st.divider()
    
    st.markdown("## 📍 Delivery Details")
    u_name = st.text_input("Name (Naam)")
    u_addr = st.text_area("Address (Pata)")
    
    # WHATSAPP INTEGRATION
    if st.button("🚀 ORDER ON WHATSAPP"):
        if u_name and u_addr and st.session_state.cart:
            items_text = "%0A".join([f"- {i['name']}" for i in st.session_state.cart])
            message = f"Order from {u_name}!%0AItems:%0A{items_text}%0ATotal: ₹{total}%0AAddress: {u_addr}"
            # Replace with your WhatsApp number
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://wa.me/91XXXXXXXXXX?text={message}">', unsafe_allow_html=True)
        else:
            st.error("Please add items and address!")

    st.divider()
    st.markdown("### ❤️ Favorites")
    for fav in st.session_state.wishlist:
        st.write(f"⭐ {fav['name']}")
