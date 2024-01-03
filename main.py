import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

criteria_labels = np.array(['benefit', 'benefit', 'benefit', 'cost', 'benefit'])

weights = np.array([0.3, 0.1, 0.3, 0.1, 0.2])

framework_options = ['Laravel', 'Django', 'Rubby on Rails', 'Spring Boots', 'Express', 'Flask', 'Koa.js']


def click_button():
    st.session_state.clicked = True

def normalize_values(values, labels):
    if not values.shape[1] == len(labels):
        st.write('Jumlah kriteria dan label tidak sama')
        return None

    normalized_all = []

    for i in range(values.shape[0]):
        normalized_value = []
        max_val = np.max(values[i])
        min_val = np.min(values[i])

        # Menangani kasus di mana nilai maksimum dan minimum sama
        if max_val == min_val:
            for j in range(values.shape[1]):
                normalized_value.append(1.0)  # Atau sesuaikan dengan nilai default yang sesuai
        else:
            # Modifikasi nilai minimum untuk menghindari nilai normalisasi menjadi 0
            min_val = min_val - 0.01

            for j in range(values.shape[1]):
                if labels[j] == 'benefit':
                    norm_c = (values[i][j] - min_val) / (max_val - min_val)
                elif labels[j] == 'cost':
                    norm_c = (min_val - values[i][j]) / (min_val - max_val)
                normalized_value.append(norm_c)

        normalized_all.append(normalized_value)

    return np.array(normalized_all)


def calculate_saw(values, weights):
    if not values.shape[1] == weights.shape[0]:
        st.write('Jumlah kriteria dan bobot tidak sama')
        return None

    alt_crit_value = []

    for i in range(values.shape[0]):
        val = np.sum(values[i] * weights.T)
        alt_crit_value.append(val)

    return alt_crit_value


def ranking(vector):
    ranks = len(vector) - vector.argsort().argsort()
    return ranks


def run():
    st.set_page_config(
        page_title="Implementasi SAW",
        page_icon="💻",
    )

    st.write("# Implementasi Metode SAW untuk Memilih Framework")
    st.write("Dikembangkan oleh Martio Husein Samsu untuk keperluan tugas UAS")

    st.markdown(
        """
          Metode SAW (Simple Additive Weighting) adalah salah satu metode
          pemilihan alternatif dalam pengambilan keputusan multi-kriteria.
          Metode ini mengubah masalah pengambilan keputusan menjadi proses
          penjumlahan hasil dari kriteria yang telah dinormalisasi dan dibobotkan.
          Kriteria dalam metode SAW memiliki bobot relatif yang mewakili tingkat
          kepentingan relatif dari setiap kriteria dalam pengambilan keputusan.
        """
    )

    st.markdown(
        """
        **Studi Kasus: Pemilihan Framework Untuk Proyek Pengembangan Perangkat Lunak**

        Dalam konteks ini, tim pengembangan IT sedang mencari framework yang sesuai
        untuk proyek pengembangan perangkat lunak. Kriteria seleksi yang dipertimbangkan
        adalah sebagai berikut:

        - Ketersediaan dokumentasi (C1), semakin lengkap dan jelas dokumentasinya semakin baik
        - Komunitas pengguna (C2), semakin besar komunitas pengguna semakin baik
        - Kelengkapan fitur (C3), semakin lengkap fitur yang disediakan semakin baik
        - Pembaharuan Framework (C4), Semakin sedikit adanya pembaharuan semakin baik.
        - Kinerja (C5), semakin baik kinerja dari framework semakin baik.
        """
    )

    st.divider()

    selected_framework = st.selectbox("Pilih Framework", framework_options)

    st.write("## Input Nilai Kriteria")

    c1 = st.slider("Nilai C1 - Ketersediaan Dokumentasi", min_value=1, max_value=5, value=1, step=1) / 10
    c2 = st.slider("Nilai C2 - Komunitas Pengguna", min_value=1, max_value=5, value=1, step=1) / 10
    c3 = st.slider("Nilai C3 - Pembaharuan Framework", min_value=1, max_value=5, value=1, step=1) / 10
    c4 = st.slider("Nilai C4 - Ketersediaan Dukungan", min_value=1, max_value=5, value=1, step=1) / 10
    c5 = st.slider("Nilai C5 - Kinerja", min_value=1, max_value=5, value=1, step=1) / 10

    if st.button("Simpan", type='primary', on_click=click_button):
        save_data(c1, c2, c3, c4, c5, selected_framework)

    if st.session_state.clicked:
        data = st.session_state.nilai_kriteria
        df = pd.DataFrame(data, columns=('C1', 'C2', 'C3', 'C4', 'C5'))
        df.index += 1
        st.dataframe(df)

        if st.button("Proses"):
            process_data()


def save_data(c1, c2, c3, c4, c5, selected_framework):
    if 'nilai_kriteria' not in st.session_state:
        st.session_state.nilai_kriteria = np.array([[c1, c2, c3, c4, c5]])
        st.session_state.frameworks = np.array([selected_framework])
    else:
        dataLama = st.session_state.nilai_kriteria
        dataBaru = np.append(dataLama, [[c1, c2, c3, c4, c5]], axis=0)
        st.session_state.nilai_kriteria = dataBaru

        frameworks = st.session_state.frameworks
        frameworksBaru = np.append(frameworks, [selected_framework], axis=0)
        st.session_state.frameworks = frameworksBaru


def process_data():
    A = st.session_state.nilai_kriteria
    frameworks = st.session_state.frameworks

    norm_a = normalize_values(A, criteria_labels)
    saw = calculate_saw(norm_a, weights)
    rank = ranking(np.asarray(saw))

    st.write("Nilai alternatif:")
    df_values = pd.DataFrame(A, columns=['C1', 'C2', 'C3', 'C4', 'C5'])
    df_values['Framework'] = frameworks  
    df_values.index += 1  
    st.dataframe(df_values)

    st.write("Normalisasi nilai alternatif:")
    df_norm_values = pd.DataFrame(norm_a, columns=['C1', 'C2', 'C3', 'C4', 'C5'])
    df_norm_values.index += 1 
    st.dataframe(df_norm_values)

    st.write("Perhitungan nilai SAW:")
    df_saw = pd.DataFrame({'Alternatif': range(1, len(saw) + 1), 'Nilai SAW': saw})
    df_saw['Framework'] = frameworks  
    df_saw.index += 1 
    st.table(df_saw)

    st.write("Perankingan:")
    df_rank = pd.DataFrame({'Alternatif': range(1, len(rank) + 1), 'Peringkat': rank})
    df_rank['Framework'] = frameworks  

    df_rank_sorted = df_rank.sort_values(by='Peringkat').reset_index(drop=True)
    df_rank_sorted.index += 1  
    df_rank_sorted.rename_axis('Alternatif', inplace=True)  
    st.table(df_rank_sorted)

if __name__ == "__main__":
    run()

