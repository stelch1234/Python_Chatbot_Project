#costarica 변수 중에서 교육/집에 관한 부분만 집중적으로 볼 예정입니다.

import numpy as np
import pandas as pd

# 시각화
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import tools
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
train = pd.read_csv('/Users/stella/Downloads/파일럿 프로젝트/코스타리카 데이터 셋/train.csv')
test = pd.read_csv('/Users/stella/Downloads/파일럿 프로젝트/코스타리카 데이터 셋/test.csv')


# 데이터셋 기본 정보 보기
train.head()
train.info()
test.info()


# 변수들을 categorical / numerical 나누기
categorical = []
numerical = []

for feature in test.columns :
    if test[feature].dtype == object:
        categorical.append(feature)
    else :
        numerical.append(feature)

train[categorical].head()
## -> 2개의 컬럼(ID/idhogar) 3개의 컬림이 categorical로 발견되었습니다.
##    하지만, 3개의 컬럼 속에는 문자 NO/YES가 속해 있어 이를 각각 0과 1로 변환하겠습니다.


# 먼저 numerical 변수 null값을 확인
train[numerical].isnull().sum().sort_values(ascending=False).head(7)
test[numerical].isnull().sum().sort_values(ascending=False).head(7)
## -> rez_esc / v18q1 / v2a1 / meaneduc / SQBmeaned 순으로 null값이 확인 되었습니다.

# 결측값 처리
train['meaneduc'].fillna(train['meaneduc'].mean(), inplace = True)
test['meaneduc'].fillna(train['meaneduc'].mean(), inplace = True)

train['SQBmeaned'].fillna(train['SQBmeaned'].mean(), inplace = True)
test['SQBmeaned'].fillna(test['SQBmeaned'].mean(), inplace = True)

train['rez_esc'].fillna(0, inplace = True)
test['rez_esc'].fillna(0, inplace = True)

train['v18q1'].fillna(0, inplace = True)
test['v18q1'].fillna(0, inplace = True)

# 타켓변수인 빈곤 수준 파악 ? ? 문제 발생
#index = {4: "NonVulnerable", 3: "Moderate Poverty", 2: "Vulnerable", 1: "Extereme Poverty"}
#target_values = train['Target'].value_counts()
#target_values['Household_level'] = target_values.Household_level.map(index)


# 빈곤 수준 파악
poverty_label_sizes = list(train.groupby('Target').size())

def barplot_with_anotate(feature_list, y_values, plotting_space = plt, annotate_vals=None) :
    x_pos = np.arange(len(feature_list))
    plotting_space.bar(x_pos, y_values);
    plotting_space.xticks(x_pos, feature_list, rotation=270);
    if annotate_vals == None:
        annotate_vals = y_values
    for i in range(len(feature_list)):
        plotting_space.text(x=x_pos[i]-0.3, y=y_values[i]+1.0, s= annotate_vals[i]);

barplot_with_anotate([ 'NonVulnerable', 'Vulnerable', 'Moderate Poverty', 'Extreme Poverty'], poverty_label_sizes,
                     annotate_vals= [str(round((count/train.shape[0])*100,2))+ '%'
                                     for count in poverty_label_sizes]);
plt.rcParams['figure.figsize'] = [6,6];
plt.xlabel('Poverty Label');
plt.ylabel('No of People');

# 하우스
# 하우스 렌탈비용 전처리
train[['v2a1', 'tipovivi3']][train['tipovivi3'] == 0][train['v2a1'].isnull()].shape
train[:'v2a1'].fillna(0, inplace = True)

# 개인당 렌탈 비용