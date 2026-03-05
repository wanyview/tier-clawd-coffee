# ☕ TIER_Clawd_Coffee v2.1 - 完整咖啡推荐

from flask import Flask, jsonify, render_template_string, request
from datetime import datetime
import random
import json
import requests

app = Flask(__name__)

# 胶囊API地址
CAPSULE_API = "http://127.0.0.1:8005"

# 历史记录文件
HISTORY_FILE = '/tmp/coffee_history.json'

# 咖啡数据库
COFFEE_DB = {
    "luckin": {"name": "瑞幸咖啡", "products": [
        {"name": "生椰拿铁", "price": 18, "tags": ["拿铁", "椰子", "甜"], "caffeine": "中"},
        {"name": "厚乳拿铁", "price": 16, "tags": ["拿铁", "浓郁"], "caffeine": "中"},
        {"name": "陨石拿铁", "price": 20, "tags": ["拿铁", "甜品"], "caffeine": "中"},
        {"name": "冰美式", "price": 12, "tags": ["美式", "提神"], "caffeine": "高"},
        {"name": "生酪拿铁", "price": 22, "tags": ["拿铁", "芝士"], "caffeine": "中"}
    ]},
    "cotti": {"name": "库迪咖啡", "products": [
        {"name": "潘帕斯蓝拿铁", "price": 13, "tags": ["拿铁", "颜值"], "caffeine": "中"},
        {"name": "生椰拿铁", "price": 11, "tags": ["拿铁", "椰子"], "caffeine": "中"},
        {"name": "冰美式", "price": 8, "tags": ["美式", "提神"], "caffeine": "高"}
    ]},
    "manner": {"name": "Manner Coffee", "products": [
        {"name": "燕麦拿铁", "price": 25, "tags": ["拿铁", "燕麦"], "caffeine": "中"},
        {"name": "桂花拿铁", "price": 28, "tags": ["拿铁", "花香"], "caffeine": "中"},
        {"name": "澳白", "price": 25, "tags": ["浓缩", "醇厚"], "caffeine": "高"}
    ]},
    "mstand": {"name": "M Stand", "products": [
        {"name": "燕麦曲奇拿铁", "price": 38, "tags": ["拿铁", "甜品"], "caffeine": "中"},
        {"name": "鲜椰冰咖", "price": 35, "tags": ["特调", "椰子"], "caffeine": "中"}
    ]},
    "peets": {"name": "皮爷咖啡", "products": [
        {"name": "创始者拿铁", "price": 42, "tags": ["拿铁", "经典"], "caffeine": "中"},
        {"name": "阿拉比卡澳白", "price": 40, "tags": ["浓缩", "精品"], "caffeine": "高"}
    ]},
    "xingyika": {"name": "幸运咖", "products": [
        {"name": "幸运咖拿铁", "price": 8, "tags": ["拿铁", "性价比"], "caffeine": "中"},
        {"name": "冰美式", "price": 6, "tags": ["美式", "提神"], "caffeine": "高"}
    ]},
    "7eleven": {"name": "711便利店", "products": [
        {"name": "现萃美式", "price": 12, "tags": ["美式", "便利店"], "caffeine": "高"},
        {"name": "现萃拿铁", "price": 15, "tags": ["拿铁", "便利店"], "caffeine": "中"}
    ]}
}

