import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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
with st.expander("体験1：ノイズに強いのはどっち？ 🤔", expanded=True):
    st.markdown("### アナログ信号とデジタル信号、どちらがノイズに強いか体験してみましょう！")
    
    # Noise level slider
    noise_level = st.slider("ノイズの量を調整", 0, 100, 0, key="noise_slider")
    
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
        st.markdown("#### アナログ信号 📻")
        fig1, ax1 = plt.subplots(2, 1, figsize=(8, 6))
        
        # Original analog
        ax1[0].plot(x, analog_signal, 'b-', linewidth=2, label='元の信号')
        ax1[0].set_title('元のアナログ信号')
        ax1[0].set_ylim(-2, 2)
        ax1[0].grid(True, alpha=0.3)
        
        # Noisy analog
        ax1[1].plot(x, analog_with_noise, 'r-', linewidth=1, label='ノイズありの信号')
        if noise_level > 0:
            ax1[1].plot(x, analog_signal, 'b--', alpha=0.5, linewidth=1, label='元の信号')
        ax1[1].set_title('ノイズが加わった信号')
        ax1[1].set_ylim(-2, 2)
        ax1[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig1)
        
        if noise_level > 30:
            st.error("復元が難しい... 😵")
            st.write("ノイズと元の信号を区別できません")
        elif noise_level > 0:
            st.warning("復元が困難になってきています")
        else:
            st.success("クリアな信号です！")
    
    with col2:
        st.markdown("#### デジタル信号 💻")
        fig2, ax2 = plt.subplots(3, 1, figsize=(8, 8))
        
        # Original digital
        ax2[0].plot(x, digital_signal, 'g-', linewidth=2, label='元の信号')
        ax2[0].set_title('元のデジタル信号')
        ax2[0].set_ylim(-2, 2)
        ax2[0].grid(True, alpha=0.3)
        
        # Noisy digital
        ax2[1].plot(x, digital_with_noise, 'r-', linewidth=1, label='ノイズありの信号')
        ax2[1].axhline(y=0, color='black', linestyle='--', alpha=0.5, label='しきい値')
        ax2[1].set_title('ノイズが加わった信号')
        ax2[1].set_ylim(-2, 2)
        ax2[1].grid(True, alpha=0.3)
        
        # Restored digital
        ax2[2].plot(x, digital_restored, 'g-', linewidth=2, label='復元された信号')
        ax2[2].set_title('復元された信号')
        ax2[2].set_ylim(-2, 2)
        ax2[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig2)
        
        if noise_level > 0:
            st.success("完全に復元できた！ ✨")
            st.write("しきい値で0と1を判別できます")
        else:
            st.info("クリアなデジタル信号です")
    
    st.markdown("""
    **まとめ**: アナログは連続的な量なので、ノイズが混ざると元の情報と区別できません。
    一方、デジタルは「0」か「1」かの不連続な量なので、多少ノイズが乗っても元の情報に復元できるのです。
    """)

# Content 2: Copy Degradation
with st.expander("体験2：繰り返しコピーするとどうなる？ 📠"):
    st.markdown("### アナログコピーとデジタルコピー、どちらが劣化するか体験してみましょう！")
    
    # Initialize session state for copy counts
    if 'analog_copies' not in st.session_state:
        st.session_state.analog_copies = 0
    if 'digital_copies' not in st.session_state:
        st.session_state.digital_copies = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### アナログコピー（カセットテープ） 📼")
        if st.button("10回コピーする！", key="analog_copy"):
            st.session_state.analog_copies += 10
        
        st.write(f"コピー回数: {st.session_state.analog_copies}回")
        
        # Create a simple image that gets degraded
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Create original pattern
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + 0.5 * np.sin(3*x)
        
        # Add degradation based on copy count
        degradation = st.session_state.analog_copies * 0.01
        noise = np.random.normal(0, degradation, len(y))
        degraded_signal = y + noise
        
        ax.plot(x, degraded_signal, 'b-', linewidth=2)
        ax.set_title(f'アナログ信号 (コピー{st.session_state.analog_copies}回)')
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        if st.session_state.analog_copies > 50:
            st.error("かなり劣化しています... 😱")
        elif st.session_state.analog_copies > 20:
            st.warning("劣化が目立ってきました")
        elif st.session_state.analog_copies > 0:
            st.info("少し劣化しています")
        else:
            st.success("オリジナル品質")
    
    with col2:
        st.markdown("#### デジタルコピー（ファイル） 💾")
        if st.button("10回コピーする！", key="digital_copy"):
            st.session_state.digital_copies += 10
        
        st.write(f"コピー回数: {st.session_state.digital_copies}回")
        
        # Digital signal never degrades
        fig, ax = plt.subplots(figsize=(6, 4))
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + 0.5 * np.sin(3*x)
        
        ax.plot(x, y, 'g-', linewidth=2)
        ax.set_title(f'デジタル信号 (コピー{st.session_state.digital_copies}回)')
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        if st.session_state.digital_copies > 0:
            st.success("完全にオリジナル品質を維持！ ✨")
        else:
            st.info("オリジナル品質")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("リセット", key="reset_analog"):
            st.session_state.analog_copies = 0
            st.rerun()
    with col2:
        if st.button("リセット", key="reset_digital"):
            st.session_state.digital_copies = 0
            st.rerun()
    
    st.markdown("""
    **まとめ**: アナログのコピーは「情報の複製」に必ず劣化が伴います。
    デジタルのコピーは「0と1の完全な複製」なので、原理的に劣化しません。これがデジタルデータの大きな強みです。
    """)

