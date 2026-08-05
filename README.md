# Hanako 箱庭 (hanako-diorama)

ZLOONG 的个人信息站点。一张每日新闻报纸，慢慢长成了六扇门的小站。

## 页面

| 页面 | 内容 |
|---|---|
| `/` | 门户首页：今日一言 + 本版目录 |
| `/news.html` | 每日新闻速览：报纸风格晨报，每日自动出报 |
| `/career.html` | 求职看板：方向判断、目标公司、技能矩阵、大三时间线 |
| `/library.html` | 知识库：网站推荐、观点笔记、Skill 线索 |
| `/ideas.html` | 灵感碎片墙：角色/世界观/机制，页面可直接添加 |
| `/calendar.html` | 赛事日历：国内 Game Jam 为主，奖金优先 |
| `/benefits.html` | 学生福利：GitHub Pack、云资源、开发工具 |

## 技术

- 纯静态 HTML + CSS，报纸风格（无框架、无构建）
- 灵感碎片 API：Python 标准库（`server.py`），GET/POST/DELETE `/api/ideas`
- 数据：`data/ideas.json`（已 gitignore，不随仓库走）

## 部署

腾讯云轻量服务器，systemd 托管（`hanako-news.service`），端口 8421：

```bash
sudo systemctl restart hanako-news
curl http://127.0.0.1:8421/
```

## 更新机制

- 每日 08:00：自动化抓取新闻，重写 `news.html`（保留 `<style>`，只换内容，期号递增）
- 每周日 10:00：同步知识库页、更新求职看板
- 灵感碎片：用户在页面直接添加，Hanako 也可通过 API 写入

## 目录

```
index.html        门户
news.html         每日新闻
career.html       求职看板
library.html      知识库
ideas.html        灵感碎片墙
calendar.html     赛事日历
benefits.html     学生福利
server.py         HTTP 服务（静态 + /api/ideas）
data/ideas.json   灵感数据（运行时生成，不入库）
```
