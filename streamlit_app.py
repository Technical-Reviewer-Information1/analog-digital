import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
from PIL import Image, ImageFilter, ImageEnhance
import io
import random

# Page configuration
st.set_page_config(
    page_title="アナログとデジタルの違い",
    page_icon="🌊",
    layout="wide"
)

# Main title and credits
st.title("アナログとデジタルの違い 🌊💻")
st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

st.markdown("""
この学習アプリでは、アナログとデジタルの「情報の表現方法の違い」と、
それによって生まれる「ノイズ耐性」や「コピー耐性」などの特長を、
視覚的・対話的なシミュレーションを通じて直感的に理解できます。
""")

# Content 1: Noise Resistance
st.markdown("## 🤔 体験1：ノイズに強いのはどっち？")
st.markdown("アナログ信号とデジタル信号、どちらがノイズに強いか体験してみましょう！")

# Control panel with better layout
col_control1, col_control2 = st.columns([3, 1])
with col_control1:
    noise_level = st.slider("🔊 ノイズの量を調整", 0, 100, 0, key="noise_slider", help="スライダーを動かしてノイズレベルを変更")
with col_control2:
    st.metric("ノイズレベル", f"{noise_level}%")

# Create analog and digital signals
x = np.linspace(0, 4*np.pi, 1000)
analog_signal = np.sin(x)
digital_signal = np.where(np.sin(x) > 0, 1, -1)

# Add noise
noise = np.random.normal(0, noise_level/100, len(x))
analog_with_noise = analog_signal + noise
digital_with_noise = digital_signal + noise

# Digital signal restoration
digital_restored = np.where(digital_with_noise > 0, 1, -1)