# 特调配方 (含手冲指南)
SPECIAL_RECIPES = [
    {
        "name": "能量冲刺",
        "desc": "双份浓缩+燕麦奶",
        "method": "1. 取18g咖啡豆研磨成细粉\n2. 双份浓缩萃取30秒\n3. 加入150ml燕麦奶\n4. 搅拌均匀即可",
        "time": "5分钟",
        "difficulty": "⭐⭐",
        "caffeine": "极高",
        "intensity": 5
    },
    {
        "name": "清新早晨",
        "desc": "美式+柠檬+薄荷",
        "method": "1. 杯底放3-4片新鲜柠檬\n2. 加入少量薄荷叶捣出汁\n3. 注入200ml美式咖啡\n4. 加冰块搅拌饮用",
        "time": "3分钟",
        "difficulty": "⭐",
        "caffeine": "中",
        "intensity": 3
    },
    {
        "name": "下午慰劳",
        "desc": "拿铁+焦糖+奶油",
        "method": "1. 杯底加入15ml焦糖糖浆\n2. 萃取单份浓缩\n3. 加入200ml牛奶，奶泡半满\n4. 顶层挤上奶油漩涡\n5. 淋上焦糖酱",
        "time": "8分钟",
        "difficulty": "⭐⭐⭐",
        "caffeine": "中",
        "intensity": 3
    },
    {
        "name": "思考者",
        "desc": "澳白+黄糖",
        "method": "1. 萃取单份浓缩(ristretto)\n2. 准备100ml全脂牛奶，打发至65度\n3. 牛奶融合咖啡至180ml\n4. 撒入黄糖粉\n5. 直接饮用，不要搅拌",
        "time": "5分钟",
        "difficulty": "⭐⭐",
        "caffeine": "高",
        "intensity": 4
    },
    {
        "name": "放松时刻",
        "desc": "卡布奇诺+肉桂",
        "method": "1. 萃取单份浓缩\n2. 准备150ml牛奶，打发至细腻奶泡\n3. 咖啡杯: 咖啡 → 奶泡 → 肉桂粉\n4. 慢慢品味",
        "time": "6分钟",
        "difficulty": "⭐⭐",
        "caffeine": "低",
        "intensity": 2
    },
    {
        "name": "效率冲刺",
        "desc": "冷萃+冰块+柠檬",
        "method": "1. 提前一晚冷萃咖啡(1:10比例)\n2. 杯中加满冰块\n3. 注入冷萃咖啡\n4. 挤入柠檬汁\n5. 快速饮用",
        "time": "2分钟(提前冷萃)",
        "difficulty": "⭐",
        "caffeine": "极高",
        "intensity": 5
    },
    {
        "name": "创意灵感",
        "desc": "香草拿铁+奶油顶",
        "method": "1. 杯底加入10ml香草糖浆\n2. 萃取单份浓缩\n3. 加入180ml牛奶\n4. 顶层挤上奶油\n5. 撒上可可粉",
        "time": "7分钟",
        "difficulty": "⭐⭐",
        "caffeine": "中",
        "intensity": 3
    }
]

def load_history():
    """加载历史记录"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"history": []}

def save_history(data):
    """保存历史记录"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    except:
        pass

def add_to_history(item):
    """添加到历史"""
    data = load_history()
    data["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "item": item,
        "timestamp": datetime.now().isoformat()
    })
    # 只保留最近30天
    if len(data["history"]) > 30:
        data["history"] = data["history"][-30:]
    save_history(data)

def get_recent_history(days=7):
    """获取最近历史"""
    data = load_history()
    recent = []
    for h in data["history"][-days:]:
        recent.append(h["item"])
    return recent

def get_today_work_status():
    """获取今日工作状态"""
    hour = datetime.now().hour
    
    if 6 <= hour < 10:
        time_period, expected = "早晨", 5
    elif 10 <= hour < 14:
        time_period, expected = "上午", 8
    elif 14 <= hour < 18:
        time_period, expected = "下午", 12
    elif 18 <= hour < 22:
        time_period, expected = "傍晚", 15
    else:
        time_period, expected = "夜晚", 18
    
    completed = min(random.randint(5, 15), expected)
    workload_ratio = completed / expected if expected > 0 else 0
    
    if workload_ratio >= 1.0:
        status, mood = "充实圆满", "reward"
    elif workload_ratio >= 0.7:
        status, mood = "高效高产", "focus"
    elif workload_ratio >= 0.4:
        status, mood = "稳步推进", "steady"
    else:
        status, mood = "还在忙", "busy"
    
    return {
        "hour": hour, "time_period": time_period,
        "completed": completed, "expected": expected,
        "workload_ratio": workload_ratio,
        "status": status, "mood": mood,
        "energy": "high" if workload_ratio > 0.6 else "medium" if workload_ratio > 0.3 else "low"
    }

def recommend(status):
    """综合推荐算法"""
    recent = get_recent_history(7)
    
    # 特调推荐
    specials = random.sample(SPECIAL_RECIPES, min(2, len(SPECIAL_RECIPES)))
    
    # 品牌推荐 (避开最近喝过的)
    brand_recs = []
    for brand_id, brand in COFFEE_DB.items():
        for p in brand["products"]:
            name = f"{brand['name']}-{p['name']}"
            if name not in recent:
                score = random.randint(1, 5)
                brand_recs.append({
                    "brand": brand["name"],
                    "product": p["name"],
                    "price": p["price"],
                    "tags": p.get("tags", [])
                })
    
    # 随机选2个品牌推荐
    brand_recs = random.sample(brand_recs, min(2, len(brand_recs))) if brand_recs else []
    
    # 知识胶囊推荐
    capsules = get_capsule_recommend("咖啡")
    
    return {
        "special": specials,
        "brand": brand_recs,
        "recent": recent[-5:] if recent else [],
        "capsules": capsules
    }

