---
title: 2019 Obesity (Fabio Mendoza Palechor et. al) 資料集備忘錄
---


# 元資料

- 用途描述：藉由飲食習慣與身體狀況預測肥胖等級
- 資料來源地理區域：歌倫比亞、秘魯、墨西哥
- 資料來源：[UCI dataset - Estimation of obesity levels based on eating habits and physical condition Data Set][source]
- 捐贈日期：2019-08-27
- 紀錄筆數：2111 筆，其中 498 筆為真人填寫之網路問卷（～23% ）、1613 筆為 SMOTE 演算法人工合成之資料（～77% ）
- 缺失值：（無）


# 資料欄位（翻譯）

| 欄位名稱                     | 中文翻譯                |資料型態或選項|
|:-----------------------------|:------------------------|:------------:|
|Gender                        | 性別                    | {Female,Male}
|Age                           | 年齡                    | numeric
|Height                        | 身高                    | numeric
|Weight                        | 體重                    | numeric
|family_history_with_overweight| 家族過重病史            | {yes,no}
|FAVC                          | 經常食用高卡路里食物    | {yes,no}
|FCVC                          | 食用蔬菜的頻率          | numeric
|NCP                           | 每日正餐數              | numeric
|CAEC                          | 正餐間飲食              | {no,Sometimes,Frequently,Always}
|SMOKE                         | 有無吸煙習慣            | {yes,no}
|CH2O                          | 每日飲水量              | numeric
|SCC                           | 有無紀錄攝取卡路里的習慣| {yes,no}
|FAF                           | 運動頻率                | numeric
|TUE                           | 花在 3C 產品上的時間    | numeric
|CALC                          | 飲酒量                  | {no,Sometimes,Frequently,Always}
|MTRANS                        | 交通方式                | {Automobile,Motorbike,Bike,Public_Transportation,Walking}
|NObeyesdad                    | BMI 評價                | {Insufficient_Weight,Normal_Weight,Overweight_Level_I,Overweight_Level_II,Obesity_Type_I,Obesity_Type_II,Obesity_Type_III}

以上所有欄位，除了 NObeyesdad 為應變數，其餘均為自變數。其中 Height(m) 與 Weight(kg) 用來計算 BMI 指數，其公式如下：

$$Body\ Mass\ Index = \frac{Weight}{Height^2}$$  <!-- 也就是 BMI = Weight/(Height**2) -->

根據[世界衛生組織（ WHO ）的資料][WHO]，BMI 評價標準如下：

| BMI       | 評價                | 評價（中文翻譯）|
|:---------:|---------------------|-----------------|
| < 18.5    | Insufficient_Weight | 過輕            |
| 18.5-24.9 | Normal_Weight       | 正常            |
| 25.0-29.9 | Overweight          | 過重            |
| 30.0-34.9 | Obesity_Type_I      | 肥胖級別一      |
| 35.0-39.9 | Obesity_Type_II     | 肥胖級別二      |
| > 40      | Obesity_Type_III    | 肥胖級別三      |

也就是 NObeyesdad 的資料內容。


# 原始問卷（翻譯）

本資料集的資料收集方式是網路問卷，其內容翻譯如下：

| 問題                                                | 選項                                 |
|-----------------------------------------------------|--------------------------------------|
| 性別                                                | 男/女                                |
| 年齡                                                | 數值                                 |
| 身高                                                | 單位為公尺的數值                     |
| 體重                                                | 單位為公斤的數值                     |
| 曾有家人有過重的困擾                                | 是/否                                |
| 經常食用高熱量食物？                                | 是/否                                |
| 各餐中是否經常攝取蔬菜？                            | 從不/偶爾/總是                       |
| 每日正餐數目                                        | 1 到 2 餐/ 3 餐/ 3 餐以上            |
| 正餐間會吃東西嗎？                                  | 無/偶爾/經常/總是                    |
| 抽煙習慣                                            | 有/無                                |
| 每天喝多少水？                                      | 少於 1 公升/ 1 到 2 公升/多於 2 公升 |
| 有無紀錄吃下的熱量的習慣？                          | 是/否                                |
| 多常運動？                                          | 不運動/1 到 2 天/2 到 4 天/4 到 5 天 |
| 你在手機、電玩、電視、電腦等等科技產品上花多少時間？| 0-2/3-5/>5 小時                      |
| 飲酒頻率                                            | 不喝酒/偶爾/經常/總是                |
| 你的交通方式                                        | 汽車/機車/腳踏車/大眾運輸/步行       |

