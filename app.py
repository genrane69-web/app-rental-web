import streamlit as st
import requests

# 🔗 วาง URL ที่ได้จาก Google Apps Script ตรงนี้
WEBHOOK_URL = "นำ_URL_จาก_APPS_SCRIPT_มาวางตรงนี้"

st.set_page_config(page_title="AppRental - ให้เช่าระบบเว็บแอป", page_icon="🚀", layout="wide")

st.title("🚀 AppRental - เช่าระบบแอปองค์กร เริ่มต้นเพียงหลักร้อย/เดือน")
st.write("พร้อมใช้งานทันที ดูแลระบบให้ 24 ชม. ปรับแต่งตามแบรนด์ของคุณได้")

st.divider()

st.header("💡 บริการระบบแอปของเรา")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🛒 1. ระบบจัดการหน้าร้าน & ขายของ (POS)")
    st.write("• บันทึกยอดขาย เช็คสต็อกสินค้าอัจฉริยะ")
    st.caption("💰 ค่าบริการเริ่มต้น: 299 บาท / เดือน")
with col2:
    st.markdown("### 🏢 2. ระบบบริหารจัดการหอพัก & อพาร์ทเม้นท์")
    st.write("• ออกใบแจ้งหนี้ ค่าน้ำ-ค่าไฟ อัตโนมัติ")
    st.caption("💰 ค่าบริการเริ่มต้น: 499 บาท / เดือน")

st.divider()

st.header("📩 ลงชื่อรับสิทธิ์ทดลองใช้งานฟรี 14 วัน!")

with st.form("lead_form"):
    name = st.text_input("ชื่อ-นามสกุล หรือ ชื่อร้านค้า")
    email = st.text_input("อีเมล / เบอร์โทรศัพท์")
    selected_app = st.selectbox(
        "ระบบที่คุณสนใจมากที่สุด",
        ["ระบบขายของ (POS)", "ระบบจัดการหอพัก", "ระบบอื่นๆ"]
    )
    note = st.text_area("รายละเอียดเพิ่มเติม / สอบถามเพิ่มเติม")
    
    submit = st.form_submit_button("ส่งข้อมูลขอรับสิทธิ์ใช้งานฟรี 🚀", type="primary")

    if submit:
        if name and email:
            # ส่งข้อมูลไปเก็บใน Google Sheets
            payload = {
                "name": name,
                "email": email,
                "selected_app": selected_app,
                "note": note
            }
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                st.success(f"ขอบคุณครับคุณ {name}! บันทึกข้อมูลเรียบร้อยแล้ว ทีมงานจะติดต่อกลับโดยเร็วที่สุดครับ")
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการส่งข้อมูล กรุณาลองใหม่อีกครั้ง")
        else:
            st.warning("กรุณากรอกชื่อและช่องทางการติดต่อให้ครบถ้วนนะครับ")
