# ☕ TIER_Clawd_Coffee

**大龙虾决定你的品味 | Clawd Decision, Your Taste**

根据每日工作状态，智能推荐专属咖啡

## 功能

- 🤖 自动获取用户状态（时段、精力、任务完成数）
- ☕ 智能推荐咖啡（16品牌、46产品）
- 🎨 精美UI界面

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/your-repo/tier-coffee.git
cd tier-coffee

# 安装依赖
pip install flask

# 启动服务
python3 coffee_happ.py
```

## 访问

- 主页: http://127.0.0.1:18801
- API: http://127.0.0.1:18801/api/coffee/auto

## 咖啡品牌

- 瑞幸、库迪、Manner、M Stand
- 百分比、皮爷、Seesaw、挪瓦
- 太平洋、幸运咖
- 711、全家、罗森、便利蜂
- GREED、T9 Tea

## API

### 自动推荐

```bash
curl http://127.0.0.1:18801/api/coffee/auto
```

### 品牌列表

```bash
curl http://127.0.0.1:18801/api/coffee/brands
```

## 技术栈

- Python Flask
- HTML/CSS/JS

## 作者

👑 曹操

## License

MIT
