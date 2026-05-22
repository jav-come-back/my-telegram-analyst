import streamlit as st
import pandas as pd
import requests
import io

# 🔑 កំណត់ព័ត៌មាន Telegram Bot របស់អ្នកនៅទីនេះ
TELEGRAM_BOT_TOKEN = "8760142697:AAG8Er5MJfIQfyUeGC0jxVbK7hUKlgnv8Ts"  # ជំនួសដោយ Token របស់អ្នក
TELEGRAM_CHAT_ID = "-5079160685"      # ជំនួសដោយ Chat ID របស់អ្នក

def send_telegram_message(message):
    """អនុគមន៍សម្រាប់បាញ់សារទៅកាន់ Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Telegram Error: {e}")
        return False

# 🌐 ការរៀបចំផ្ទាំង Web Interface របស់ Streamlit
st.set_page_config(page_title="Universal Data Analyst Tool", page_icon="🌐", layout="centered")

st.title("🌐 UNIVERSAL DATA ANALYST TOOL")
st.markdown("💡 *Upload ឯកសាររបស់អ្នកដើម្បីមើល Summary និងបាញ់ចូល Telegram ភ្លាមៗ*")
st.write("---")

# 📥 ផ្ទាំងសម្រាប់ឱ្យអ្នកប្រើប្រាស់អូសទម្លាក់ File (Upload)
uploaded_file = st.file_uploader("📥 ចុចទីនេះដើម្បី Upload File (CSV ឬ Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # អានទិន្នន័យពី File ដែលបាន Upload
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"✅ បានផ្ទុកទិន្នន័យជោគជ័យ: {len(df)} ជួរ ផ្អែកលើ File `{uploaded_file.name}`")
        
        # 📋 បង្ហាញ Data Profile Summary លើ Web
        st.subheader("📋 DATA PROFILE SUMMARY")
        col1, col2 = st.columns(2)
        col1.metric("Total Records", f"{len(df)} rows")
        col2.metric("Total Columns", f"{len(df.columns)} cols")
        
        # 👀 Data Preview
        st.write("### 👀 ទិន្នន័យគំរូ (Top 5 Rows)")
        st.dataframe(df.head(5))
        
        st.write("---")
        st.subheader("🚀 មុខងារបាញ់របាយការណ៍ (Notification)")
        
        # បង្កើតប៊ូតុងចុចផ្ញើ
        if st.button("📤 ផ្ញើរបាយការណ៍សង្ខេបទៅ Telegram"):
            # រៀបចំអត្ថបទសង្ខេបសម្រាប់ផ្ញើ
            summary_text = (
                f"📊 *🔴 NEW DATA ANALYST REPORT* 📊\n\n"
                f"📂 *File Name:* `{uploaded_file.name}`\n"
                f"🔹 *Total Records:* {len(df):,} rows\n"
                f"🔹 *Total Columns:* {len(df.columns)} columns\n\n"
                f"📈 *Top 5 Values Counter (Sample Data):*\n"
            )
            
            # យក Column ទីមួយ និងទីពីរមកធ្វើគំរូរាប់ចំនួនជួរផ្ញើទៅជា Summary
            first_col = df.columns[0]
            top_values = df[first_col].value_counts().head(5)
            for val, count in top_values.items():
                summary_text += f"• `{val}`: {count:,} ដង\n"
                
            summary_text += f"\n📢 *Status:* ទិន្នន័យត្រូវបានវិភាគ និងផ្ទៀងផ្ទាត់រួចរាល់។"
            
            # ដំណើរការផ្ញើ
            with st.spinner("កំពុងបាញ់សារទៅកាន់ Telegram..."):
                success = send_telegram_message(summary_text)
                if success:
                    st.balloons()
                    st.success("🚀 បានផ្ញើរបាយការណ៍សង្ខេបទៅកាន់ Telegram Group របស់អ្នករួចរាល់ហើយ!")
                else:
                    st.error("❌ ការផ្ញើបានបរាជ័យ! សូមពិនិត្យមើល Bot Token និង Chat ID ឡើងវិញ។")
                    
    except Exception as e:
        st.error(f"❌ មានបញ្ហាក្នុងការអានឯកសារ: {e}")