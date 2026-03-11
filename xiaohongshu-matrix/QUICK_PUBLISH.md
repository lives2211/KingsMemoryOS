# 🚀 快速发布指南

## 自动发布方案

### 方案1: 半自动发布（推荐）

**步骤1: 启动Chrome**
```bash
cd xiaohongshu-matrix/xiaohongshu-skills
python3 scripts/chrome_launcher.py
```

**步骤2: 登录账号**
- 在Chrome中访问 https://creator.xiaohongshu.com
- 扫码登录数码虾账号

**步骤3: 自动填充内容**
```bash
cd xiaohongshu-matrix

# 发布数码虾
python3 xiaohongshu-skills/scripts/publish_pipeline.py \
  --title "实测30天，这3个AI工具让我效率提升10倍" \
  --content-file generated/tech-geek/ai_tech_viral_2026.md \
  --preview
```

**步骤4: 手动点击发布**
- 在浏览器中检查内容
- 点击"发布"按钮

**步骤5: 切换账号发布职场虾**
- 退出登录
- 登录职场虾账号
- 重复步骤3-4

---

### 方案2: 全自动发布（需要配置）

**前提条件**:
- Chrome已启动
- 已登录小红书
- Cookie有效

**运行命令**:
```bash
./auto_publish_both.sh
```

---

### 方案3: 手动复制发布（最稳定）

**数码虾内容**:
- **标题**: 实测30天，这3个AI工具让我效率提升10倍
- **正文**: `generated/tech-geek/ai_tech_viral_2026.md`
- **标签**: #AI工具 #效率提升 #ChatGPT #Midjourney #Notion

**职场虾内容**:
- **标题**: 工作3年，AI让我从月薪8k到年薪50万
- **正文**: `generated/career-growth/ai_career_viral_2026.md`
- **标签**: #职场干货 #AI技能 #升职加薪 #2026趋势 #职场逆袭

**步骤**:
1. 打开 https://creator.xiaohongshu.com/publish/publish
2. 登录账号
3. 点击"上传图文"
4. 复制标题和正文
5. 上传图片
6. 添加标签
7. 点击发布

---

## 推荐方案

**立即执行**: 方案3（手动复制发布）
- 最稳定可靠
- 可以检查内容
- 确保发到正确账号

**长期运营**: 方案1（半自动）
- 自动填充内容
- 只需最后点击发布
- 适合批量发布

---

## 现在操作

**请选择方案**:
1. 半自动发布（自动填充，手动点击）
2. 全自动发布（需要配置）
3. 手动复制发布（最稳定）

**推荐**: 方案3，立即手动复制发布！
