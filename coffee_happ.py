# ☕ Coffee Happ - Auto Recommendation
from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

# Coffee Database
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
        {"name": "库迪冰萃", "price": 10, "tags": ["美式", "清爽"], "caffeine": "高"},
        {"name": "冰美式", "price": 8, "tags": ["美式", "提神"], "caffeine": "高"}
    ]},
    "manner": {"name": "Manner Coffee", "products": [
        {"name": "燕麦拿铁", "price": 25, "tags": ["拿铁", "燕麦", "健康"], "caffeine": "中"},
        {"name": "桂花拿铁", "price": 28, "tags": ["拿铁", "花香"], "caffeine": "中"},
        {"name": "澳白", "price": 25, "tags": ["浓缩", "醇厚"], "caffeine": "高"}
    ]},
    "mstand": {"name": "M Stand", "products": [
        {"name": "燕麦曲奇拿铁", "price": 38, "tags": ["拿铁", "甜品"], "caffeine": "中"},
        {"name": "鲜椰冰咖", "price": 35, "tags": ["特调", "椰子"], "caffeine": "中"}
    ]},
    "percentage": {"name": "百分比咖啡", "products": [
        {"name": "百分比拿铁", "price": 30, "tags": ["拿铁", "精品"], "caffeine": "中"},
        {"name": "澳白", "price": 28, "tags": ["浓缩", "醇厚"], "caffeine": "高"}
    ]},
    "peets": {"name": "皮爷咖啡", "products": [
        {"name": "创始者拿铁", "price": 42, "tags": ["拿铁", "经典"], "caffeine": "中"},
        {"name": "阿拉比卡澳白", "price": 40, "tags": ["浓缩", "精品"], "caffeine": "高"}
    ]},
    "seesaw": {"name": "Seesaw Coffee", "products": [
        {"name": "斑马拿铁", "price": 35, "tags": ["拿铁", "经典"], "caffeine": "中"},
        {"name": "长颈鹿美式", "price": 30, "tags": ["美式", "单品"], "caffeine": "高"}
    ]},
    "nowwa": {"name": "挪瓦咖啡", "products": [
        {"name": "生椰拿铁", "price": 18, "tags": ["拿铁", "椰子"], "caffeine": "中"},
        {"name": "柠檬冰咖", "price": 15, "tags": ["特调", "清爽"], "caffeine": "高"}
    ]},
    "pacific": {"name": "太平洋咖啡", "products": [
        {"name": "经典拿铁", "price": 28, "tags": ["拿铁", "经典"], "caffeine": "中"},
        {"name": "美式咖啡", "price": 25, "tags": ["美式", "醇厚"], "caffeine": "高"}
    ]},
    "xingyika": {"name": "幸运咖", "products": [
        {"name": "幸运咖拿铁", "price": 8, "tags": ["拿铁", "性价比"], "caffeine": "中"},
        {"name": "冰美式", "price": 6, "tags": ["美式", "提神"], "caffeine": "高"}
    ]},
    "7eleven": {"name": "711便利店", "products": [
        {"name": "现萃美式", "price": 12, "tags": ["美式", "便利店"], "caffeine": "高"},
        {"name": "现萃拿铁", "price": 15, "tags": ["拿铁", "便利店"], "caffeine": "中"}
    ]},
    "family": {"name": "全家便利店", "products": [
        {"name": "湃客美式", "price": 12, "tags": ["美式", "便利店"], "caffeine": "高"},
        {"name": "湃客拿铁", "price": 15, "tags": ["拿铁", "便利店"], "caffeine": "中"}
    ]},
    "lawson": {"name": "罗森便利店", "products": [
        {"name": "现萃美式", "price": 11, "tags": ["美式", "便利店"], "caffeine": "高"},
        {"name": "现萃拿铁", "price": 14, "tags": ["拿铁", "便利店"], "caffeine": "中"}
    ]},
    "bianlifeng": {"name": "便利蜂", "products": [
        {"name": "美式咖啡", "price": 10, "tags": ["美式", "便利店"], "caffeine": "高"},
        {"name": "拿铁咖啡", "price": 12, "tags": ["拿铁", "便利店"], "caffeine": "中"}
    ]},
    "greed": {"name": "GREED coffee", "products": [
        {"name": "Dirty", "price": 35, "tags": ["特调", "浓缩"], "caffeine": "高"},
        {"name": "SOE拿铁", "price": 32, "tags": ["拿铁", "单品"], "caffeine": "中"}
    ]},
    "t9": {"name": "T9 Tea", "products": [
        {"name": "茶咖拿铁", "price": 28, "tags": ["茶咖", "融合"], "caffeine": "中"}
    ]}
}

