#!/usr/bin/env python3
"""
小红书自动发布系统 - Web仪表盘
简单HTTP服务器，查看发布状态和统计
"""

import json
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent / "core"))

from content_loader import ContentLoader
from monitor import PublishMonitor
from account_manager import AccountManager


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass
    
    def do_GET(self):
        """处理GET请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            self._serve_dashboard()
        elif path == '/api/stats':
            self._serve_stats()
        elif path == '/api/records':
            self._serve_records()
        elif path == '/api/accounts':
            self._serve_accounts()
        elif path == '/api/content':
            self._serve_content()
        else:
            self._serve_404()
    
    def _serve_dashboard(self):
        """服务主页面"""
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书自动发布系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .stat-card .value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }
        .section {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .section h2 {
            font-size: 20px;
            margin-bottom: 16px;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        th {
            font-weight: 600;
            color: #666;
            font-size: 14px;
        }
        .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        .status-failed {
            background: #f8d7da;
            color: #721c24;
        }
        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .refresh-btn:hover {
            background: #5568d3;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📕 小红书自动发布系统</h1>
            <p>安全 · 智能 · 自动化</p>
        </header>
        
        <div class="stats-grid" id="stats">
            <div class="stat-card">
                <h3>今日发布</h3>
                <div class="value" id="today-count">-</div>
            </div>
            <div class="stat-card">
                <h3>成功率</h3>
                <div class="value" id="success-rate">-</div>
            </div>
            <div class="stat-card">
                <h3>账号数量</h3>
                <div class="value" id="account-count">-</div>
            </div>
            <div class="stat-card">
                <h3>内容库存</h3>
                <div class="value" id="content-count">-</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 最近发布记录</h2>
            <button class="refresh-btn" onclick="loadData()">刷新</button>
            <table id="records-table">
                <thead>
                    <tr>
                        <th>时间</th>
                        <th>标题</th>
                        <th>账号</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>👤 账号状态</h2>
            <table id="accounts-table">
                <thead>
                    <tr>
                        <th>账号</th>
                        <th>别名</th>
                        <th>状态</th>
                        <th>发布数</th>
                        <th>最后使用</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>
    
    <script>
        async function loadData() {
            // 加载统计
            const statsRes = await fetch('/api/stats');
            const stats = await statsRes.json();
            
            document.getElementById('today-count').textContent = stats.today_count || 0;
            document.getElementById('success-rate').textContent = (stats.success_rate || 0) + '%';
            
            // 加载账号
            const accountsRes = await fetch('/api/accounts');
            const accounts = await accountsRes.json();
            
            document.getElementById('account-count').textContent = accounts.length;
            
            const accountsBody = document.querySelector('#accounts-table tbody');
            accountsBody.innerHTML = accounts.map(acc => `
                <tr>
                    <td>${acc.name}</td>
                    <td>${acc.alias}</td>
                    <td><span class="status status-${acc.status}">${acc.status}</span></td>
                    <td>${acc.notes_count}</td>
                    <td>${acc.last_used || '未使用'}</td>
                </tr>
            `).join('');
            
            // 加载记录
            const recordsRes = await fetch('/api/records');
            const records = await recordsRes.json();
            
            const recordsBody = document.querySelector('#records-table tbody');
            if (records.length === 0) {
                recordsBody.innerHTML = '<tr><td colspan="4" class="empty-state">暂无发布记录</td></tr>';
            } else {
                recordsBody.innerHTML = records.map(r => `
                    <tr>
                        <td>${new Date(r.created_at).toLocaleString()}</td>
                        <td>${r.title}</td>
                        <td>${r.account}</td>
                        <td><span class="status status-${r.status}">${r.status}</span></td>
                    </tr>
                `).join('');
            }
            
            // 加载内容库存
            const contentRes = await fetch('/api/content');
            const content = await contentRes.json();
            
            document.getElementById('content-count').textContent = content.total || 0;
        }
        
        // 页面加载时获取数据
        loadData();
        
        // 每30秒自动刷新
        setInterval(loadData, 30000);
    </script>
</body>
</html>'''
        
        self._send_response(200, 'text/html', html.encode('utf-8'))
    
    def _serve_stats(self):
        """服务统计数据"""
        monitor = PublishMonitor()
        stats = monitor.get_stats(days=1)
        
        data = {
            'today_count': stats['total'],
            'success_count': stats['success'],
            'failed_count': stats['failed'],
            'success_rate': stats['success_rate']
        }
        
        self._send_json(data)
    
    def _serve_records(self):
        """服务发布记录"""
        monitor = PublishMonitor()
        records = monitor.get_records(limit=20)
        
        data = [r.to_dict() for r in records]
        self._send_json(data)
    
    def _serve_accounts(self):
        """服务账号列表"""
        manager = AccountManager()
        accounts = manager.list_accounts()
        
        # 如果没有账号，创建默认账号
        if not accounts:
            try:
                manager.add_account("default", "默认账号")
                accounts = manager.list_accounts()
            except:
                pass
        
        data = [acc.to_dict() for acc in accounts]
        self._send_json(data)
    
    def _serve_content(self):
        """服务内容库存"""
        loader = ContentLoader("../xiaohongshu")
        dates = loader.list_available_dates()
        
        total = 0
        for date in dates:
            total += loader.get_notes_count_by_date(date)
        
        data = {
            'dates': dates,
            'total': total
        }
        self._send_json(data)
    
    def _serve_404(self):
        """404页面"""
        self._send_response(404, 'text/plain', b'Not Found')
    
    def _send_response(self, status, content_type, data):
        """发送响应"""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)
    
    def _send_json(self, data):
        """发送JSON响应"""
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self._send_response(200, 'application/json', json_data)


def run_server(port=8088):
    """运行服务器"""
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"🚀 仪表盘已启动: http://localhost:{port}")
    print("按 Ctrl+C 停止")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        server.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书自动发布系统仪表盘")
    parser.add_argument("--port", type=int, default=8088, help="端口号")
    args = parser.parse_args()
    
    run_server(args.port)