# Content 3: Bit Representation
with st.expander("体験3：ビットの表現力を体験！ 🔢"):
    st.markdown("### 「nビットで2のn乗通りの情報を表現できる」という原理を体験してみましょう！")
    
    # Bit count slider
    bit_count = st.slider("ビット数を選択", 1, 8, 3, key="bit_slider")
    
    # Calculate possible combinations
    combinations = 2 ** bit_count
    
    # Display bit representation
    st.markdown(f"#### {bit_count}ビットの表現")
    
    # Show bit icons
    bit_icons = []
    for i in range(bit_count):
        bit_icons.append("⚫" if i % 2 == 0 else "💡")
    
    st.markdown(f"ビット表現例: {' '.join(bit_icons)}")
    
    # Show all possible combinations
    st.markdown(f"**{bit_count}ビットでは 2^{bit_count} = {combinations} 通りの情報を区別できます**")
    
    # Show some examples of combinations
    if bit_count <= 4:
        st.markdown("##### 全ての組み合わせ:")
        combinations_list = []
        for i in range(combinations):
            binary = format(i, f'0{bit_count}b')
            icon_repr = ' '.join(['💡' if b == '1' else '⚫' for b in binary])
            combinations_list.append(f"{binary} → {icon_repr}")
        
        # Display in columns
        cols = st.columns(min(4, combinations))
        for i, combo in enumerate(combinations_list):
            with cols[i % len(cols)]:
                st.text(combo)
    else:
        st.markdown("組み合わせが多すぎるので、いくつかの例を表示します:")
        for i in range(min(8, combinations)):
            binary = format(i, f'0{bit_count}b')
            icon_repr = ' '.join(['💡' if b == '1' else '⚫' for b in binary])
            st.text(f"{binary} → {icon_repr}")
        if combinations > 8:
            st.text("...")
    
    # Application problem
    st.markdown("#### 応用問題")
    st.markdown("アルファベット大文字(26) + 小文字(26) + 数字(10) = 合計62文字を区別するには、何ビット必要でしょう？")
    
    target_chars = 62
    required_bits = np.ceil(np.log2(target_chars)).astype(int)
    
    if combinations >= target_chars:
        st.success(f"✅ {bit_count}ビット (2^{bit_count}={combinations}通り) あれば、{target_chars}文字を全部区別できる！")
    else:
        st.error(f"❌ {bit_count}ビット (2^{bit_count}={combinations}通り) では足りない！")
    
    st.info(f"正解: {required_bits}ビット以上が必要です (2^{required_bits}={2**required_bits}通り)")
    
    st.markdown("""
    **まとめ**: コンピュータの世界では、全ての情報を「0」と「1」の組み合わせで表現しています。
    ビット数が1つ増えるだけで、表現できる情報量は2倍になります。
    """)

# Additional creative content
with st.expander("おまけ：データ圧縮の違いも体験！ 🗜️"):
    st.markdown("### アナログとデジタルでは、データ圧縮の方法も違います")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### アナログ圧縮（音質劣化）")
        quality = st.slider("音質レベル", 1, 10, 10, key="analog_quality")
        
        # Simulate audio waveform
        x = np.linspace(0, 2*np.pi, 1000)
        original_wave = np.sin(5*x) + 0.3*np.sin(15*x) + 0.2*np.sin(30*x)
        
        # Simulate quality loss
        compression_factor = quality / 10
        compressed_wave = original_wave * compression_factor + np.random.normal(0, (10-quality)*0.01, len(original_wave))
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, compressed_wave, 'b-', alpha=0.8)
        ax.set_title(f'アナログ音質レベル: {quality}/10')
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        if quality < 5:
            st.warning("音質が劣化しています")
        else:
            st.success("高音質です")
    
    with col2:
        st.markdown("#### デジタル圧縮（可逆/非可逆）")
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
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.linspace(0, 2*np.pi, 100 if compression_type != "非可逆圧縮" else 30)
        y = np.sin(5*x) + 0.3*np.sin(15*x) + 0.2*np.sin(30*x)
        
        if compression_type == "非可逆圧縮":
            y = y + np.random.normal(0, quality_loss, len(y))
        
        ax.plot(x, y, 'g-', marker='o' if len(x) < 50 else '', alpha=0.8)
        ax.set_title(f'デジタル圧縮: {compression_type}')
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.metric("データサイズ", f"{compressed_size} KB", f"{compressed_size - original_size} KB")
        
        if compression_type == "可逆圧縮":
            st.success("サイズ削減 + 品質維持 ✨")
        elif compression_type == "非可逆圧縮":
            st.info("大幅サイズ削減（品質は少し犠牲）")
        else:
            st.info("最高品質")

st.markdown("---")
st.markdown("### 🎓 学習のまとめ")
st.markdown("""
1. **ノイズ耐性**: デジタルは0と1の判別ができるため、アナログより強い
2. **コピー耐性**: デジタルは完全複製、アナログは劣化する
3. **表現力**: nビットで2^n通りの情報を表現可能
4. **圧縮**: アナログは品質劣化、デジタルは可逆圧縮も可能

これらの違いを理解することで、なぜ現代社会でデジタル技術が重要なのかが分かりますね！
""")