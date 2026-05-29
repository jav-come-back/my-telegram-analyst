import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import io
from matplotlib.font_manager import FontProperties # 🎯 បន្ថែមសម្រាប់គ្រប់គ្រង Font

# 🔑 ព័ត៌មាន Telegram Bot របស់អ្នក
TELEGRAM_BOT_TOKEN = "8760142697:AAG8Er5MJfIQfyUeGC0jxVbK7hUKlgnv8Ts"
TELEGRAM_CHAT_ID = "-5079160685"

# 🎯 អនុគមន៍ទាញយកពុម្ពអក្សរខ្មែរពី Google Fonts មកប្រើក្នុង Matplotlib កុំឱ្យលោតការ៉េៗ
@st.cache_data
def get_khmer_font():
    try:
        font_url = "https://github.com/google/fonts/raw/main/ofl/hanuman/Hanuman-Regular.ttf"
        response = requests.get(font_url, timeout=10)
        font_data = io.BytesIO(response.content)
        return FontProperties(fname=font_data)
    except Exception:
        # បើអ៊ីនធឺណិតមានបញ្ហា វានឹងប្រើ Font ធម្មតារបស់ប្រព័ន្ធសិនដើម្បីកុំឱ្យគាំង
        return FontProperties()

khmer_font = get_khmer_font()

def send_telegram_report(message, chart_fig=None):
    """អនុគមន៍បាញ់ទាំងអត្ថបទ និងរូបភាពក្រាហ្វទៅកាន់ Telegram ក្នុងពេលតែមួយ"""
    try:
        if chart_fig is not None:
            img_buf = io.BytesIO()
            chart_fig.savefig(img_buf, format='png', dpi=300, bbox_inches='tight')
            img_buf.seek(0)
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            files = {'photo': ('chart.png', img_buf, 'image/png')}
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': message,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=payload, files=files)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, json=payload)
            
        return response.status_code == 200
    except Exception as e:
        st.error(f"Telegram Engine Error: {e}")
        return False

# 🌐 การกำหนด cấu hình trang Web Interface แบบ Premium
st.set_page_config(page_title="Executive Data Analyst Suite", page_icon="📊", layout="wide")

