import streamlit as st
from PIL import Image, ImageDraw

# 1. 페이지 기본 설정 (샤프 블랙 디자인)
st.set_page_config(
    page_title="VIRSTAGED | 2.5D Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. VIRSTAGED 매트 블랙 & 핫핑크 스타일 커스텀 CSS
st.markdown("""
    <style>
    /* Obsidian Black Base Background */
    .stApp {
        background-color: #050505;
        color: #F5F6F8;
    }
    /* Sharp Edges (0px Radius) & Matte Dark Panels */
    div[data-baseweb="select"], div[data-baseweb="input"], button, div[class*="stCard"] {
        border-radius: 0px !important;
    }
    /* Hot Pink Primary Button Accent */
    button[kind="primary"] {
        background-color: #FF007F !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
    }
    button[kind="primary"]:hover {
        background-color: #E0006F !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 테스트용 가짜(더미) 에셋 자동 생성 함수
def create_dummy_character():
    img = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 가짜 아바타 형상 (핑크 사각형 + 텍스트)
    draw.rectangle([50, 100, 250, 350], fill=(255, 0, 127, 200), outline=(255, 255, 255, 255), width=3)
    draw.text((100, 200), "DUMMY AVATAR", fill=(255, 255, 255, 255))
    return img

def create_dummy_background():
    img = Image.new('RGB', (800, 500), (18, 18, 24))
    draw = ImageDraw.Draw(img)
    # 가짜 그리드 배경
    for i in range(0, 800, 40):
        draw.line([(i, 0), (i, 500)], fill=(40, 40, 60), width=1)
    for j in range(0, 500, 40):
        draw.line([(0, j), (800, j)], fill=(40, 40, 60), width=1)
    draw.text((320, 240), "[ VIRTUAL STAGE CANVAS ]", fill=(100, 100, 150))
    return img

# 4. 세션 상태 초기화 (초기 화면: SETUP)
if 'scene' not in st.session_state:
    st.session_state.scene = 'SETUP'

# 5. 상단 헤더 로고
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #222; padding-bottom: 10px;">
        <h2 style="color: #F5F6F8; margin: 0; font-family: monospace;">VIRSTAGED <span style="font-size:14px; color:#8D99AE;">| 2.5D Studio</span></h2>
        <span style="color: #FF007F; font-size: 12px; font-weight: bold;">● STATUS: PREVIEW MODE</span>
    </div>
""", unsafe_allow_html=True)
st.write("")

# ─────────────────────────────────────────────────────────────
# SCENE 1: SETUP ROOM (준비 화면)
# ─────────────────────────────────────────────────────────────
if st.session_state.scene == 'SETUP':
    st.markdown("#### ⚙️ SETUP ROOM")
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.write("**ASSET CONFIGURATION**")
        st.file_uploader("CHARACTER IMAGE (PNG)", type=['png', 'jpg'])
        st.file_uploader("BACKGROUND IMAGE (JPG)", type=['jpg', 'png'])
        st.file_uploader("AUDIO BGM (.MP3)", type=['mp3'])
        
        st.write("")
        # 핫핑크 메인 실행 버튼
        if st.button("START STAGE", type="primary", use_container_width=True):
            st.session_state.scene = 'LIVE'
            st.rerun()
            
    with col2:
        st.write("**PREVIEW CANVAS**")
        # 가짜 이미지 합성하여 미리보기 제공
        bg_preview = create_dummy_background()
        char_preview = create_dummy_character()
        bg_preview.paste(char_preview, (250, 50), char_preview)
        st.image(bg_preview, caption="Auto-generated Dummy Preview", use_container_width=True)

# ─────────────────────────────────────────────────────────────
# SCENE 2: LIVE STAGE (본 무대 화면)
# ─────────────────────────────────────────────────────────────
elif st.session_state.scene == 'LIVE':
    # 상단 툴바 버튼
    t_col1, t_col2, t_col3, t_col4 = st.columns([2, 1, 1, 1])
    with t_col1:
        st.markdown("<h4 style='margin:0; color:#FF007F;'>LIVE STAGE VIEWPORT</h4>", unsafe_allow_html=True)
    with t_col2:
        if st.button("📸 CAPTURE", use_container_width=True):
            st.toast("Snapshot Captured!")
    with t_col3:
        if st.button("🎬 RECORD", type="primary", use_container_width=True):
            st.toast("Recording Started...")
    with t_col4:
        if st.button("🛑 STOP STAGE", use_container_width=True):
            st.session_state.scene = 'REVIEW'
            st.rerun()
            
    st.divider()
    
    # 무대 메인 화면 + 우측 조종 사이드바
    stage_col, ctrl_col = st.columns([3, 1])
    
    with stage_col:
        bg_preview = create_dummy_background()
        char_preview = create_dummy_character()
        bg_preview.paste(char_preview, (250, 50), char_preview)
        st.image(bg_preview, caption="[ 2.5D Interactive Stage Viewport ]", use_container_width=True)
        
    with ctrl_col:
        st.write("**STAGE CONTROL**")
        st.write("---")
        st.write("■ AUDIO")
        st.slider("VOLUME", 0, 100, 80)
        st.checkbox("AUDIO SYNC", value=True)
        
        st.write("---")
        st.write("■ LIGHTING")
        st.color_picker("LIGHT COLOR", "#FF007F")
        st.slider("INTENSITY", 0, 100, 50)
        
        st.write("---")
        st.write("■ VISUAL FX")
        st.selectbox("PARTICLE", ["CHERRY BLOSSOM", "CYBER DUST", "STAGE FOG"])
        st.slider("Z-DEPTH", 0, 100, 30)

# ─────────────────────────────────────────────────────────────
# SCENE 3: REVIEW ROOM (결과 화면)
# ─────────────────────────────────────────────────────────────
elif st.session_state.scene == 'REVIEW':
    st.markdown("#### 🎬 REVIEW ROOM")
    
    r_col1, r_col2 = st.columns([1, 1])
    with r_col1:
        st.write("**CAPTURED SHOTS**")
        st.image(create_dummy_background(), caption="SNAPSHOT_01.PNG", width=250)
        st.button("DOWNLOAD ALL SHOTS")
    with r_col2:
        st.write("**RECORDED VIDEO**")
        st.info("Video playback player will be rendered here.")
        
    st.divider()
    if st.button("RESTART SESSION", type="primary"):
        st.session_state.scene = 'SETUP'
        st.rerun()