原始問卷的所有問題都是選擇題——這也是為什麼資料集的前 498 筆資料之中，所有的數值型資料看起來都像是類別型資料。  
舉例來說，FCVC（食用蔬菜頻率）這一欄位在前 498 筆紀錄中均為 1 或 2 或 3 ，分別代表從不、偶爾，與經常。  

第 499 筆紀錄到第 2111 筆紀錄就不再出現這樣的類別型紀錄，是因為原作者們利用了 SMOTE 演算法提高資料的平衡性。


# 不平衡資料

不平衡的資料集會讓機器學習出現偏差。若我們的資料集有絕大部分都是體重正常的紀錄，機器學習出來的成果就會只能準確預測正常體重的人們，甚至是偏好將各種情況都歸類為體重正常。所以我們需要將每個類別的資料量調整到差不多的數目。

當資料出現類別筆數的不平衡，我們有兩種選擇：

1. 提高預測錯誤的代價
2. 從樣本下手，讓每個類別的樣本數趨近一致

以 2. 的方法來說，又有兩種選擇——把較多的資料砍掉，或是把較少的資料補起來——前者的作法相當奢侈，且以本資料集的情形來說，砍掉較多的資料相當於砍掉一半以上的有效資料。不只如此，儘管犧牲了一半以上的有效資料，仍是無法彌補最少的兩類資料（ Obesity_Type_III, Obesity_Type_III ）紀錄稀缺的問題。

所以本資料集原作者們選擇使用 SMOTE 演算法將較為稀缺的資料紀錄筆數補起來，平衡所有應變數類別的紀錄筆數。

SMOTE (Synthetic Minority Over-sampling Technique) 藉由複製稀缺的紀錄（同時加上一些微擾）來盡可能做到不影響該類別特徵的情況下，補足短缺的樣本數。其方法大致如下：

對於每個較稀缺的類別紀錄 C ：

1. 找出 5 個最近鄰 neightbors = Get kNN(5)
2. 令 N 為任意一個在 neightbors 內的紀錄
3. 藉由 C 與 N 特徵之差異加上一點微擾生成人造紀錄 R ，其中 R 的特徵為  
   `R.feats = C.feats + (C.feats - N.feats)*rand(0, 1)`

重複以上動作直到各類別紀錄數目平衡。


# 相關文章

本資料集的發表文章：

- [Obesity Level Estimation Software based on Decision Trees][mainpaper]

本資料集服務的文章，裡面比較了決策樹、邏輯回歸，與單純貝氏三者對「藉由飲食與身體狀況預測肥胖等級」這件事的準確程度，還寫了一個程式：

- [Data Article Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico][datapaper]

類別不平衡問題的描述與解決方案：

- [Class Imbalance Problem][cip]

使用 SMOTE 的手把手教學：

- [SMOTE for Imbalanced Classification with Python][smotepython]

SMOTE 演算法的原始論文：

- [SMOTE: Synthetic Minority Over-sampling Technique][SMOTE]


<!-- references -->
[WHO]: https://www.euro.who.int/en/health-topics/disease-prevention/nutrition/a-healthy-lifestyle/body-mass-index-bmi?source=post_page---------------------------
[source]: https://archive.ics.uci.edu/ml/datasets/Estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition+#
[datapaper]: https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub
[mainpaper]: https://thescipub.com/pdf/jcssp.2019.67.77.pdf
[cip]: http://www.chioka.in/class-imbalance-problem/
[smotepython]: https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/
[SMOTE]: https://arxiv.org/abs/1106.1813