# 🎨 Custom Advanced CSS injection សម្រាប់ស្ទីលវេបសាយកម្រិតខ្ពស់ (Clean & Corporate UI)
st.markdown("""
    <style>
    /* ប្តូរពណ៌ផ្ទៃខាងក្រោយ និងពុម្ពអក្សរមេ */
    .stApp { background-color: #F8FAFC; color: #1E293B; }
    
    /* ស្ទីលចំណងជើងធំ */
    .main-header { font-size: 36px !important; font-weight: 800 !important; color: #0F172A; text-align: center; margin-bottom: 2px; letter-spacing: -0.5px; }
    .sub-header { font-size: 15px !important; text-align: center; color: #64748B; margin-bottom: 30px; font-weight: 400; }
    
    /* កែសម្រួលប៊ូតុងរត់ និងប៊ូតុង Upload */
    div.stButton > button:first-child {
        background-color: #2563EB !important; color: white !important; font-weight: 600 !important;
        border-radius: 8px !important; border: none !important; padding: 10px 24px !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important; transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover { background-color: #1D4ED8 !important; transform: translateY(-1px); }
    
    /* ស្ទីលប្រអប់ Card ព័ត៌មានសង្ខេប */
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #0F172A !important; }
    div[data-testid="stMetricLabel"] { font-size: 13px !important; color: #475569 !important; text-transform: uppercase; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# បង្ហាញចំណងជើងធំលំដាប់អាជីព
st.markdown('<h1 class="main-header">📊 EXECUTIVE DATA ANALYST SUITE</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🤖 Real-time Business Intelligence & Automated Telegram Dispatch Engine</p>', unsafe_allow_html=True)
st.write("---")

# 📥 ផ្ទាំងអូសទម្លាក់ File បែបស្អាតស្អំ
uploaded_file = st.file_uploader("📥 Drag and drop your business dataset (CSV, XLSX, or XLS)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # អានទិន្នន័យ
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"⚡ **System Connected:** `{uploaded_file.name}` loaded with {len(df):,} records successfully.")
        
        # ------------------------------------------------------------------
        # SIDEBAR CONTROL PANEL
        # ------------------------------------------------------------------
        st.sidebar.markdown("### 🛠️ CONTROL PANEL")
        columns_list = df.columns.tolist()
        
        x_axis = st.sidebar.selectbox("📊 X-Axis (Categories):", columns_list, index=0)
        y_axis = st.sidebar.selectbox("📈 Y-Axis (Metrics):", columns_list, index=min(1, len(columns_list)-1))
        
        chart_type = st.sidebar.selectbox("🎨 Visualization View:", [
            "Vertical Bar Chart",
            "Horizontal Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Area Chart",
            "Scatter Plot"
        ])
        
        st.sidebar.write("---")
        st.sidebar.markdown("<small style='color:#64748B;'>Engine Status: Ready ✅</small>", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # MAIN DASHBOARD LAYOUT
        # ------------------------------------------------------------------
        tab1, tab2 = st.tabs(["📋 Executive Overview", "📊 Deep Visualizer Engine"])
        
        with tab1:
            st.markdown("### 📋 METRIC INSIGHT CARDS")
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Total Records", f"{len(df):,}")
            m_col2.metric("Data Features", f"{len(df.columns)} Columns")
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            m_col3.metric("Numeric Metrics", f"{len(numeric_cols)}")
            
            st.write("---")
            st.markdown("### 👀 Dataset Preview (First 5 Data Rows)")
            st.dataframe(df.head(5), use_container_width=True)
            
            if len(numeric_cols) > 0:
                with st.expander("🔍 View Core Statistical Summary"):
                    st.dataframe(df[numeric_cols].describe().loc[['mean', 'min', 'max']], use_container_width=True)

        with tab2:
            st.markdown("### 📊 INTERACTIVE GRAPHICAL CHART")
            
            # 🔄 Smart Processing Engine
            y_converted = pd.to_numeric(df[y_axis], errors='coerce')
            y_is_numeric = y_converted.notna().sum() > (len(df) * 0.5)
            
            if not y_is_numeric:
                agg_data = df.groupby(x_axis).size().reset_index(name='COUNT').head(15)
                x_plot = agg_data[x_axis].astype(str).tolist()
                y_plot = agg_data['COUNT'].tolist()
                metric_label = f"Count of {y_axis}"
            else:
                agg_data = df.groupby(x_axis)[y_axis].sum().reset_index().head(15)
                x_plot = agg_data[x_axis].astype(str).tolist()
                y_plot = pd.to_numeric(agg_data[y_axis], errors='coerce').fillna(0).tolist()
                metric_label = f"Sum of {y_axis}"
                
            # បង្កើតក្រាហ្វិក Matplotlib បែបពណ៌ Modern & Clean
            fig, ax = plt.subplots(figsize=(10, 4.5))
            ax.set_facecolor('#FFFFFF')
            fig.patch.set_facecolor('#F8FAFC')
            ax.grid(True, linestyle='--', alpha=0.3, color='#CBD5E1', zorder=0)
            
            # 🎨 ប្រព័ន្ធពណ៌បែប Premium Corporate
            color_palette = ['#1E40AF', '#0D9488', '#3B82F6', '#14B8A6', '#6366F1', '#EC4899', '#F59E0B', '#10B981']
            chart_colors = [color_palette[i % len(color_palette)] for i in range(len(x_plot))]
            
            if "Vertical Bar Chart" in chart_type:
                bars = ax.bar(x_plot, y_plot, color=chart_colors, width=0.5, edgecolor='none', zorder=3)
                ax.bar_label(bars, padding=4, fmt='{:,.0f}', fontsize=8, color='#475569', weight='bold')
                
                # 🎯 ដាក់ Font ខ្មែរទៅឱ្យប្រអប់ Legend
                labels_handles = [plt.Rectangle((0,0),1,1, color=chart_colors[i]) for i in range(len(x_plot))]
                ax.legend(labels_handles, x_plot, title=x_axis, loc="center left", bbox_to_anchor=(1, 0.5), prop=khmer_font).get_title().set_fontproperties(khmer_font)

            elif "Horizontal Bar Chart" in chart_type:
                bars = ax.barh(x_plot, y_plot, color=chart_colors, height=0.5, edgecolor='none', zorder=3)
                ax.bar_label(bars, padding=4, fmt='{:,.0f}', fontsize=8, color='#475569', weight='bold')
                
                # 🎯 ដាក់ Font ខ្មែរទៅឱ្យប្រអប់ Legend
                labels_handles = [plt.Rectangle((0,0),1,1, color=chart_colors[i]) for i in range(len(x_plot))]
                ax.legend(labels_handles, x_plot, title=x_axis, loc="center left", bbox_to_anchor=(1, 0.5), prop=khmer_font).get_title().set_fontproperties(khmer_font)

            elif "Line Chart" in chart_type:
                ax.plot(x_plot, y_plot, marker='o', color='#F59E0B', linewidth=2, markersize=6, zorder=3)
                for i, val in enumerate(y_plot):
                    ax.annotate(f'{val:,.0f}', (x_plot[i], y_plot[i]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8, color='#475569', weight='bold')
            
            elif "Pie Chart" in chart_type:
                wedges, texts, autotexts = ax.pie(y_plot, labels=x_plot, autopct='%1.1f%%', startangle=90, colors=chart_colors)
                plt.setp(autotexts, size=8, weight="bold")
                
                # 🎯 កែសម្រួលអក្សរខ្មែរជុំវិញនំខេក កុំឱ្យចេញប្រអប់ការ៉េ
                for text in texts:
                    text.set_fontproperties(khmer_font)
                
                # 🎯 ដាក់ Font ខ្មែរទៅឱ្យប្រអប់ Legend
                ax.legend(wedges, x_plot, title=x_axis, loc="center left", bbox_to_anchor=(1, 0.5), prop=khmer_font).get_title().set_fontproperties(khmer_font)
                ax.axis('equal')
                
            elif "Area Chart" in chart_type:
                ax.fill_between(x_plot, y_plot, color='#6366F1', alpha=0.2, zorder=2)
                ax.plot(x_plot, y_plot, color='#6366F1', linewidth=2, zorder=3)
                
            elif "Scatter Plot" in chart_type:
                ax.scatter(x_plot, y_plot, color='#EF4444', s=100, alpha=0.8, edgecolors='none', zorder=3)
                
            if "Pie Chart" not in chart_type:
                # 🎯 បញ្ចូល Font ខ្មែរទៅកាន់ឈ្មោះអ័ក្ស X និង Y
                ax.set_xlabel(x_axis, fontsize=9, fontweight='bold', color='#475569', fontproperties=khmer_font)
                ax.set_ylabel(metric_label, fontsize=9, fontweight='bold', color='#475569', fontproperties=khmer_font)
                
                # 🎯 បញ្ចូល Font ខ្មែរទៅកាន់ឈ្មោះទិន្នន័យនៅលើអ័ក្ស (Ticks)
                for label in ax.get_xticklabels():
                    label.set_fontproperties(khmer_font)
                for label in ax.get_yticklabels():
                    label.set_fontproperties(khmer_font)
                    
                for spine in ['top', 'right']:
                    ax.spines[spine].set_visible(False)
                for spine in ['left', 'bottom']:
                    ax.spines[spine].set_color('#E2E8F0')
                    
            # 🎯 បញ្ចូល Font ខ្មែរទៅកាន់ចំណងជើងធំរបស់ក្រាហ្វិក
            ax.set_title(f"{metric_label} broken down by {x_axis}", fontsize=11, fontweight='bold', color='#0F172A', pad=15, fontproperties=khmer_font)
            
            # បង្ហាញក្រាហ្វិក
            st.pyplot(fig)
            
            # ------------------------------------------------------------------
            # TELEGRAM DISPATCH SECTION
            # ------------------------------------------------------------------
            st.write("---")
            st.markdown("### 🚀 TELEGRAM EXECUTIVE DISPATCH")
            
            if st.button("📤 Transmission Report to Clients Telegram"):
                summary_text = (
                    f"📊 *🔴 LIVE ENTERPRISE DATA REPORT* 📊\n\n"
                    f"📂 *Dataset Name:* `{uploaded_file.name}`\n"
                    f"🔹 *Total Records:* {len(df):,} rows\n\n"
                    f"📈 *Metric Focused:* `{metric_label}`\n"
                    f"🎯 *Categorized By:* `{x_axis}`\n\n"
                    f"📢 *Status:* Analysis report dispatched seamlessly."
                )
                
                with st.spinner("Transmitting encrypted summary and high-res chart..."):
                    success = send_telegram_report(summary_text, chart_fig=fig)
                    if success:
                        st.balloons()
                        st.success("🚀 **Dispatched Successfully!** High-resolution chart sent to client's Telegram channels.")
                    else:
                        st.error("❌ **Failed!** Verify network rules or Bot connection details.")
                        
    except Exception as e:
        st.error(f"❌ System Error: {e}")