# Plot signals
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📻 アナログ信号")
    
    # Create subplot
    fig1 = sp.make_subplots(
        rows=2, cols=1,
        subplot_titles=('元のアナログ信号', 'ノイズが加わった信号'),
        vertical_spacing=0.15
    )
    
    # Original analog
    fig1.add_trace(
        go.Scatter(x=x, y=analog_signal, mode='lines', name='元の信号',
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Noisy analog
    fig1.add_trace(
        go.Scatter(x=x, y=analog_with_noise, mode='lines', name='ノイズありの信号',
                  line=dict(color='red', width=1)),
        row=2, col=1
    )
    
    if noise_level > 0:
        fig1.add_trace(
            go.Scatter(x=x, y=analog_signal, mode='lines', name='元の信号（参考）',
                      line=dict(color='blue', width=1, dash='dash'), opacity=0.5),
            row=2, col=1
        )
    
    fig1.update_xaxes(title_text="時間", row=2, col=1)
    fig1.update_yaxes(title_text="振幅", range=[-2, 2])
    fig1.update_layout(
        height=500,
        showlegend=False,
        template='plotly_white',
        hovermode='x unified'
    )
    
    # Add annotations for better understanding
    if noise_level > 50:
        fig1.add_annotation(
            text="⚠️ 高ノイズ：復元困難",
            xref="paper", yref="paper",
            x=0.5, y=0.02, showarrow=False,
            font=dict(size=12, color="red")
        )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    if noise_level > 30:
        st.error("復元が難しい... 😵")
        st.write("ノイズと元の信号を区別できません")
    elif noise_level > 0:
        st.warning("復元が困難になってきています")
    else:
        st.success("クリアな信号です！")

with col2:
    st.markdown("### 💻 デジタル信号")
    
    # Create subplot
    fig2 = sp.make_subplots(
        rows=3, cols=1,
        subplot_titles=('元のデジタル信号', 'ノイズが加わった信号', '復元された信号'),
        vertical_spacing=0.1
    )
    
    # Original digital
    fig2.add_trace(
        go.Scatter(x=x, y=digital_signal, mode='lines', name='元の信号',
                  line=dict(color='green', width=2)),
        row=1, col=1
    )
    
    # Noisy digital
    fig2.add_trace(
        go.Scatter(x=x, y=digital_with_noise, mode='lines', name='ノイズありの信号',
                  line=dict(color='red', width=1)),
        row=2, col=1
    )
    
    # Threshold line
    fig2.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5,
                   annotation_text="しきい値", row=2, col=1)
    
    # Restored digital
    fig2.add_trace(
        go.Scatter(x=x, y=digital_restored, mode='lines', name='復元された信号',
                  line=dict(color='green', width=2)),
        row=3, col=1
    )
    
    fig2.update_xaxes(title_text="時間", row=3, col=1)
    fig2.update_yaxes(title_text="振幅", range=[-2, 2])
    fig2.update_layout(
        height=650,
        showlegend=False,
        template='plotly_white',
        hovermode='x unified'
    )
    
    # Add success annotation for digital restoration
    if noise_level > 0:
        fig2.add_annotation(
            text="✅ 復元成功！",
            xref="paper", yref="paper",
            x=0.5, y=0.02, showarrow=False,
            font=dict(size=12, color="green")
        )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    if noise_level > 0:
        st.success("ある程度復元できた！ ✨")
        st.write("しきい値で0と1を判別できます")
    else:
        st.info("クリアなデジタル信号です")

st.info("""
**まとめ**: アナログは連続的な量なので、ノイズが混ざると元の情報と区別できません。
一方、デジタルは「0」か「1」かの不連続な量なので、多少ノイズが乗っても元の情報に復元できるのです。
""")

st.markdown("---")

# Content 2: Copy Degradation  
st.markdown("## 📠 体験2：繰り返しコピーするとどうなる？")
st.markdown("アナログコピーとデジタルコピー、どちらが劣化するか体験してみましょう！")

# Initialize session state for copy counts
if 'analog_copies' not in st.session_state:
    st.session_state.analog_copies = 0
if 'digital_copies' not in st.session_state:
    st.session_state.digital_copies = 0

# Add comparison metrics at the top
col_metric1, col_metric2, col_metric3 = st.columns(3)
with col_metric1:
    st.metric("📼 アナログコピー回数", st.session_state.analog_copies)
with col_metric2:
    st.metric("💾 デジタルコピー回数", st.session_state.digital_copies)
with col_metric3:
    degradation_rate = min(100, st.session_state.analog_copies * 2)
    st.metric("📉 アナログ劣化率", f"{degradation_rate}%")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📼 アナログコピー（カセットテープ）")
    if st.button("🔄 10回コピーする！", key="analog_copy"):
        st.session_state.analog_copies += 10
    
    st.write(f"コピー回数: {st.session_state.analog_copies}回")
    
    # Create original pattern
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + 0.5 * np.sin(3*x)
    
    # Add degradation based on copy count
    degradation = st.session_state.analog_copies * 0.01
    noise = np.random.normal(0, degradation, len(y))
    degraded_signal = y + noise
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=degraded_signal, mode='lines', name='信号',
                  line=dict(color='blue', width=2))
    )
    
    # Add quality indicator color based on degradation
    color = 'blue' if degradation < 0.3 else 'orange' if degradation < 0.6 else 'red'
    
    fig.update_layout(
        title=f'アナログ信号 (コピー{st.session_state.analog_copies}回)',
        xaxis_title="時間",
        yaxis_title="振幅",
        yaxis=dict(range=[-2, 2]),
        template='plotly_white',
        height=400,
        plot_bgcolor='rgba(255,0,0,0.05)' if degradation > 0.5 else 'rgba(255,255,0,0.05)' if degradation > 0.2 else 'rgba(0,255,0,0.05)'
    )
    
    # Update trace color
    fig.data[0].line.color = color
    
    # Add degradation annotation
    if degradation > 0:
        fig.add_annotation(
            text=f"劣化レベル: {int(degradation*100)}%",
            xref="paper", yref="paper",
            x=0.02, y=0.98, showarrow=False,
            font=dict(size=12, color=color),
            bgcolor="white", bordercolor=color, borderwidth=1
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.analog_copies > 50:
        st.error("かなり劣化しています... 😱")
    elif st.session_state.analog_copies > 20:
        st.warning("劣化が目立ってきました")
    elif st.session_state.analog_copies > 0:
        st.info("少し劣化しています")
    else:
        st.success("オリジナル品質")

with col2:
    st.markdown("### 💾 デジタルコピー（ファイル）")
    if st.button("🔄 10回コピーする！", key="digital_copy"):
        st.session_state.digital_copies += 10
    
    st.write(f"コピー回数: {st.session_state.digital_copies}回")
    
    # Digital signal never degrades
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + 0.5 * np.sin(3*x)
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=y, mode='lines', name='信号',
                  line=dict(color='green', width=2))
    )
    
    fig.update_layout(
        title=f'デジタル信号 (コピー{st.session_state.digital_copies}回)',
        xaxis_title="時間",
        yaxis_title="振幅",
        yaxis=dict(range=[-2, 2]),
        template='plotly_white',
        height=400,
        plot_bgcolor='rgba(0,255,0,0.05)'
    )
    
    # Add perfect quality annotation
    if st.session_state.digital_copies > 0:
        fig.add_annotation(
            text="✨ 完全品質維持",
            xref="paper", yref="paper",
            x=0.02, y=0.98, showarrow=False,
            font=dict(size=12, color="green"),
            bgcolor="white", bordercolor="green", borderwidth=1
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.digital_copies > 0:
        st.success("完全にオリジナル品質を維持！ ✨")
    else:
        st.info("オリジナル品質")

col_reset1, col_reset2 = st.columns(2)
with col_reset1:
    if st.button("🔄 アナログリセット", key="reset_analog"):
        st.session_state.analog_copies = 0
        st.rerun()
with col_reset2:
    if st.button("🔄 デジタルリセット", key="reset_digital"):
        st.session_state.digital_copies = 0
        st.rerun()

st.info("""
**まとめ**: アナログのコピーは「情報の複製」に必ず劣化が伴います。
デジタルのコピーは「0と1の完全な複製」なので、原理的に劣化しません。これがデジタルデータの大きな強みです。
""")

st.markdown("---")

# Content 3: Bit Representation
st.markdown("## 🔢 体験3：ビットの表現力を体験！")
st.markdown("「nビットで2のn乗通りの情報を表現できる」という原理を体験してみましょう！")

# Bit count slider
bit_count = st.slider("🔢 ビット数を選択", 1, 8, 3, key="bit_slider")

# Calculate possible combinations
combinations = 2 ** bit_count

# Enhanced bit representation display
st.markdown(f"### {bit_count}ビットのインタラクティブ表現")

# Interactive bit pattern generator
col_bit1, col_bit2 = st.columns([3, 1])

with col_bit1:
    # Show interactive bit icons
    bit_values = []
    bit_cols = st.columns(bit_count)
    
    for i in range(bit_count):
        with bit_cols[i]:
            bit_val = st.checkbox(f"Bit{i}", key=f"bit_{i}", help=f"ビット位置{i}")
            bit_values.append(bit_val)
    
    # Convert to binary representation
    binary_str = ''.join(['1' if b else '0' for b in bit_values])
    decimal_val = int(binary_str, 2) if binary_str else 0
    icon_repr = ' '.join(['💡' if b else '⚫' for b in bit_values])
    
    st.markdown(f"**選択中のパターン:** `{binary_str}` = {decimal_val}")
    st.markdown(f"**アイコン表示:** {icon_repr}")

with col_bit2:
    # Show binary counter
    if st.button("🔄 ランダム", help="ランダムパターン"):
        import random
        for i in range(bit_count):
            st.session_state[f"bit_{i}"] = random.choice([True, False])
        st.rerun()

# Show all possible combinations with enhanced display
st.markdown(f"**{bit_count}ビットでは 2^{bit_count} = {combinations} 通りの情報を区別できます**")

# Add interactive bit calculator with Plotly
bit_range = list(range(1, 9))
expression_counts = [2**i for i in bit_range]

fig_bits = go.Figure()
fig_bits.add_trace(
    go.Bar(x=bit_range, y=expression_counts, 
           name="表現可能数",
           marker_color='lightblue',
           text=expression_counts,
           textposition='auto')
)

# Highlight current selection
fig_bits.add_trace(
    go.Bar(x=[bit_count], y=[combinations],
           name="現在の選択",
           marker_color='red',
           text=[combinations],
           textposition='auto')
)

fig_bits.update_layout(
    title="🔢 ビット数と表現可能数の関係",
    xaxis_title="ビット数",
    yaxis_title="表現可能数 (2^n)",
    template='plotly_white',
    height=400,
    yaxis_type="log",
    showlegend=True
)

st.plotly_chart(fig_bits, use_container_width=True)

# Enhanced combination display
if bit_count <= 4:
    st.markdown("#### 全ての組み合わせ:")
    combinations_list = []
    for i in range(combinations):
        binary = format(i, f'0{bit_count}b')
        icon_repr = ' '.join(['💡' if b == '1' else '⚫' for b in binary])
        combinations_list.append(f"{binary} → {icon_repr}")
    
    # Display in columns with better formatting
    cols = st.columns(min(4, combinations))
    for i, combo in enumerate(combinations_list):
        with cols[i % len(cols)]:
            st.code(combo, language=None)
else:
    st.markdown("組み合わせが多すぎるので、いくつかの例を表示します:")
    
    # Add interactive selection for viewing specific combinations
    view_range = st.slider("表示範囲を選択", 0, max(0, combinations-8), 0, key="combo_range")
    
    for i in range(view_range, min(view_range + 8, combinations)):
        binary = format(i, f'0{bit_count}b')
        icon_repr = ' '.join(['💡' if b == '1' else '⚫' for b in binary])
        st.code(f"{i:3d}: {binary} → {icon_repr}", language=None)
    
    if combinations > view_range + 8:
        st.text(f"... あと{combinations - view_range - 8}個の組み合わせがあります")

# Enhanced application problem with visualization
st.markdown("### 🎯 応用問題：62文字を区別するには？")
st.markdown("アルファベット大文字(26) + 小文字(26) + 数字(10) = 合計62文字を区別するには、何ビット必要でしょう？")

target_chars = 62
required_bits = np.ceil(np.log2(target_chars)).astype(int)

col_app1, col_app2 = st.columns([2, 1])

with col_app1:
    if combinations >= target_chars:
        st.success(f"✅ {bit_count}ビット (2^{bit_count}={combinations}通り) あれば、{target_chars}文字を全部区別できる！")
    else:
        st.error(f"❌ {bit_count}ビット (2^{bit_count}={combinations}通り) では足りない！")
    
    st.info(f"💡 正解: {required_bits}ビット以上が必要です (2^{required_bits}={2**required_bits}通り)")

with col_app2:
    # Visual comparison chart
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(
        go.Bar(x=["必要数", "現在表現数"], 
               y=[target_chars, combinations],
               marker_color=['lightcoral' if combinations < target_chars else 'lightgreen', 
                            'lightblue'],
               text=[target_chars, combinations],
               textposition='auto')
    )
    
    fig_comparison.update_layout(
        title="必要数 vs 表現可能数",
        yaxis_title="文字数",
        template='plotly_white',
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

st.info("""
**まとめ**: コンピュータの世界では、全ての情報を「0」と「1」の組み合わせで表現しています。
ビット数が1つ増えるだけで、表現できる情報量は2倍になります。
""")

st.markdown("---")

# Additional creative content
st.markdown("## 🗜️ おまけ：データ圧縮の違いも体験！")
st.markdown("アナログとデジタルでは、データ圧縮の方法も違います")

show_comparison = st.toggle("🔄 同時比較表示", help="両方の圧縮方法を同時に比較表示します")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎵 アナログ圧縮（音質劣化）")
    quality = st.slider("音質レベル", 1, 10, 10, key="analog_quality")

# Simulate audio waveform
x_audio = np.linspace(0, 2*np.pi, 1000)
original_wave = np.sin(5*x_audio) + 0.3*np.sin(15*x_audio) + 0.2*np.sin(30*x_audio)

# Simulate quality loss
compression_factor = quality / 10
compressed_wave = original_wave * compression_factor + np.random.normal(0, (10-quality)*0.01, len(original_wave))

with col1:
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x_audio, y=compressed_wave, mode='lines', name='音声波形',
                  line=dict(color='blue', width=2), opacity=0.8)
    )
    
    fig.update_layout(
        title=f'アナログ音質レベル: {quality}/10',
        xaxis_title="時間",
        yaxis_title="振幅",
        yaxis=dict(range=[-2, 2]),
        template='plotly_white',
        height=300,
        plot_bgcolor='rgba(255,0,0,0.1)' if quality < 5 else 'rgba(0,255,0,0.1)'
    )
    
    # Add quality annotations
    quality_text = "高音質" if quality >= 8 else "普通" if quality >= 5 else "低音質"
    quality_color = "green" if quality >= 8 else "orange" if quality >= 5 else "red"
    
    fig.add_annotation(
        text=f"📊 {quality_text}",
        xref="paper", yref="paper",
        x=0.02, y=0.98, showarrow=False,
        font=dict(size=12, color=quality_color),
        bgcolor="white", bordercolor=quality_color, borderwidth=1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if quality < 5:
        st.warning("音質が劣化しています")
    else:
        st.success("高音質です")

with col2:
    st.markdown("### 💻 デジタル圧縮（可逆/非可逆）")
    compression_type = st.selectbox("圧縮タイプ", ["無圧縮", "可逆圧縮", "非可逆圧縮"], key="digital_compression")

# Simulate data size
original_size = 1000
if compression_type == "無圧縮":
    compressed_size = original_size
    quality_loss = 0
elif compression_type == "可逆圧縮":
    compressed_size = int(original_size * 0.7)
    quality_loss = 0
else:  # 非可逆圧縮
    compressed_size = int(original_size * 0.3)
    quality_loss = 0.1

# Show data representation
x = np.linspace(0, 2*np.pi, 100 if compression_type != "非可逆圧縮" else 30)
y = np.sin(5*x) + 0.3*np.sin(15*x) + 0.2*np.sin(30*x)

if compression_type == "非可逆圧縮":
    y = y + np.random.normal(0, quality_loss, len(y))

# Create Plotly figure
with col2:
    fig = go.Figure()
    
    if len(x) < 50:
        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines+markers', name='データ',
                      line=dict(color='green', width=2), 
                      marker=dict(size=4), opacity=0.8)
        )
    else:
        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines', name='データ',
                      line=dict(color='green', width=2), opacity=0.8)
        )
    
    fig.update_layout(
        title=f'デジタル圧縮: {compression_type}',
        xaxis_title="時間",
        yaxis_title="振幅",
        yaxis=dict(range=[-2, 2]),
        template='plotly_white',
        height=300,
        plot_bgcolor='rgba(0,255,0,0.1)' if compression_type in ["無圧縮", "可逆圧縮"] else 'rgba(255,255,0,0.1)'
    )
    
    # Add compression info
    compression_info = {
        "無圧縮": "🔵 最高品質",
        "可逆圧縮": "🟢 品質維持+圧縮", 
        "非可逆圧縮": "🟡 高圧縮率"
    }
    
    fig.add_annotation(
        text=compression_info[compression_type],
        xref="paper", yref="paper",
        x=0.02, y=0.98, showarrow=False,
        font=dict(size=12),
        bgcolor="white", bordercolor="gray", borderwidth=1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.metric("データサイズ", f"{compressed_size} KB", f"{compressed_size - original_size} KB")
    
    if compression_type == "可逆圧縮":
        st.success("サイズ削減 + 品質維持 ✨")
    elif compression_type == "非可逆圧縮":
        st.info("大幅サイズ削減（品質は少し犠牲）")
    else:
        st.info("最高品質")

# Enhanced comparison view
if show_comparison:
    st.markdown("### 📊 圧縮方式の直接比較")
    
    # Comparison chart
    quality_rates = {"無圧縮": 100, "可逆圧縮": 100, "非可逆圧縮": 90}
    size_rates = {"無圧縮": 1000, "可逆圧縮": 700, "非可逆圧縮": 300}
    
    fig_comp = go.Figure()
    
    fig_comp.add_trace(
        go.Scatter(x=[quality*10, quality_rates[compression_type]], 
                  y=[1000 - (10-quality)*50, size_rates[compression_type]],
                  mode='markers+text',
                  text=['アナログ', 'デジタル'],
                  textposition='top center',
                  marker=dict(size=15, color=['red', 'blue']),
                  name='圧縮比較')
    )
    
    fig_comp.update_layout(
        title="🔄 品質 vs ファイルサイズ比較",
        xaxis_title="品質保持率 (%)",
        yaxis_title="ファイルサイズ (KB)",
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Final summary with interactive elements
st.markdown("## 🎓 学習のまとめ")

# Create an interactive summary chart using bar chart instead of radar
categories = ['ノイズ耐性', 'コピー耐性', '圧縮効率']
analog_scores = [2, 1, 2]  # Lower scores for analog
digital_scores = [5, 5, 4]  # Higher scores for digital

fig_summary = go.Figure()

fig_summary.add_trace(
    go.Bar(x=categories, y=analog_scores, 
           name='アナログ',
           marker_color='rgba(255,0,0,0.6)',
           text=analog_scores,
           textposition='auto')
)

fig_summary.add_trace(
    go.Bar(x=categories, y=digital_scores,
           name='デジタル', 
           marker_color='rgba(0,0,255,0.6)',
           text=digital_scores,
           textposition='auto')
)

fig_summary.update_layout(
    title="📊 アナログ vs デジタル 総合比較",
    xaxis_title="比較項目",
    yaxis_title="スコア (1-5)",
    yaxis=dict(range=[0, 5]),
    template='plotly_white',
    height=500,
    showlegend=True,
    barmode='group'
)

st.plotly_chart(fig_summary, use_container_width=True)

st.markdown("""
#### 🔑 重要なポイント
1. **ノイズ耐性**: デジタルは0と1の判別ができるため、アナログより強い
2. **コピー耐性**: デジタルは完全複製、アナログは劣化する  
3. **圧縮**: アナログは品質劣化、デジタルは可逆圧縮も可能

🌟 これらの違いを理解することで、なぜ現代社会でデジタル技術が重要なのかが分かりますね！
""")

# Final interactive element
st.markdown("---")
if st.button("🎉 学習完了！理解度をチェックしましょう！", type="primary"):
    st.balloons()
    st.success("🎊 素晴らしい！アナログとデジタルの違いについて学習が完了しました！ 🎊")
    st.markdown("今日学んだことを他の人にも教えてあげてくださいね！")