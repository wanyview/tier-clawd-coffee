# ☕ TIER_Coffee v2.0 - 智能工作状态咖啡推荐

from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random
import json

app = Flask(__name__)

# 咖啡数据库
COFFEE_DB = {
    "luckin": {"name": "瑞幸咖啡", "products": [
        {"name": "生椰拿铁", "price": 18, "tags": ["拿铁", "椰子", "甜"], "caffeine": "中", "mood": ["relax"]},
        {"name": "厚乳拿铁", "price": 16, "tags": ["拿铁", "浓郁"], "caffeine": "中", "mood": ["focus"]},
        {"name": "陨石拿铁", "price": 20, "tags": ["拿铁", "甜品"], "caffeine": "中", "mood": ["reward"]},
        {"name": "冰美式", "price": 12, "tags": ["美式", "提神"], "caffeine": "高", "mood": ["busy", "tired"]},
        {"name": "生酪拿铁", "price": 22, "tags": ["拿铁", "芝士"], "caffeine": "中", "mood": ["celebrate"]}
    ]},
    "cotti": {"name": "库迪咖啡", "products": [
        {"name": "潘帕斯蓝拿铁", "price": 13, "tags": ["拿铁", "颜值"], "caffeine": "中", "mood": ["trendy"]},
        {"name": "生椰拿铁", "price": 11, "tags": ["拿铁", "椰子"], "caffeine": "中", "mood": ["relax"]},
        {"name": "库迪冰萃", "price": 10, "tags": ["美式", "清爽"], "caffeine": "高", "mood": ["busy"]},
        {"name": "冰美式", "price": 8, "tags": ["美式", "提神"], "caffeine": "高", "mood": ["tired", "busy"]}
    ]},
    "manner": {"name": "Manner Coffee", "products": [
        {"name": "燕麦拿铁", "price": 25, "tags": ["拿铁", "燕麦", "健康"], "caffeine": "中", "mood": ["healthy"]},
        {"name": "桂花拿铁", "price": 28, "tags": ["拿铁", "花香"], "caffeine": "中", "mood": ["relax", "文艺"]},
        {"name": "澳白", "price": 25, "tags": ["浓缩", "醇厚"], "caffeine": "高", "mood": ["focus", "pro"]}
    ]},
    "mstand": {"name": "M Stand", "products": [
        {"name": "燕麦曲奇拿铁", "price": 38, "tags": ["拿铁", "甜品"], "caffeine": "中", "mood": ["reward", "celebrate"]},
        {"name": "鲜椰冰咖", "price": 35, "tags": ["特调", "椰子"], "caffeine": "中", "mood": ["summer"]}
    ]},
    "percentage": {"name": "百分比咖啡", "products": [
        {"name": "百分比拿铁", "price": 30, "tags": ["拿铁", "精品"], "caffeine": "中", "mood": ["pro"]},
        {"name": "澳白", "price": 28, "tags": ["浓缩", "醇厚"], "caffeine": "高", "mood": ["focus"]}
    ]},
    "peets": {"name": "皮爷咖啡", "products": [
        {"name": "创始者拿铁", "price": 42, "tags": ["拿铁", "经典"], "caffeine": "中", "mood": ["classic"]},
        {"name": "阿拉比卡澳白", "price": 40, "tags": ["浓缩", "精品"], "caffeine": "高", "mood": ["pro"]}
    ]},
    "seesaw": {"name": "Seesaw Coffee", "products": [
        {"name": "斑马拿铁", "price": 35, "tags": ["拿铁", "经典"], "caffeine": "中", "mood": ["trendy"]},
        {"name": "长颈鹿美式", "price": 30, "tags": ["美式", "单品"], "caffeine": "高", "mood": ["focus"]}
    ]},
    "nowwa": {"name": "挪瓦咖啡", "products": [
        {"name": "生椰拿铁", "price": 18, "tags": ["拿铁", "椰子"], "caffeine": "中", "mood": ["relax"]},
        {"name": "柠檬冰咖", "price": 15, "tags": ["特调", "清爽"], "caffeine": "高", "mood": ["summer"]}
    ]},
    "pacific": {"name": "太平洋咖啡", "products": [
        {"name": "经典拿铁", "price": 28, "tags": ["拿铁", "经典"], "caffeine": "中", "mood": ["classic", "business"]},
        {"name": "美式咖啡", "price": 25, "tags": ["美式", "醇厚"], "caffeine": "高", "mood": ["focus"]}
    ]},
    "xingyika": {"name": "幸运咖", "products": [
        {"name": "幸运咖拿铁", "price": 8, "tags": ["拿铁", "性价比"], "caffeine": "中", "mood": ["budget"]},
        {"name": "冰美式", "price": 6, "tags": ["美式", "提神"], "caffeine": "高", "mood": ["tired", "budget"]}
    ]},
    "7eleven": {"name": "711便利店", "products": [
        {"name": "现萃美式", "price": 12, "tags": ["美式", "便利店"], "caffeine": "高", "mood": ["urgent", "24h"]},
        {"name": "现萃拿铁", "price": 15, "tags": ["拿铁", "便利店"], "caffeine": "中", "mood": ["convenient"]}
    ]},
    "family": {"name": "全家便利店", "products": [
        {"name": "湃客美式", "price": 12, "tags": ["美式", "便利店"], "caffeine": "高", "mood": ["urgent"]},
        {"name": "湃客拿铁", "price": 15, "tags": ["拿铁", "便利店"], "caffeine": "中", "mood": ["convenient"]}
    ]},
    "lawson": {"name": "罗森便利店", "products": [
        {"name": "现萃美式", "price": 11, "tags": ["美式", "便利店"], "caffeine": "高", "mood": ["urgent"]},
        {"name": "现萃拿铁", "price": 14, "tags": ["拿铁", "便利店"], "caffeine": "中", "mood": ["convenient"]}
    ]},
    "bianlifeng": {"name": "便利蜂", "products": [
        {"name": "美式咖啡", "price": 10, "tags": ["美式", "便利店"], "caffeine": "高", "mood": ["urgent"]},
        {"name": "拿铁咖啡", "price": 12, "tags": ["拿铁", "便利店"], "caffeine": "中", "mood": ["convenient"]}
    ]},
    "greed": {"name": "GREED coffee", "products": [
        {"name": "Dirty", "price": 35, "tags": ["特调", "浓缩"], "caffeine": "高", "mood": ["pro", "trendy"]},
        {"name": "SOE拿铁", "price": 32, "tags": ["拿铁", "单品"], "caffeine": "中", "mood": ["pro"]}
    ]},
    "t9": {"name": "T9 Tea", "products": [
        {"name": "茶咖拿铁", "price": 28, "tags": ["茶咖", "融合"], "caffeine": "中", "mood": ["fusion", "healthy"]}
    ]}
}

