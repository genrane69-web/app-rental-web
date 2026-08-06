import streamlit as st
import requests

# -----------------------------------------------------------------------------
# 1. ตั้งค่าหน้าเว็บ
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AppRental - ระบบเว็บแอปสำหรับธุรกิจ",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔗 วาง URL ที่ได้จาก Google Apps Script ตรงนี้
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxAmkZZQvY-Y2mK8LVvYH7TFQI0RJnNbWI880zJVkJgGCKifD0bnYaAGdjIOK-BFvi5/exec"

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (Stripe / Linear / Apple Design System)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
        /* บังคับสีข้อความหัวข้อทั้งหมดให้เป็นสีดำเข้ม */
    h1, h2, h3, [data-testid="stHeadingWithTitleContent"] {
        color: #0F172A !important;
    }
            /* 1. บังคับสีตัวหนังสือหัวข้อคำถาม FAQ (st.expander) ให้เป็นสีเข้ม */
    [data-testid="stExpander"] summary * {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    /* 2. บังคับสีข้อความภายในกล่องคำตอบ FAQ เวลาเปิดอ่าน */
    [data-testid="stExpander"] div {
        color: #334155 !important;
    }

    /* 3. บังคับสีตัวหนังสือป้ายชื่อช่องกรอกข้อมูลในฟอร์ม (Form Labels) ให้ชัดเจน */
    [data-testid="stWidgetLabel"] p, label {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* ซ่อน Header และ Elements ดั้งเดิมของ Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC;
        padding-top: 0rem;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px;
    }

    /* Navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        margin-bottom: 24px;
        position: sticky;
        top: 10px;
        z-index: 999;
    }
    .navbar-brand {
        font-weight: 800;
        font-size: 1.25rem;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    .navbar-menu {
        display: flex;
        gap: 24px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #475569;
    }
    .navbar-menu a {
        color: #475569;
        text-decoration: none;
        transition: color 0.2s;
    }
    .navbar-menu a:hover {
        color: #2563EB;
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border-radius: 28px;
        padding: 60px 40px;
        color: white;
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
        position: relative;
        overflow: hidden;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.15;
        margin-bottom: 16px;
        background: linear-gradient(180deg, #FFFFFF 0%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        max-width: 650px;
        margin: 0 auto 32px auto;
        line-height: 1.6;
    }

    /* Stats Section */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,.05);
    }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2563EB;
        margin-bottom: 4px;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Social Proof Logos */
    .logo-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 40px;
        opacity: 0.6;
        filter: grayscale(100%);
        margin: 24px 0 40px 0;
        font-weight: 700;
        font-size: 1.1rem;
        color: #475569;
    }

    /* Dashboard Mockup */
    .dashboard-mockup {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
        margin-bottom: 48px;
    }
    .mockup-header {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #EF4444; }
    .dot-yellow { background: #F59E0B; }
    .dot-green { background: #10B981; }

    /* Custom Cards & Hover Effects */
    .saas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 1px 2px rgba(0,0,0,.05), 0 8px 24px rgba(15,23,42,.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .saas-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 40px rgba(15, 23, 42, 0.12);
        border-color: #CBD5E1;
    }

    /* Feature List */
    .feature-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #334155;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }
    .check-icon {
        color: #22C55E;
        font-weight: bold;
    }

    /* Price Badge */
    .price-tag {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        margin: 16px 0;
    }
    .price-tag span {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Buttons Override */
    div.stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
    }

    /* Form Styling */
    [data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 8px 24px rgba(15,23,42,.06);
    }

    /* Testimonials */
    .review-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stars { color: #F59E0B; margin-bottom: 8px; }

    /* Footer */
    .footer-container {
        border-top: 1px solid #E2E8F0;
        padding-top: 32px;
        margin-top: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #64748B;
        font-size: 0.875rem;
    }
        /* ==================================================
       ตั้งค่า responsive สำหรับจอมือถือและแท็บเล็ต (<= 768px)
       ================================================== */
    @media (max-width: 768px) {
        /* 1. ลดระยะขอบรอบเว็บให้มีพื้นที่อ่านเนื้อหามากขึ้น */
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }

        /* 2. ซ่อนเมนูลิงก์ navbar ยาวๆ ไม่ให้ล้นจอมือถือ */
        .navbar-menu {
            display: none !important;
        }

        /* 3. ย่อขนาดส่วน Hero Section และตัวหนังสือ */
        .hero-container {
            padding: 36px 16px !important;
            border-radius: 20px !important;
        }
        .hero-title {
            font-size: 1.75rem !important;
            line-height: 1.25 !important;
        }
        .hero-subtitle {
            font-size: 0.95rem !important;
        }

        /* 4. ปรับขนาดการ์ดและฟอร์มกรอกข้อมูลให้กะทัดรัด */
        .saas-card, .review-card, [data-testid="stForm"] {
            padding: 20px !important;
            border-radius: 16px !important;
        }

        /* 5. ปรับส่วนโลโก้ลูกค้าให้ตัดขึ้นบรรทัดใหม่เมื่อจอลอยแน่น */
        .logo-bar {
            gap: 16px !important;
            font-size: 0.9rem !important;
            flex-wrap: wrap !important;
        }

        /* 6. ปรับ Footer ด้านล่างสุดให้เรียงเป็นแนวตั้งแทนแนวนอน */
        .footer-container {
            flex-direction: column !important;
            gap: 16px !important;
            text-align: center !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. NAVBAR
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">🚀 AppRental</div>
        <div class="navbar-menu">
            <a href="#services">บริการ</a>
            <a href="#pricing">ราคา</a>
            <a href="#reviews">รีวิว</a>
            <a href="#faq">FAQ</a>
            <a href="#register">ติดต่อ</a>
        </div>
        <div style="font-weight: 600; color: #2563EB;">[ ทดลองใช้ฟรี ]</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">AppRental<br>ระบบเว็บแอปสำหรับธุรกิจ</div>
        <div class="hero-subtitle">
            พร้อมใช้งานภายใน 5 นาที • ไม่ต้องซื้อขาด • ไม่ต้องดูแลเซิร์ฟเวอร์<br>
            ยกระดับการทำงานให้เป็นระบบและทันสมัย เริ่มต้นเพียง 159 บาท / เดือน
        </div>
    </div>
""", unsafe_allow_html=True)

hero_btn_col1, hero_btn_col2, hero_btn_col3 = st.columns([1, 2, 1])
with hero_btn_col2:
    st.button("✨ เริ่มทดลองใช้งานฟรี 30 วัน (ไม่ต้องใช้บัตรเครดิต)", key="hero_cta")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. STATS SECTION
# -----------------------------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-card"><div class="stat-number">500+</div><div class="stat-label">ลูกค้าไว้วางใจใช้งาน</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-card"><div class="stat-number">99.9%</div><div class="stat-label">Server Uptime</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-card"><div class="stat-number">24/7</div><div class="stat-label">ทีมงานคอยดูแล</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-card"><div class="stat-number">14 วัน</div><div class="stat-label">ทดลองใช้ฟรีทุกฟีเจอร์</div></div>', unsafe_allow_html=True)

# Social Proof Logos
st.markdown("""
    <div style="text-align: center; margin-top: 32px; color: #94A3B8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
        ได้รับความไว้วางใจจากผู้ใช้และร้านค้าชั้นนำ
    </div>
    <div class="logo-bar">
        <span>Google</span>
        <span>LINE</span>
        <span>Shopee</span>
        <span>Lazada</span>
        <span>TikTok</span>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. PRODUCT DASHBOARD PREVIEW
# -----------------------------------------------------------------------------
st.markdown("""
    <div class="dashboard-mockup">
        <div class="mockup-header">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
            <span style="font-size: 0.8rem; color: #94A3B8; margin-left: 8px;">apprental.co/dashboard</span>
        </div>
        <div style="background: #F8FAFC; border-radius: 12px; padding: 24px; border: 1px solid #F1F5F9;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #0F172A;">📊 สรุปยอดขายรวมประจำเดือน</div>
                <div style="color: #22C55E; font-weight: 600; font-size: 0.9rem;">+24.5% จากเดือนที่แล้ว</div>
            </div>
            <div style="height: 12px; background: #2563EB; border-radius: 6px; width: 85%; margin-bottom: 8px;"></div>
            <div style="height: 12px; background: #38BDF8; border-radius: 6px; width: 60%; margin-bottom: 8px;"></div>
            <div style="height: 12px; background: #CBD5E1; border-radius: 6px; width: 40%;"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. SERVICE CARDS (POS & APARTMENT)
# -----------------------------------------------------------------------------
st.markdown('<div id="services"></div>', unsafe_allow_html=True)
st.subheader("💡 บริการระบบแอปยอดนิยม")

c_pos, c_dorm = st.columns(2)

with c_pos:
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">🛒 POS System</div>
            <div style="color: #64748B; font-size: 0.875rem; margin-top: 4px; margin-bottom: 16px;">
                เหมาะสำหรับ: ร้านค้าทั่วไป, ร้านกาแฟ, มินิมาร์ท
            </div>
            <div class="price-tag">159 ฿ <span>/ เดือน</span></div>
            <hr style="border: none; border-top: 1px solid #F1F5F9; margin: 16px 0;">
            <div class="feature-item"><span class="check-icon">✓</span> ระบบบันทึกยอดขายหน้าร้านง่ายๆ</div>
            <div class="feature-item"><span class="check-icon">✓</span> ตัดสต็อกสินค้าให้อัตโนมัติ</div>
            <div class="feature-item"><span class="check-icon">✓</span> รองรับการสแกนบาร์โค้ด</div>
            <div class="feature-item"><span class="check-icon">✓</span> ออกใบเสร็จและรายงานยอดขาย</div>
            <div class="feature-item"><span class="check-icon">✓</span> ดึงข้อมูลเข้า Google Sheets ได้ทันที</div>
        </div>
    """, unsafe_allow_html=True)
    st.button("ทดลองใช้งาน POS", key="select_pos")

with c_dorm:
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A;">🏢 Apartment System</div>
            <div style="color: #64748B; font-size: 0.875rem; margin-top: 4px; margin-bottom: 16px;">
                เหมาะสำหรับ: หอพัก, อพาร์ทเม้นท์, ห้องเช่า
            </div>
            <div class="price-tag">199 ฿ <span>/ เดือน</span></div>
            <hr style="border: none; border-top: 1px solid #F1F5F9; margin: 16px 0;">
            <div class="feature-item"><span class="check-icon">✓</span> คำนวณค่าน้ำ-ค่าไฟ อัตโนมัติ</div>
            <div class="feature-item"><span class="check-icon">✓</span> ออกใบแจ้งหนี้ PDF สวยงาม</div>
            <div class="feature-item"><span class="check-icon">✓</span> แจ้งเตือนยอดผ่าน LINE ผู้เช่า</div>
            <div class="feature-item"><span class="check-icon">✓</span> ระบบรับแจ้งซ่อมออนไลน์</div>
            <div class="feature-item"><span class="check-icon">✓</span> สรุปรายงานการจ่ายเงินประจำเดือน</div>
        </div>
    """, unsafe_allow_html=True)
    st.button("ทดลองใช้งาน Apartment", key="select_dorm")

# -----------------------------------------------------------------------------
# 8. FEATURES GRID
# -----------------------------------------------------------------------------
st.subheader("⚡ คุณสมบัติเด่นที่ทำให้เราแตกต่าง")
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 12px;">⚡</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0F172A; margin-bottom: 8px;">พร้อมใช้ใน 5 นาที</div>
            <div style="color: #64748B; font-size: 0.9rem; line-height: 1.5;">
                ไม่ต้องรอเขียนโปรแกรมเป็นเดือนๆ สมัครเสร็จรับ ลิงก์ และสิทธิ์เข้าใช้งานได้ทันที
            </div>
        </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 12px;">🛠️</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0F172A; margin-bottom: 8px;">ดูแลระบบให้ฟรี 24 ชม.</div>
            <div style="color: #64748B; font-size: 0.9rem; line-height: 1.5;">
                มีทีมงานคอยดูแลเซิร์ฟเวอร์ สำรองข้อมูล และอัปเดตฟีเจอร์ใหม่ๆ ให้ตลอดเวลา
            </div>
        </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 2rem; margin-bottom: 12px;">📱</div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0F172A; margin-bottom: 8px;">รองรับทุกอุปกรณ์</div>
            <div style="color: #64748B; font-size: 0.9rem; line-height: 1.5;">
                ใช้งานผ่านเบราว์เซอร์บนมือถือ แท็บเล็ต หรือคอมพิวเตอร์ได้ทันทีโดยไม่ต้องลงแอป
            </div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. TESTIMONIALS
# -----------------------------------------------------------------------------
st.markdown('<div id="reviews"></div>', unsafe_allow_html=True)
st.subheader("💬 เสียงตอบรับ")

r1, r2 = st.columns(2)
with r1:
    st.markdown("""
        <div class="review-card">
            <div class="stars">★★★★★</div>
            <div style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin-bottom: 12px;">
                "ตั้งแต่เปลี่ยนมาใช้ระบบ POS ของ AppRental การเช็คสต็อกง่ายขึ้นมาก ประหยัดเวลาไปได้วันละหลายชั่วโมง ยอดขายโตขึ้นชัดเจนครับ"
            </div>
            <div style="font-weight: 700; color: #0F172A;">คุณสมชาย</div>
            <div style="font-size: 0.8rem; color: #64748B;">เจ้าของร้าน ABC MiniMart</div>
        </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
        <div class="review-card">
            <div class="stars">★★★★★</div>
            <div style="color: #334155; font-size: 0.95rem; line-height: 1.6; margin-bottom: 12px;">
                "ระบบจัดการหอพักช่วยให้ออกบิลค่าน้ำไฟไวมาก ผู้เช่าก็ชอบเพราะแจ้งเตือนเข้า LINE ตรงๆ ไม่ต้องคอยตามจดกระดาษอีกต่อไป"
            </div>
            <div style="font-weight: 700; color: #0F172A;">คุณเอก</div>
            <div style="font-size: 0.8rem; color: #64748B;">ผู้บริหาร Apartment XYZ</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 10. FAQ SECTION
# -----------------------------------------------------------------------------
st.markdown('<div id="faq"></div>', unsafe_allow_html=True)
st.subheader("❓ คำถามที่พบบ่อย (FAQ)")

with st.expander("Q: สามารถทดลองใช้งานฟรีได้กี่วัน?"):
    st.write("A: สามารถทดลองใช้งานได้ฟรี 30 วันเต็ม โดยไม่ต้องกรอกข้อมูลบัตรเครดิตครับ")

with st.expander("Q: สามารถยกเลิกการเช่าเมื่อไรก็ได้ใช่ไหม?"):
    st.write("A: ใช่ครับ ไม่มีสัญญาผูกมัดใดๆ คุณสามารถยกเลิกหรือเปลี่ยนแพ็กเกจได้ทุกเมื่อ")

with st.expander("Q: ข้อมูลภายในระบบมีความปลอดภัยแค่ไหน?"):
    st.write("A: ปลอดภัยสูงและเป็นส่วนตัว 100% ด้วยโครงสร้างการเก็บข้อมูลใน Google Drive ของลูกค้าเองครับ
    * **คุณเป็นเจ้าของข้อมูล 100%:** ข้อมูลบันทึกตรงเข้า Google Sheets ของคุณ ไม่ได้เก็บไว้ที่เซิร์ฟเวอร์ส่วนกลางของเรา
    * **เข้ารหัสตามมาตรฐาน Google:** การส่งข้อมูลทั้งหมดผ่านโปรโตคอลเข้ารหัส SSL/TLS (HTTPS)
    * **ควบคุมสิทธิ์ได้เอง:** มีเพียงคุณและผู้ที่คุณอนุญาตใน Google Drive เท่านั้นที่เปิดดูไฟล์ได้")

st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 11. LEAD FORM / REGISTER
# -----------------------------------------------------------------------------
st.markdown('<div id="register"></div>', unsafe_allow_html=True)
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
    
    submit = st.form_submit_button("🚀 ส่งข้อมูลขอรับสิทธิ์ใช้งานฟรี")

    if submit:
        if name and email:
            payload = {
                "name": name,
                "email": email,
                "selected_app": selected_app,
                "note": note
            }
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                st.balloons()
                st.success(f"🎉 ขอบคุณครับคุณ {name}! บันทึกข้อมูลเรียบร้อยแล้ว ทีมงานจะติดต่อกลับโดยเร็วที่สุดครับ")
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการส่งข้อมูล กรุณาตรวจสอบอินเทอร์เน็ตหรือลองใหม่อีกครั้ง")
        else:
            st.warning("⚠️ กรุณากรอกชื่อและช่องทางการติดต่อให้ครบถ้วนนะครับ")

# -----------------------------------------------------------------------------
# 12. BOTTOM CTA BANNER & FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
    <div style="background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); border-radius: 24px; padding: 48px; color: white; text-align: center; margin-top: 48px;">
        <h2 style="color: white; font-weight: 800; margin-bottom: 8px;">พร้อมเริ่มใช้งานแล้วหรือยัง?</h2>
        <p style="color: #93C5FD; font-size: 1.05rem; margin-bottom: 24px;">ทดลองใช้ฟรี 14 วัน ไม่ต้องใช้บัตรเครดิต</p>
    </div>
    
    <div class="footer-container">
        <div>
            <strong style="color: #0F172A;">AppRental</strong><br>
            บริการให้เช่าระบบเว็บแอปสำหรับธุรกิจ
        </div>
        <div>
            • LINE @222utxsg
            ©2026 AppRental. All rights reserved.
        </div>
    </div>
""", unsafe_allow_html=True)