HTML = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>☕ TIER_Clawd_Coffee</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;padding:20px}
.card{background:#fff;border-radius:24px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,0.4);max-width:520px;margin:0 auto}
h1{color:#1a1a2e;text-align:center;font-size:28px}
.status{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:16px;border-radius:12px;margin:16px 0}
.status .st{font-size:20px;font-weight:700}
.status .ts{font-size:13px;opacity:0.9;margin-top:4px}
.type-badge{background:#fff;color:#667eea;padding:4px 12px;border-radius:20px;font-size:12px;display:inline-block;margin-top:8px}
.section{margin-top:20px}
.section h2{color:#333;font-size:16px;margin-bottom:12px}
.item{background:#f8f9ff;border-radius:12px;padding:16px;margin-bottom:12px;border-left:4px solid #667eea}
.item .name{font-size:18px;font-weight:600;color:#333}
.item .desc{color:#666;font-size:13px;margin-top:4px}
.item .method{background:#fff;padding:12px;border-radius:8px;margin-top:8px;font-size:12px;color:#555;white-space:pre-line}
.item .meta{font-size:12px;color:#888;margin-top:8px}
.item .price{color:#e74c3c;font-size:18px;font-weight:700;float:right}
.tag{display:inline-block;padding:3px 8px;background:#eee;border-radius:12px;font-size:11px;color:#666;margin-right:4px}
.btn{width:100%;padding:14px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;margin-top:16px}
.btn:hover{opacity:0.9}
.recent{font-size:12px;color:#888;margin-top:12px}
</style></head>
<body>
<div class="card">
<h1>☕ TIER_Clawd_Coffee</h1>
<div class="status" id="status">加载中...</div>
<div id="content"></div>
<button class="btn" onclick="getRec()">☕ 换一批推荐</button>
</div>
<script>
async function getRec(){
    try{
        const res=await fetch('/api/coffee/today');
        const json=await res.json();
        document.getElementById('status').innerHTML='<div class="st">'+json.work_status.status+'</div><div class="ts">'+json.work_status.time_period+' | 已完成 '+json.work_status.completed+'/'+json.work_status.expected+'</div>';
        let html='<div class="section"><h2>☕ 特调配方</h2>';
        json.special.forEach(s=>{
            html+=`<div class="item"><span class="price">${s.intensity}⭐</span><div class="name">${s.name}</div><div class="desc">${s.desc}</div><div class="method">制作方法:\n${s.method}\n⏱️ ${s.time} | 难度 ${s.difficulty}</div></div>`;
        });
        html+='</div><div class="section"><h2>🏪 品牌推荐</h2>';
        json.brand.forEach(b=>{
            html+=`<div class="item"><span class="price">¥${b.price}</span><div class="name">${b.product}</div><div class="desc">${b.brand}</div><div class="tags">${b.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div></div>`;
        });
        if(json.recent && json.recent.length>0){
            html+='</div><div class="recent">最近喝过: '+json.recent.join(', ')+'</div>';
        }
        if(json.capsules && json.capsules.length>0){
            html+='</div><div class="section"><h2>📚 相关知识胶囊</h2>';
            json.capsules.forEach(c=>{
                html+=`<div class="item" style="border-left-color:#9b59b6"><div class="name">📚 ${c.title}</div><div class="desc">${c.domain}</div></div>`;
            });
        }
        document.getElementById('content').innerHTML=html;
    }catch(e){document.getElementById('content').innerHTML='<p style="color:red">加载失败</p>'}
}
getRec();
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/coffee/today')
def today_recommend():
    status = get_today_work_status()
    recs = recommend(status)
    return jsonify({
        "work_status": {
            "status": status["status"],
            "completed": status["completed"],
            "expected": status["expected"],
            "time_period": status["time_period"]
        },
        "special": recs["special"],
        "brand": recs["brand"],
        "recent": recs["recent"],
        "capsules": recs["capsules"]
    })

@app.route('/api/coffee/select', methods=['POST'])
def select_coffee():
    """记录选择的咖啡"""
    data = request.json
    item = data.get('item', '')
    if item:
        add_to_history(item)
        return jsonify({"status": "saved", "item": item})
    return jsonify({"status": "error"})

@app.route('/api/coffee/history')
def get_history():
    """获取历史"""
    return jsonify(load_history())

def get_capsule_recommend(keyword="咖啡"):
    """获取随机知识胶囊推荐"""
    # 预定义的优质知识胶囊库 (含科学内容)
    premium_capsules = [
        {"title": "咖啡因代谢机制", "domain": "科学", "content": "咖啡因在人体内的半衰期约为5-6小时。它通过肝脏CYP1A2酶代谢，代谢产物包括副黄嘌呤、可可碱和茶碱。个体差异会导致代谢速度不同。"},
        {"title": "阿拉比卡 vs 罗布斯塔", "domain": "科学", "content": "阿拉比卡豆占全球产量60%，风味细腻但种植要求高。罗布斯塔占30%，咖啡因含量高2倍，常用于意式浓缩基底。精品咖啡店主要使用阿拉比卡。"},
        {"title": "手冲咖啡最佳水温", "domain": "科教", "content": "手冲咖啡最佳水温为90-96°C。水温过高会导致苦涩，过低则萃取不足。浅烘焙豆建议93-96°C，深烘焙豆建议88-91°C。"},
        {"title": "拿铁艺术拉花技巧", "domain": "科教", "content": "拉花关键：牛奶60-65°C最佳，融合时液面与奶缸保持10cm高度，注入时形成白心，收尾时向前推进完成图案。需要反复练习。"},
        {"title": "咖啡品鉴师标准", "domain": "文化", "content": "SCA认证品鉴师采用100分制评估：香气40分、风味30分、余韵15分、酸质8分、醇厚度7分。80分以上为精品级。"},
        {"title": "全球咖啡产区分布", "domain": "地理", "content": "咖啡带在南北纬25度之间，主要产区：中南美、非洲、亚洲。不同海拔、土壤、气候造就各产区独特风味。"},
        {"title": "咖啡与健康关系", "domain": "医学", "content": "研究表明每天1-3杯咖啡可降低2型糖尿病风险20-30%，降低帕金森病风险25-30%。咖啡中的抗氧化物质有抗炎作用。"},
        {"title": "意式浓缩萃取原理", "domain": "科学", "content": "意式浓缩通过9个大气压、90-93°C热水在25-30秒内萃取30ml液体。萃取不足味道酸涩，过度萃取则苦涩。"},
        {"title": "咖啡豆烘焙曲线", "domain": "技术", "content": "烘焙分三阶段：干燥期、美拉德反应（产生香气）、焦糖化（产生甜味）。一爆后30-60秒为最佳出炉时机。"},
        {"title": "咖啡风味轮使用指南", "domain": "科教", "content": "SCA风味轮从中心到外围分为三级风味：水果/花香→具体品种→处理法风味。品鉴时从中心向外逐层描述。"},
        {"title": "水对咖啡的影响", "domain": "科学", "content": "SCA推荐咖啡用水TDS为150mg/L，pH值7。钙离子提升醇厚度，镁离子增强酸质。纯净水萃取效率低，自来水矿物质过多影响风味。"},
        {"title": "咖啡保鲜存储方法", "domain": "生活", "content": "咖啡最大敌人是氧气、光照、温度和湿度。开袋后应放入密封罐，置于阴凉处，2周内饮用完毕。切勿冷藏。"},
        {"title": "早餐咖啡最佳时间", "domain": "健康", "content": "早餐后9:30-11:00是最佳咖啡时间。此时皮质醇水平开始下降。空腹喝咖啡可能刺激胃酸分泌，建议搭配早餐。"},
        {"title": "咖啡与睡眠质量", "domain": "医学", "content": "咖啡因阻断腺苷受体抑制睡意，但腺苷仍在累积。下午3点后喝咖啡可能影响睡眠质量，导致深度睡眠减少。"},
        {"title": "精品咖啡SCA标准", "domain": "标准", "content": "SCA精品咖啡标准：杯测分数≥80分，无瑕疵豆，烘焙日期14天内，含水量10-12%，颗粒均匀度≥70%。"}
    ]
    return random.sample(premium_capsules, 3)

@app.route('/api/coffee/capsules')
def capsule_recommend():
    """获取咖啡相关胶囊推荐"""
    capsules = get_capsule_recommend("咖啡")
    return jsonify({"capsules": capsules})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18801, debug=False)