# 特调配方 (自定义咖啡)
SPECIAL_RECIPES = [
    {"name": "能量满满", "desc": "双份浓缩+燕麦奶", "caffeine": "极高", "mood": ["tired", "busy"], "intensity": 5},
    {"name": "清新早晨", "desc": "美式+柠檬+薄荷", "caffeine": "中", "mood": ["morning", "fresh"], "intensity": 3},
    {"name": "下午慰劳", "desc": "拿铁+焦糖+奶油", "caffeine": "中", "mood": ["afternoon", "reward"], "intensity": 3},
    {"name": "思考者", "desc": "澳白+黄糖", "caffeine": "高", "mood": ["focus", "work"], "intensity": 4},
    {"name": "放松时刻", "desc": "卡布奇诺+肉桂", "caffeine": "低", "mood": ["relax", "evening"], "intensity": 2},
    {"name": "效率冲刺", "desc": "冷萃+冰块", "caffeine": "极高", "mood": ["urgent", "deadline"], "intensity": 5},
    {"name": "创意灵感", "desc": "拿铁+香草+奶油", "caffeine": "中", "mood": ["creative"], "intensity": 3},
    {"name": "商务洽谈", "desc": "美式+标准杯", "caffeine": "高", "mood": ["business", "meeting"], "intensity": 4}
]

