# 🚀 OpenClaw 技能使用指南

## 按功能分类

### 🤖 AI 模型 & API
| 技能 | 用途 |
|------|------|
| `llm-models` | 调用 Claude/GPT/Gemini/Kimi 等 100+ LLM |
| `agent-tools` | inference.sh 150+ AI 应用（FLUX/Veo/OmniHuman等）|
| `python-sdk` / `javascript-sdk` | 程序化调用 AI API |
| `ai-rag` | RAG 知识检索 |

### 🖼️ 图像 & 视频生成
| 技能 | 用途 |
|------|------|
| `ai-image-generation` | FLUX/Gemini/Grok 图片生成 |
| `flux-image` | FLUX 专业图片 |
| `nano-banana` / `nano-banana-2` | Gemini 原生图片 |
| `ai-video-generation` | Veo/Seedance/Wan 视频 |
| `google-veo` | Google Veo 视频 |
| `image-to-video` | 图片转视频 |
| `ai-avatar-video` | AI 数字人 |
| `talking-head-production` | 说话头像 |
| `remotion-render` | 代码渲染视频 |

### 🎵 音频 & 语音
| 技能 | 用途 |
|------|------|
| `ai-voice-cloning` | Kokoro/DIA TTS |
| `text-to-speech` | 自然语音合成 |
| `dialogue-audio` | 多角色对话音频 |
| `ai-podcast` | AI 播客制作 |
| `ai-music` | AI 音乐生成 |
| `speech-to-text` | Whisper 语音转文字 |

### 📱 社交媒体 & 营销
| 技能 | 用途 |
|------|------|
| `twitter-automation` | Twitter 自动发推 |
| `twitter-thread-creation` | 推特线程 |
| `ai-social-media-content` | TikTok/Ins/YouTube 内容 |
| `ai-marketing-videos` | 广告视频 |
| `social-media-carousel` | 轮播图设计 |
| `linkedin-content` | LinkedIn 帖子 |

### 📝 内容创作
| 技能 | 用途 |
|------|------|
| `ai-content-pipeline` | 多步骤内容管线 |
| `content-repurposing` | 内容复用（博客→推特等）|
| `brief` | 内容简报 |
| `seo-content-brief` | SEO 内容简报 |
| `technical-blog-writing` | 技术博客 |
| `case-study-writing` | 案例研究 |
| `newsletter-curation` | 新闻通讯 |
| `book-cover-design` | 书籍封面 |
| `logo-design-guide` | Logo 设计 |

### 🎨 设计 & UI
| 技能 | 用途 |
|------|------|
| `landing-page-design` | 落地页设计 |
| `app-store-screenshots` | 应用商店截图 |
| `og-image-design` | 社交分享图 |
| `youtube-thumbnail-design` | YouTube 缩略图 |
| `web-design-guidelines` | UI 设计规范 |
| `vercel-composition-patterns` | React 组件模式 |
| `vercel-react-best-practices` | React/Next.js 最佳实践 |
| `vercel-react-native-skills` | React Native 最佳实践 |
| `sleek-design-mobile-apps` | Sleek App 设计 |

### 🔍 SEO & 数据分析
| 技能 | 用途 |
|------|------|
| `audit` | 网站 SEO 审计 |
| `audit-speed` | 页面速度审计 |
| `diagnose-seo` | 技术 SEO 诊断 |
| `find-keywords` | 关键词研究 |
| `build-clusters` | 主题聚类 |
| `beat-competitors` | 竞品分析 |
| `fix-linking` | 内链优化 |
| `build-links` | 外链建设 |
| `target-serp` | SERP 功能 |
| `rank-local` | 本地 SEO |
| `optimize-for-ai` | AI 搜索优化 |
| `data-visualization` | 数据可视化 |

### 💻 开发工具
| 技能 | 用途 |
|------|------|
| `python-executor` | Python 代码执行 |
| `prompt-engineering` | 提示词工程 |
| `autonomous-agents` | 自主 Agent 设计 |
| `autonomous-agent-patterns` | Agent 设计模式 |
| `memory-systems` | 记忆系统设计 |
| `workflow-automation` | 工作流自动化 |

### 🌐 浏览器 & 自动化
| 技能 | 用途 |
|------|------|
| `agent-browser` | 浏览器自动化 |
| `web-search` | 网络搜索 |
| `background-removal` | 背景去除 |
| `image-upscaling` | 图片放大 |

---

## 常用命令速查

```bash
# 列出所有技能
openclaw skills list

# 查看特定技能
openclaw skills list | grep <关键词>

# 搜索技能
npx clawhub search <关键词>
```

---

## 💡 开发项目推荐组合

**短视频制作**: ai-video-generation + ai-voice-cloning + ai-music  
**内容营销**: ai-content-pipeline + twitter-automation + linkedin-content  
**SEO 优化**: audit + find-keywords + build-clusters + beat-competitors  
**产品发布**: app-store-screenshots + landing-page-design + youtube-thumbnail-design  
**技术博客**: technical-blog-writing + data-visualization + prompt-engineering  
**AI 应用开发**: llm-models + python-sdk + autonomous-agents + memory-systems