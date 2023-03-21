import streamlit as st
from streamlit_option_menu import option_menu
import PIL.Image as Image
import cv2
import numpy as np

# Canny法の仮のしきい値を決定
def calc_thres(image):
    sigma = 0.33  # 0.33
    med_val = np.median(image)
    min_val = int(max(0, (1.0 - sigma) * med_val))
    max_val = int(min(255, (1.0 + sigma) * med_val))
    return min_val,max_val

imfile = st.file_uploader("ファイルアップロード", type=['jpg','jpeg','png'])
if imfile:
    inimage = Image.open(imfile)
    cvimage = np.array(inimage,np.uint8)
    cvimage = cv2.cvtColor(cvimage,cv2.COLOR_RGB2GRAY)

selected=option_menu(None, ["二階調化", "エッジ検出"], 
    menu_icon="cast", default_index=0, orientation="vertical"
)
st.title(f"{selected}")

if selected=="二階調化":
    selected2 = st.selectbox("処理モード", ('デフォルト', '反転','大津の方法')) 

    col1,col2 = st.columns([1,1])
    if selected2 == '大津の方法':
        slider = st.slider("しきい値", 0, 255, 127, 1,disabled=True)
    else:
        slider = st.slider("しきい値", 0, 255, 127, 1)
    
    with col1:
        st.header('入力画像')
        if imfile:
            st.image(inimage,caption='入力画像',use_column_width=True)

    with col2:
        global ret
        st.header('二階調画像')
        if imfile:
            op3 = {'デフォルト':cv2.THRESH_BINARY,
                   '反転':cv2.THRESH_BINARY_INV,
                   '大津の方法':cv2.THRESH_OTSU}
            ret,cvimage = cv2.threshold(cvimage,slider,255,op3[selected2])
            outimage = Image.fromarray(cvimage)
            st.image(outimage, caption='結果画像',use_column_width=True)
            
    if imfile and selected2 == '大津の方法':
        slider = ret 
    st.markdown(f"## しきい値:{slider}")

if selected=="エッジ検出":
    
    selected3 = st.radio("処理モード", ('Sobel','SobelX', 'SobelY','Canny'),horizontal=True) 

    col1,col2 = st.columns([1,1])
    if imfile and selected3 == 'Canny':
        m1,m2 = calc_thres(cvimage)
        minVal = st.slider("minVal", 0, 255, m1, 1)
        maxVal = st.slider("maxVal", 0, 255, m2, 1)
    
    with col1:
        st.header('入力画像')
        if imfile:
            st.image(inimage,caption='入力画像',use_column_width=True)

    with col2:
        st.header('エッジ画像')
        if imfile:
            if selected3 != 'Canny':
                cviX,cviY = 0.0, 0.0
                if selected3 != 'SobelX':
                    cviX = cv2.Sobel(cvimage,cv2.CV_64F,0,1,ksize=3)
                if selected3 != 'SobelY':
                    cviY = cv2.Sobel(cvimage,cv2.CV_64F,1,0,ksize=3)
                cvimage = np.sqrt(cviX ** 2 + cviY ** 2).astype(np.uint8)      
            else: # 'Canny':
                cvimage = cv2.Canny(cvimage,threshold1=minVal, threshold2=maxVal)
            outimage = Image.fromarray(cvimage)
            st.image(outimage, caption='結果画像',use_column_width=True)