# 用户今日状态 (自动获取)
def get_user_status():
    """根据时间自动判断用户状态"""
    hour = datetime.now().hour
    
    # 基于时间判断时段
    if 6 <= hour < 10:
        time_of_day = "morning"
    elif 10 <= hour < 14:
        time_of_day = "lunch"
    elif 14 <= hour < 18:
        time_of_day = "afternoon"
    elif 18 <= hour < 22:
        time_of_day = "evening"
    else:
        time_of_day = "night"
    
    # 基于任务完成情况判断精力 (模拟)
    # 实际应该从任务系统获取
    completed_tasks = random.randint(3, 8)  # 模拟今日完成3-8个任务
    if completed_tasks >= 6:
        energy = "energetic"  # 充沛
    elif completed_tasks >= 3:
        energy = "normal"  # 一般
    else:
        energy = "tired"  # 疲惫
    
    # 简化天气 (可接入真实API)
    weather = "sunny"
    
    return {
        "time_of_day": time_of_day,
        "energy": energy,
        "weather": weather,
        "completed_tasks": completed_tasks,
        "hour": hour
    }

def recommend(energy="normal", time_of_day="afternoon", weather="sunny"):
    candidates = []
    for brand_id, brand in COFFEE_DB.items():
        for p in brand["products"]:
            score = 0
            # 精力状态
            if energy == "tired" and "提神" in p.get("tags", []):
                score += 5
            if energy == "energetic" and "花香" in p.get("tags", []):
                score += 3
            # 时间
            if time_of_day == "morning" and p.get("caffeine") == "高":
                score += 2
            if time_of_day == "evening" and p.get("caffeine") == "低":
                score += 3
            # 天气
            if weather == "hot" and "冰" in p["name"]:
                score += 3
            if weather == "cold" and "冰" not in p["name"]:
                score += 2
            candidates.append({
                "brand": brand["name"],
                "product": p["name"],
                "price": p["price"],
                "tags": p.get("tags", []),
                "score": score
            })
    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:3]

HTML = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>☕ TIER_Clawd_Coffee</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:#fff;border-radius:24px;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,0.3);max-width:420px;width:100%;text-align:center}
h1{color:#333;margin-bottom:8px;font-size:28px}
.status{color:#888;font-size:14px;margin-bottom:24px}
.status span{background:#f0f0f0;padding:4px 12px;border-radius:20px;margin:0 4px}
.result{background:#f8f9ff;border-radius:16px;padding:20px;margin-top:24px;text-align:left}
.coffee-item{background:#fff;border-radius:12px;padding:16px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
.coffee-item:last-child{margin-bottom:0}
.coffee-name{font-size:18px;font-weight:600;color:#333}
.coffee-brand{color:#888;font-size:13px;margin-top:4px}
.coffee-price{color:#e74c3c;font-size:18px;font-weight:700;float:right}
.tag{display:inline-block;padding:3px 8px;background:#eee;border-radius:12px;font-size:11px;color:#666;margin-right:4px;margin-top:8px}
.btn{width:100%;padding:16px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;margin-top:20px}
.btn:hover{opacity:0.9}
</style></head>
<body>
<div class="card">
<h1>☕ TIER_Clawd_Coffee</h1>
<p class="status" id="status">根据您今日状态自动推荐...</p>
<div class="result" id="result">
<div class="coffee-item" style="text-align:center;color:#888">点击下方按钮获取推荐</div>
</div>
<button class="btn" onclick="getRec()">☕ 立即推荐</button>
</div>
<script>
async function getRec(){
    const btn=document.querySelector('.btn');btn.textContent='推荐中...';btn.disabled=true;
    try{
        const res=await fetch('/api/coffee/auto');
        const json=await res.json();
        document.getElementById('status').innerHTML='<span>'+json.status.energy+'</span><span>'+json.status.time+'</span>已完成'+json.status.tasks+'个任务';
        let html='';
        json.recommendations.forEach((c,i)=>{
            html+=`<div class="coffee-item"><span class="coffee-price">¥${c.price}</span><div class="coffee-name">${c.product}</div><div class="coffee-brand">${c.brand}</div><div class="tags">${c.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div></div>`;
        });
        document.getElementById('result').innerHTML=html;
    }catch(e){document.getElementById('result').innerHTML='<div style="color:red;text-align:center">推荐失败</div>'}
    btn.textContent='☕ 再次推荐';btn.disabled=false;
}
getRec();
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/coffee/auto')
def auto_recommend():
    """自动获取用户状态并推荐"""
    status = get_user_status()
    recommendations = recommend(status["energy"], status["time_of_day"], status["weather"])
    
    # 状态映射
    energy_map = {"energetic": "精力充沛", "normal": "状态一般", "tired": "有点疲惫"}
    time_map = {"morning": "早晨", "lunch": "午间", "afternoon": "下午", "evening": "傍晚", "night": "夜晚"}
    
    return jsonify({
        "status": {
            "energy": energy_map.get(status["energy"], "一般"),
            "time": time_map.get(status["time_of_day"], "现在"),
            "tasks": status["completed_tasks"],
            "hour": status["hour"]
        },
        "recommendations": recommendations
    })

@app.route('/api/coffee/brands')
def brands():
    return jsonify({"total": len(COFFEE_DB)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18801, debug=False)
