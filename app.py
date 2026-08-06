import streamlit as st
import requests

# -----------------------------------------------------------------------------
# 1. ตั้งค่าหน้าเว็บ
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AppRental - ให้เช่าระบบเว็บแอปองค์กร",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔗 นำ URL ที่ได้จาก Google Apps Script มาวางตรงนี้
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxAmkZZQvY-Y2mK8LVvYH7TFQI0RJnNbWI880zJVkJgGCKifD0bnYaAGdjIOK-BFvi5/exec"

# -----------------------------------------------------------------------------
# 2. ตกแต่งความสวยงามด้วย Custom CSS
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* ซ่อน Header และ Menu ส่วนเกินของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* สไตล์สำหรับกล่องเน้นข้อความ (Hero Banner) */
    .hero-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 40px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    /* สไตล์ปุ่มกดสุ่ม/ส่งข้อมูล */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #FF4B4B, #FF7B54);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }

    /* แต่งกล่องฟอร์มกรอกข้อมูล */
    [data-testid="stForm"] {
        border-radius: 20px;
        padding: 30px;
        background-color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. ส่วนหัวเว็บ (Hero Section)
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="hero-container">
        <h1 style="color: #FFFFFF; font-size: 2.5rem; margin-bottom: 10px;">🚀 AppRental</h1>
        <p style="color: #94A3B8; font-size: 1.2rem; margin-bottom: 0px;">
            เช่าระบบเว็บแอปพร้อมใช้งาน ยกระดับธุรกิจของคุณง่ายๆ เริ่มต้นหลักร้อย/เดือน
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. แสดงรายละเอียดบริการด้วย Tabs & Cards
# -----------------------------------------------------------------------------
st.subheader("💡 ระบบแอปสำเร็จรูปที่เราให้บริการ")

tab1, tab2 = st.tabs(["🛒 1. ระบบจัดการหน้าร้าน (POS)", "🏢 2. ระบบบริหารจัดการหอพัก"])

with tab1:
    with st.container(border=True):
        col_info, col_price = st.columns([2, 1])
        with col_info:
            st.markdown("### 🛒 ระบบขายของหน้าร้าน & เช็คสต็อก (POS)")
            st.write("• บันทึกยอดขายประจำวัน ตัดสต็อกสินค้าอัจฉริยะ")
            st.write("• ออกใบเสร็จรับเงิน และสรุปรายงานยอดขาย Daily/Monthly")
            st.write("• ดึงข้อมูลเข้า Google Sheets หรือ Excel ได้ตลอดเวลา")
        with col_price:
            st.metric(label="ค่าบริการรายเดือน", value="299 บาท", delta="ทดลองใช้ฟรี 14 วัน")
            st.caption("✅ รวมบริการดูแลเซิร์ฟเวอร์และอัปเดตฟรี")

with tab2:
    with st.container(border=True):
        col_info, col_price = st.columns([2, 1])
        with col_info:
            st.markdown("### 🏢 ระบบจัดการหอพัก & อพาร์ทเม้นท์")
            st.write("• คำนวณค่าน้ำ-ค่าไฟ และออกใบแจ้งหนี้อัตโนมัติ")
            st.write("• ระบบรับแจ้งซ่อมออนไลน์สำหรับผู้เช่า")
            st.write("• แจ้งเตือนยอดชำระเงินตรงเข้า LINE ผู้เช่า")
        with col_price:
            st.metric(label="ค่าบริการรายเดือน", value="499 บาท", delta="ทดลองใช้ฟรี 14 วัน")
            st.caption("✅ รวมบริการดูแลเซิร์ฟเวอร์และอัปเดตฟรี")

st.divider()

# -----------------------------------------------------------------------------
# 5. จุดเด่นบริการ (Features Grid)
# -----------------------------------------------------------------------------
st.subheader("⚡ ทำไมถึงต้องเลือกเช่าระบบกับเรา?")
col_a, col_b, col_c = st.columns(3)

with col_a:
    with st.container(border=True):
        st.markdown("#### ⚡ พร้อมใช้ใน 5 นาที")
        st.write("ไม่ต้องเสียเวลาและค่าใช้จ่ายเขียนโปรแกรมหลักแสน สมัครแล้วเข้าใช้ได้ทันที")

with col_b:
    with st.container(border=True):
        st.markdown("#### 🛠️ ดูแลระบบให้ฟรี")
        st.write("หมดห่วงเรื่องเซิร์ฟเวอร์ล่ม มีทีมงานสำรองข้อมูลและอัปเดตความปลอดภัย 24 ชม.")

with col_c:
    with st.container(border=True):
        st.markdown("#### 📱 รองรับทุกอุปกรณ์")
        st.write("เปิดใช้งานผ่านมือถือ แท็บเล็ต หรือคอมพิวเตอร์ได้ทันทีโดยไม่ต้องลงแอปเพิ่ม")

st.divider()

# -----------------------------------------------------------------------------
# 6. ฟอร์มลงชื่อรับสิทธิ์ใช้งานฟรี (Lead Form)
# -----------------------------------------------------------------------------
st.subheader("📩 ลงชื่อขอรับสิทธิ์ทดลองใช้งานฟรี 14 วัน")
st.write("กรอกข้อมูลสั้นๆ ด้านล่าง ทีมงานจะติดต่อกลับเพื่อตั้งค่าระบบให้ทันที")

with st.form("lead_form"):
    name = st.text_input("ชื่อ-นามสกุล หรือ ชื่อร้านค้า / หอพัก", placeholder="เช่น คุณสมชาย (ร้านขายดี)")
    email = st.text_input("เบอร์โทรศัพท์ / LINE ID / อีเมล", placeholder="เช่น 081-234-5678 หรือ Line ID")
    selected_app = st.selectbox(
        "สนใจทดลองใช้งานระบบใดมากที่สุด",
        ["ระบบขายของ (POS)", "ระบบจัดการหอพัก", "สนใจทั้ง 2 ระบบ / ต้องการให้พัฒนาเพิ่ม"]
    )
    note = st.text_area("ข้อความถึงทีมงาน / คำถามเพิ่มเติม (ถ้ามี)", placeholder="เช่น อยากได้ระบบสแกนบาร์โค้ดเพิ่มด้วย...")
    
    submit = st.form_submit_button("🚀 ยืนยันขอรับสิทธิ์ใช้งานฟรี")

    if submit:
        if name and email:
            payload = {
                "name": name,
                "email": email,
                "selected_app": selected_app,
                "note": note
            }
            try:
                # ส่งข้อมูลไปที่ Google Apps Script
                response = requests.post(WEBHOOK_URL, json=payload)
                st.balloons()
                st.success(f"🎉 ขอบคุณครับคุณ {name}! บันทึกข้อมูลเรียบร้อยแล้ว ทีมงานจะติดต่อกลับโดยเร็วที่สุดครับ")
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการส่งข้อมูล กรุณาตรวจสอบอินเทอร์เน็ตหรือลองใหม่อีกครั้ง")
        else:
            st.warning("⚠️ กรุณากรอกชื่อและช่องทางการติดต่อให้ครบถ้วนนะครับ")