# 用户今日工作状态 (从任务系统获取)
def get_today_work_status():
    """获取今日工作状态"""
    hour = datetime.now().hour
    
    # 基于时间和模拟任务完成情况判断
    if 6 <= hour < 10:
        time_period = "早晨"
        expected_tasks = 5
    elif 10 <= hour < 14:
        time_period = "上午"
        expected_tasks = 8
    elif 14 <= hour < 18:
        time_period = "下午"
        expected_tasks = 12
    elif 18 <= hour < 22:
        time_period = "傍晚"
        expected_tasks = 15
    else:
        time_period = "夜晚"
        expected_tasks = 18
    
    # 模拟实际完成（实际应该从任务系统读取）
    completed = min(random.randint(5, 15), expected_tasks)
    
    # 计算工作强度
    workload_ratio = completed / expected_tasks if expected_tasks > 0 else 0
    
    # 判断状态
    if workload_ratio >= 1.0:
        status = "充实圆满"  # 任务全完成
        mood = "reward"
        recommendation_type = "special"  # 推荐特调
    elif workload_ratio >= 0.7:
        status = "高效高产"  # 完成大部分
        mood = "focus"
        recommendation_type = "brand"  # 推荐品牌
    elif workload_ratio >= 0.4:
        status = "稳步推进"  # 进行中
        mood = "steady"
        recommendation_type = "brand"
    else:
        status = "还在忙"  # 刚开始
        mood = "busy"
        recommendation_type = "boost"  # 需要提神
    
    # 判断是否需要特调
    if hour >= 17 or workload_ratio >= 0.9:
        recommendation_type = "special"
    
    return {
        "hour": hour,
        "time_period": time_period,
        "completed_tasks": completed,
        "expected_tasks": expected_tasks,
        "workload_ratio": workload_ratio,
        "status": status,
        "mood": mood,
        "recommendation_type": recommendation_type,
        "energy_level": "high" if workload_ratio > 0.6 else "medium" if workload_ratio > 0.3 else "low"
    }

def recommend_coffee(status):
    """根据状态推荐咖啡"""
    candidates = []
    mood = status["mood"]
    recommendation_type = status["recommendation_type"]
    
    # 如果需要特调
    if recommendation_type == "special":
        # 返回特调推荐
        special = random.sample(SPECIAL_RECIPES, min(2, len(SPECIAL_RECIPES)))
        return {
            "type": "special",
            "recommendations": [
                {
                    "name": s["name"],
                    "desc": s["desc"],
                    "caffeine": s["caffeine"],
                    "intensity": s["intensity"],
                    "reason": f"因为您今天{status['status']}，适合来一杯特调"
                } for s in special
            ]
        }
    
    # 品牌推荐
    for brand_id, brand in COFFEE_DB.items():
        for p in brand["products"]:
            score = 0
            # 匹配心情
            if mood in p.get("mood", []):
                score += 5
            # 工作强度匹配
            if status["energy_level"] == "low" and "提神" in p.get("tags", []):
                score += 3
            if status["energy_level"] == "high" and "放松" in str(p.get("tags", [])):
                score += 2
            # 时段匹配
            if status["time_period"] == "早晨" and p.get("caffeine") == "高":
                score += 2
            if status["time_period"] == "夜晚" and p.get("caffeine") == "低":
                score += 3
            
            candidates.append({
                "brand": brand["name"],
                "product": p["name"],
                "price": p["price"],
                "tags": p.get("tags", []),
                "score": score
            })
    
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "type": "brand",
        "recommendations": candidates[:3]
    }

