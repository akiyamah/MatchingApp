from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    from accounts.models import Hobby, Goal, Area

    if Hobby.objects.exists() or Goal.objects.exists() or Area.objects.exists():
        return

    hobbies = [
        "旅行", 
        "音楽", 
        "映画", 
        "読書", 
        "スポーツ観戦", 
        "スポーツ", 
        "料理", 
        "お酒", 
        "ゲーム", 
        "ペット", 
        "美容", 
        "ファッション", 
        "アート", 
        "カフェ巡り", 
        "ドライブ", 
        "アウトドア", 
        "インドア", 
        'その他',
        ]
    goals = [
        '素敵な人に出会いたい',
        '交際相手を見つけたい', 
        '結婚相手を見つけたい',
        '知り合いを増やしたい',
        '友達づくり',
        '楽しみたい',
        'お酒が好き',
        'その他',
        ]
    areas = [
        '東京都',
        '神奈川県',
        '大阪府',
        '愛知県',
        '埼玉県',
        '千葉県',
        '兵庫県',
        '北海道',
        '福岡県',
        '静岡県',
        '京都府',
        '広島県',
        '宮城県',
        '新潟県',
        '岡山県',
        '熊本県',
        '群馬県',
        '岐阜県',
        '長野県',
        '福島県',
        '青森県',
        '石川県',
        '栃木県',
        '岩手県',
        '山梨県',
        '宮崎県',
        '富山県',
        '香川県',
        '大分県',
        '山形県',
        '奈良県',
        '山口県',
        '高知県',
        '石垣市',
        '和歌山県',
        '佐賀県',
        '鹿児島県',
        '滋賀県',
        '宮崎市',
        '徳島県',
        '秋田県',
        '三重県',
        '福井県',
        '愛媛県',
        '沖縄県',
        ]

    for name in hobbies:
        Hobby.objects.create(name=name)
    
    for name in goals:
        Goal.objects.create(name=name)

    for name in areas:
        Area.objects.create(name=name)




