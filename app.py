import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import os
import urllib.request
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib import font_manager, rc

app = Flask(__name__)
CORS(app)

# 1. 한글 폰트 설정
def set_korean_font_robust():
    font_filename = "NanumGothic.ttf"
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    if not os.path.exists(font_filename):
        try:
            urllib.request.urlretrieve(font_url, font_filename)
        except:
            return
    try:
        font_manager.fontManager.addfont(font_filename) 
        rc('font', family='NanumGothic') 
    except:
        pass
    plt.rcParams['axes.unicode_minus'] = False 

set_korean_font_robust()

# 2. 국가명 한글 매핑
COUNTRY_KO = {
    'Germany': '독일', 'France': '프랑스', 'Netherlands': '네덜란드', 'Italy': '이탈리아',
    'Spain': '스페인', 'Sweden': '스웨덴', 'Norway': '노르웨이', 'Poland': '폴란드',
    'Turkey': '튀르키예', 'United Kingdom': '영국', 'United States': '미국', 'Canada': '캐나다',
    'Brazil': '브라질', 'India': '인도', 'China': '중국', 'Japan': '일본',
    'Australia': '호주', 'South Africa': '남아공', 'Mexico': '멕시코', 'Indonesia': '인도네시아'
}

@app.route('/')
def home():
    try:
        with open('index.html', 'r', encoding='utf-8') as f: return f.read()
    except: return "index.html 파일이 없습니다."

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files: return jsonify({'error': "파일 없음"}), 400
        file = request.files['file']
        k = int(request.form.get('k', 4))

        try: df = pd.read_csv(file, encoding='utf-8')
        except: 
            file.seek(0)
            df = pd.read_csv(file, encoding='cp949')

        numeric_cols = ['avg_temperature', 'co2_emission', 'energy_consumption', 'renewable_share', 'industrial_activity_index', 'energy_price']
        df_clean = df.dropna(subset=numeric_cols + ['country'])
        df_grouped = df_clean.groupby('country')[numeric_cols].mean()

        # 파생변수
        df_grouped['energy_efficiency'] = (df_grouped['industrial_activity_index'] / df_grouped['energy_consumption']) * 1000
        df_grouped = df_grouped.replace([np.inf, -np.inf], np.nan).dropna()

        # 클러스터링
        X = df_grouped[['co2_emission', 'energy_efficiency', 'renewable_share', 'energy_price']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        df_grouped['Cluster'] = clusters

        avg_eff = df_grouped['energy_efficiency'].median()
        avg_co2 = df_grouped['co2_emission'].median()

        FIXED_COLORS = ['#198754', '#0d6efd', '#dc3545', '#6f42c1', '#fd7e14', '#20c997']
        
        summary_dict = []
        cluster_info = {}

        for cluster_id in range(k):
            sub_df = df_grouped[df_grouped['Cluster'] == cluster_id]
            if sub_df.empty: continue

            stats = sub_df.mean()
            eff, co2 = stats['energy_efficiency'], stats['co2_emission']
            
            # [핵심] 유형별 개선 계획(Advice) 생성 로직
            if eff > avg_eff and co2 < avg_co2:
                base_label = "친환경 선도형"
                desc = "높은 효율과 낮은 탄소 배출을 달성한 이상적인 그룹"
                advice = "현재의 정책 기조를 유지하며, 보유한 저탄소 기술을 타 국가에 수출하여 글로벌 리더십을 강화하십시오. R&D 투자를 통해 초격차 기술을 확보해야 합니다."
            elif eff <= avg_eff and co2 < avg_co2:
                base_label = "청정 개발형"
                desc = "탄소 배출은 적지만, 산업 효율화가 필요한 그룹"
                advice = "산업 인프라의 현대화가 시급합니다. 스마트 그리드 도입과 에너지 관리 시스템(EMS) 구축을 통해 에너지 효율을 높이는 데 투자를 집중하십시오."
            elif eff <= avg_eff and co2 >= avg_co2:
                base_label = "에너지 위기형"
                desc = "낮은 효율과 많은 탄소 배출로 개선이 시급한 그룹"
                advice = "🚨 긴급 조치가 필요합니다. 노후 석탄 발전소를 단계적으로 폐쇄하고, 재생에너지 비율을 법적으로 강제하는 강력한 규제와 인센티브 정책을 동시에 시행해야 합니다."
            else:
                base_label = "고성장 산업형"
                desc = "산업 역량은 높지만 탄소 감축 노력이 필요한 그룹"
                advice = "산업 경쟁력은 우수하나 탄소 비용이 리스크가 될 수 있습니다. CCUS(탄소 포집) 기술 도입과 공장 에너지 효율화 프로젝트를 통해 탄소 발자국을 줄이십시오."

            color = FIXED_COLORS[cluster_id % len(FIXED_COLORS)]
            final_label = f"{base_label} (G{cluster_id+1})"

            ko_countries = [COUNTRY_KO.get(c, c) for c in sub_df.index]
            c_str = ", ".join(ko_countries)

            cluster_info[cluster_id] = {'label': final_label, 'color': color, 'data': sub_df, 'ko_names': ko_countries}

            detail_html = f"""
            <div class='alert' style='background-color:{color}15; border-left: 5px solid {color};'>
                <h5 style='color:{color}'><strong>{final_label}</strong></h5>
                <p>{desc}</p>
                <hr>
                <ul class='list-unstyled'>
                    <li>📊 <strong>효율성 점수:</strong> {eff:.2f} <small class='text-muted'>(중앙값 {avg_eff:.2f})</small></li>
                    <li>☁️ <strong>CO2 배출량:</strong> {co2:.1f} <small class='text-muted'>(중앙값 {avg_co2:.1f})</small></li>
                    <li>💰 <strong>평균 에너지 가격:</strong> € {stats['energy_price']:.1f}</li>
                </ul>
                <div class='mt-3'><strong>🌍 포함 국가:</strong><br>{c_str}</div>
            </div>
            """

            summary_dict.append({
                'cluster': int(cluster_id),
                'label': final_label,
                'explanation': desc,
                'advice': advice, # [추가] 조언 데이터 전달
                'reason_detail': detail_html,
                'countries': c_str,
                'count': len(sub_df),
                'co2': round(stats['co2_emission'], 1),
                'renewable': round(stats['renewable_share'], 1),
                'industry': round(stats['industrial_activity_index'], 1), 
                'price': round(stats['energy_price'], 1),
                'color': color 
            })

        # 그래프 생성 (8 x 5.5, dpi 150)
        fig = plt.figure(figsize=(8, 5.5), dpi=300)
        ax = fig.add_subplot(111, projection='3d')

        for cid, info in cluster_info.items():
            sub_data = info['data']
            ax.scatter(
                sub_data['energy_efficiency'], sub_data['co2_emission'], sub_data['renewable_share'],
                c=info['color'], label=info['label'], s=100, alpha=0.9, edgecolors='white', linewidth=1.0
            )
            for idx, (country, row) in enumerate(sub_data.iterrows()):
                ko_name = COUNTRY_KO.get(country, country)
                ax.text(
                    row['energy_efficiency'], row['co2_emission'], row['renewable_share'], 
                    ko_name, fontsize=8, fontweight='bold', zorder=10
                )

        ax.set_xlabel('에너지 효율성', fontsize=9, labelpad=5)
        ax.set_ylabel('CO2 배출량', fontsize=9, labelpad=5)
        ax.set_zlabel('재생에너지 비중', fontsize=9, labelpad=5)
        ax.set_title(f'국가별 에너지/기후 클러스터링 (K={k})', fontsize=12, fontweight='bold', pad=10)
        ax.view_init(elev=25, azim=135)
        plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left', fontsize=9)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return jsonify({'message': 'Success', 'image': f'data:image/png;base64,{plot_url}', 'summary': summary_dict})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)