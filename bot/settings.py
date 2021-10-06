from . import secret


LINE_CHANNEL_ACCESS_TOKEN=secret.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=secret.LINE_CHENNEL_SECRET


LABELS = [
        'Gender',
        'Age',
        'family_history_with_overweight',
        'FAVC',
        'FCVC',
        'NCP',
        'CAEC',
        'SMOKE',
        'CH2O',
        'SCC',
        'FAF',
        'TUE',
        'CALC',
        'MTRANS'
        ]
QUESTION_DESC = [
        '請問您的性別？',
        '請問您的年齡？',
        '您曾有家人有過重的困擾?',
        '您是否經常食用高熱量食物？',
        '您各餐中是否經常攝取蔬菜？',
        '您每日的正餐數目？',
        '您正餐間會吃東西嗎？',
        '您是否有抽煙習慣？',
        '您每天喝多少水？',
        '您有無紀錄吃下的熱量的習慣？',
        '您每週運動的頻率？',
        '你每日在手機、電玩、電視、電腦等等科技產品上花多少時間？',
        '您的飲酒頻率？',
        '你慣用的交通方式？'
        ]
CHOICES = [
        ['男性', '女性'],
        [],
        ['是', '否'],
        ['是', '否'],
        ['從不', '偶爾', '總是'],
        ['1 到 2 餐', '3 餐', '3 餐以上'],
        ['從不', '偶爾', '經常', '總是'],
        ['有', '無'],
        ['少於 1 公升', '1 到 2 公升', '多於 2 公升'],
        ['是', '否'],
        ['不運動', '1 到 2 天', '2 到 4 天', ' 4 到 5 天'],
        ['0 到 2 小時', '3 到 5 小時', '5 小時以上'],
        ['從不', '偶爾', '經常', '總是'],
        ['汽車', '機車', '腳踏車', '大眾運輸', '步行']
        ]


class DummyClass:
    def __getitem__(self, index):
        return index


_age_transformer = DummyClass()
CHOICE_TRANSFORMATION_TABLE = [
        {1: 'Male', 2: 'Female'},
        _age_transformer,
        {1: 'yes', 2: 'no'},
        {1: 'yes', 2: 'no'},
        {1: 1, 2: 2, 3: 3},  # preserve to keep index correct
        {1: 1, 2: 3, 3: 4},
        {1: 'no', 2: 'Sometimes', 3: 'Frequently', 4: 'Always'},
        {1: 'yes', 2: 'no'},
        {1: 1, 2: 2, 3: 3},
        {1: 'yes', 2: 'no'},
        {1: 0, 2: 1, 3: 2, 4: 3},
        {1: 0, 2: 1, 3: 2},
        {1: 'no', 2: 'Sometimes', 3: 'Frequently', 4: 'Always'},
        {1: 'Automobile', 2: 'Motorbike', 3: 'Bike', 4: 'Public_Transportation', 5: 'Walking'}
        ]

SUGGETIONS = {
       'Insufficient_Weight': '再這樣生活下去身體會撐不下去的，請多攝取一些營養。',
       'Normal_Weight': '您的生活習慣很健康！請繼續保持。',
       'Overweight_Level_I': '您正在走上變胖的路上，要小心囉！',
       'Overweight_Level_II': '您正在走上變胖的路上，要小心囉！',
       'Obesity_Type_I': '您的生活習慣跟胖子一樣！請盡快改變、邁向健康！',
       'Obesity_Type_II': '您的生活習慣跟胖子一樣！請盡快改變、邁向健康！',
       'Obesity_Type_III': '危險！您的生活習慣會造成不可挽回的後果！請立即做出改變！'
       }
