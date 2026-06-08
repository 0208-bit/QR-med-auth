import streamlit as st
import uuid
from blockchain_sim import add_medicine, verify_medicine
from qr_utils import generate_qr

# For QR scanning
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

st.title("DrugsVrf | QR-Based Drugs Authentication")

page = st.sidebar.selectbox("Choose Role", ["Manufacturer", "Customer"])

if page == "Manufacturer":
    st.header("Register New Medicine")
    name = st.text_input("Medicine Name")
    batch = st.text_input("Batch Number")
    expiry = st.date_input("Expiry Date")
    manufacturer = st.text_input("Manufacturer Name")

    if st.button("Register Medicine"):
        med_id = str(uuid.uuid4())[:8]
        add_medicine(med_id, name, batch, str(expiry), manufacturer)
        qr_path = generate_qr(med_id, name, batch, expiry, manufacturer)
        st.write("QR Data Encoded:", f"ID:{med_id}, Name:{name}, Batch:{batch}, Exp:{expiry}, Mfg:{manufacturer}")

        st.success(f"Medicine registered with ID: {med_id}")
        st.image(qr_path, caption="🔍 Scan to Verify Medicine")
        

elif page == "Customer":
    option = st.radio("Verification Method", ["Enter Code", "Scan QR Code"])

    if option == "Scan QR Code":
        uploaded_file = st.file_uploader("Upload QR Code", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            from PIL import Image
            import numpy as np
            import cv2

            image = Image.open(uploaded_file).convert("RGB")
            image_np = np.array(image)
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(image_np)

            if data:
                st.success("✅ Medicine Verified!")
                st.write("QR Code Data:", data)
            else:
                st.error("❌ No valid QR code found in the image.")

    if option == "Enter Code":
        st.header("Verify Medicine Manually")
        med_id = st.text_input("Enter Medicine QR Code / ID")
        if st.button("Verify"):
            data = verify_medicine(med_id)
            if data:
                st.success("✅ Medicine is Authentic")
                st.json(data)
            else:
                st.error("❌ Medicine not found or is counterfeit")

    elif option == "Scan QR Code":
        st.header("Scan QR Code with Camera")

        class QRScanner(VideoProcessorBase):
            def __init__(self):
                self.result = None
                self.qr_detector = cv2.QRCodeDetector()

            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")
                val, pts, _ = self.qr_detector.detectAndDecode(img)
                if val:
                    self.result = val
                return av.VideoFrame.from_ndarray(img, format="bgr24")

        ctx = webrtc_streamer(
            key="qr",
            video_processor_factory=QRScanner,
            rtc_configuration=RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            ),
            media_stream_constraints={"video": True, "audio": False},
        )

        if ctx.video_processor:
            qr_code = ctx.video_processor.result
            if qr_code:
                st.success(f"QR Code Detected: {qr_code}")
                data = verify_medicine(qr_code)
                if data:
                    st.success("✅ Medicine is Authentic")
                    st.json(data)
                else:
                    st.error("❌ Medicine not found or is counterfeit")
