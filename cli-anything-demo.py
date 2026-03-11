#!/usr/bin/env python3
"""
CLI-Anything 概念演示
展示如何将软件变成 Agent 可用的 CLI 工具
"""

import click
import json
from datetime import datetime

@click.group()
@click.option('--json', 'json_output', is_flag=True, help='JSON output for agents')
@click.pass_context
def cli(ctx, json_output):
    """Demo CLI - 示例 CLI 工具"""
    ctx.ensure_object(dict)
    ctx.obj['json_output'] = json_output

@cli.command()
@click.option('--name', '-n', default='project', help='Project name')
@click.option('--width', '-w', default=1920, help='Width in pixels')
@click.option('--height', '-h', default=1080, help='Height in pixels')
@click.option('--output', '-o', default='project.json', help='Output file')
@click.pass_context
def new(ctx, name, width, height, output):
    """Create new project"""
    project = {
        'name': name,
        'width': width,
        'height': height,
        'created': datetime.now().isoformat(),
        'layers': [],
        'modified': False
    }
    
    with open(output, 'w') as f:
        json.dump(project, f, indent=2)
    
    if ctx.obj.get('json_output'):
        click.echo(json.dumps({'status': 'created', 'file': output, 'project': project}))
    else:
        click.echo(f"✓ Created project: {name} ({width}x{height})")
        click.echo(f"  Saved to: {output}")

@cli.command()
@click.option('--project', '-p', required=True, help='Project file')
@click.option('--name', '-n', required=True, help='Layer name')
@click.option('--type', '-t', default='solid', help='Layer type')
@click.pass_context
def add_layer(ctx, project, name, type):
    """Add layer to project"""
    with open(project, 'r') as f:
        data = json.load(f)
    
    layer = {
        'name': name,
        'type': type,
        'visible': True
    }
    data['layers'].append(layer)
    data['modified'] = True
    
    with open(project, 'w') as f:
        json.dump(data, f, indent=2)
    
    if ctx.obj.get('json_output'):
        click.echo(json.dumps({'status': 'layer_added', 'layer': layer, 'total_layers': len(data['layers'])}))
    else:
        click.echo(f"✓ Added layer: {name} ({type})")
        click.echo(f"  Total layers: {len(data['layers'])}")

@cli.command()
@click.option('--project', '-p', required=True, help='Project file')
@click.pass_context
def info(ctx, project):
    """Show project info"""
    with open(project, 'r') as f:
        data = json.load(f)
    
    if ctx.obj.get('json_output'):
        click.echo(json.dumps(data))
    else:
        click.echo(f"Project: {data['name']}")
        click.echo(f"Size: {data['width']}x{data['height']}")
        click.echo(f"Layers: {len(data['layers'])}")
        click.echo(f"Modified: {data['modified']}")

if __name__ == '__main__':
    cli()