HTML = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>☕ TIER_Coffee</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:#fff;border-radius:24px;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,0.4);max-width:480px;width:100%}
h1{color:#1a1a2e;text-align:center;margin-bottom:8px;font-size:32px}
.subtitle{color:#666;text-align:center;font-size:14px;margin-bottom:24px}
.work-status{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:20px;border-radius:16px;margin-bottom:24px}
.work-status h3{font-size:14px;opacity:0.9;margin-bottom:8px}
.work-status .status{font-size:24px;font-weight:700}
.work-status .tasks{font-size:13px;opacity:0.9;margin-top:8px}
.type-badge{display:inline-block;background:#fff;color:#667eea;padding:4px 12px;border-radius:20px;font-size:12px;margin-top:12px}
.result{background:#f8f9ff;border-radius:16px;padding:20px;margin-top:20px}
.result h2{color:#333;font-size:16px;margin-bottom:16px}
.coffee-item{background:#fff;border-radius:12px;padding:16px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
.coffee-item:last-child{margin-bottom:0}
.coffee-name{font-size:18px;font-weight:600;color:#333}
.coffee-desc{color:#666;font-size:13px;margin-top:4px}
.coffee-reason{color:#667eea;font-size:12px;margin-top:8px;font-style:italic}
.coffee-price{color:#e74c3c;font-size:18px;font-weight:700;float:right}
.tag{display:inline-block;padding:3px 8px;background:#eee;border-radius:12px;font-size:11px;color:#666;margin-right:4px;margin-top:8px}
.special-item{background:linear-gradient(135deg,#f8f9ff,#e8f4f8);border:2px solid #667eea;border-radius:12px;padding:16px;margin-bottom:12px}
.special-item .name{font-size:18px;font-weight:600;color:#667eea}
.special-item .desc{color:#666;font-size:14px;margin-top:4px}
.btn{width:100%;padding:16px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;margin-top:20px}
.btn:hover{opacity:0.9}
</style></head>
<body>
<div class="card">
<h1>☕ TIER_Coffee</h1>
<p class="subtitle">根据今日工作状态智能推荐</p>
<div class="work-status" id="workStatus">
<h3>今日工作状态</h3>
<div class="status" id="status">加载中...</div>
<div class="tasks" id="tasks">--</div>
<div class="type-badge" id="typeBadge">--</div>
</div>
<div class="result" id="result">
<div style="text-align:center;color:#888">点击下方按钮获取推荐</div>
</div>
<button class="btn" onclick="getRec()">☕ 获取今日推荐</button>
</div>
<script>
async function getRec(){
    const btn=document.querySelector('.btn');btn.textContent='推荐中...';btn.disabled=true;
    try{
        const res=await fetch('/api/coffee/today');
        const json=await res.json();
        document.getElementById('status').innerText=json.work_status.status;
        document.getElementById('tasks').innerText='已完成 '+json.work_status.completed+' / 预期 '+json.work_status.expected+' 个任务';
        document.getElementById('typeBadge').innerText=json.recommendation_type==='special'?'☕ 特调推荐':'☕ 品牌推荐';
        let html='<h2>'+(json.recommendation_type==='special'?'今日特调':'今日推荐')+'</h2>';
        json.recommendations.forEach((c,i)=>{
            if(json.recommendation_type==='special'){
                html+=`<div class="special-item"><span class="coffee-price">${c.intensity}⭐</span><div class="name">${c.name}</div><div class="desc">${c.desc}</div><div class="coffee-reason">${c.reason}</div></div>`;
            }else{
                html+=`<div class="coffee-item"><span class="coffee-price">¥${c.price}</span><div class="coffee-name">${c.product}</div><div class="coffee-desc">${c.brand}</div><div class="tags">${c.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div></div>`;
            }
        });
        document.getElementById('result').innerHTML=html;
    }catch(e){document.getElementById('result').innerHTML='<div style="color:red;text-align:center">推荐失败</div>'}
    btn.textContent='☕ 换一种推荐';btn.disabled=false;
}
getRec();
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/coffee/today')
def today_recommend():
    """今日咖啡推荐"""
    status = get_today_work_status()
    recommendation = recommend_coffee(status)
    
    return jsonify({
        "work_status": {
            "status": status["status"],
            "completed": status["completed_tasks"],
            "expected": status["expected_tasks"],
            "time_period": status["time_period"],
            "energy": status["energy_level"]
        },
        "recommendation_type": recommendation["type"],
        "recommendations": recommendation["recommendations"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18801, debug=False)
