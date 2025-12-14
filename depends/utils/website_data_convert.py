import sqlite3
import json
from datetime import datetime
from pathlib import Path


def export_db3_to_json(db_path: str, output_path: str = None) -> str:
    """
    将SQLite数据库文件导出为JSON格式
    
    Args:
        db_path: SQLite数据库文件路径
        output_path: 输出JSON文件路径，如果为None则自动生成
    
    Returns:
        输出文件路径
    """
    if not Path(db_path).exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")
    
    # 如果没有指定输出路径，自动生成
    if output_path is None:
        db_name = Path(db_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{db_name}_export_{timestamp}.json"
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
    
    try:
        # 获取所有表名
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # 导出数据
        export_data = {
            "export_info": {
                "source_db": db_path,
                "export_time": datetime.now().isoformat(),
                "total_tables": len(tables)
            },
            "tables": {}
        }
        
        for table_name in tables:
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            # 获取表数据
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            # 转换为字典列表
            table_data = []
            for row in rows:
                row_dict = {}
                for i, column in enumerate(columns_info):
                    column_name = column[1]  # 列名
                    value = row[i]
                    # 处理特殊类型
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='ignore')
                    row_dict[column_name] = value
                table_data.append(row_dict)
            
            # 保存表信息
            export_data["tables"][table_name] = {
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5])
                    }
                    for col in columns_info
                ],
                "row_count": len(table_data),
                "data": table_data
            }
        
        # 写入JSON文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据库导出完成!")
        print(f"源文件: {db_path}")
        print(f"输出文件: {output_path}")
        print(f"导出表数量: {len(tables)}")
        print(f"总记录数: {sum(table_info['row_count'] for table_info in export_data['tables'].values())}")
        
        return output_path
        
    finally:
        conn.close()


def export_db3_simple(db_path: str, output_path: str = None) -> str:
    """
    简化版导出函数，只导出数据不包含表结构信息
    
    Args:
        db_path: SQLite数据库文件路径
        output_path: 输出JSON文件路径
    
    Returns:
        输出文件路径
    """
    if not Path(db_path).exists():
        raise FileNotFoundError(f"数据库文件不存在: {db_path}")
    
    if output_path is None:
        db_name = Path(db_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{db_name}_simple_export_{timestamp}.json"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        export_data = {}
        
        for table_name in tables:
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            table_data = []
            for row in rows:
                row_dict = dict(row)
                # 处理bytes类型数据
                for key, value in row_dict.items():
                    if isinstance(value, bytes):
                        row_dict[key] = value.decode('utf-8', errors='ignore')
                table_data.append(row_dict)
            
            export_data[table_name] = table_data
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"简化导出完成: {output_path}")
        return output_path
        
    finally:
        conn.close()


def convert_onenav_to_websites(onenav_json_path: str, output_path: str = None) -> str:
    """
    将onenav格式的JSON转换为websites格式的JSON
    
    Args:
        onenav_json_path: onenav导出的JSON文件路径
        output_path: 输出文件路径
    
    Returns:
        输出文件路径
    """
    import json
    from datetime import datetime
    
    if not Path(onenav_json_path).exists():
        raise FileNotFoundError(f"文件不存在: {onenav_json_path}")
    
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"websites_converted_{timestamp}.json"
    
    # 读取onenav JSON
    with open(onenav_json_path, 'r', encoding='utf-8') as f:
        onenav_data = json.load(f)
    
    # 转换时间戳函数
    def convert_timestamp(timestamp_str):
        """将onenav的时间戳转换为ISO格式"""
        if not timestamp_str or timestamp_str == "":
            return None
        try:
            # onenav使用Unix时间戳（秒）
            timestamp = int(timestamp_str)
            dt = datetime.fromtimestamp(timestamp)
            return dt.isoformat() + "+08:00"
        except (ValueError, TypeError):
            return None
    
    # 转换分类数据
    converted_categories = []
    for cat in onenav_data.get('on_categorys', []):
        converted_cat = {
            "id": cat.get('id'),
            "name": cat.get('name', ''),
            "description": cat.get('description') if cat.get('description') else "",
            "icon": 'bookmark',
            "sort_order": cat.get('weight', 0),
            "created_at": convert_timestamp(cat.get('add_time'))
        }
        converted_categories.append(converted_cat)
    
    # 转换网站数据
    converted_websites = []
    for site in onenav_data.get('on_links', []):
        converted_site = {
            "id": site.get('id'),
            "name": site.get('title', ''),  # onenav使用title字段
            "url": site.get('url', ''),
            "back_url": site.get('url_standby') if site.get('url_standby') else "",
            "description": site.get('description') if site.get('description') else "",
            "sort_order": site.get('weight', 0),
            "icon": "default.webp",
            "category_id": site.get('fid'),  # onenav使用fid字段
            "created_at": convert_timestamp(site.get('add_time'))
        }
        converted_websites.append(converted_site)
    
    # 构建websites格式的输出
    websites_data = {
        "export_info": {
            "user_id": 1,
            "username": "admin",
            "export_time": datetime.now().isoformat(),
            "version": "1.0"
        },
        "categories": converted_categories,
        "websites": converted_websites
    }
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(websites_data, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成!")
    print(f"源文件: {onenav_json_path}")
    print(f"输出文件: {output_path}")
    print(f"分类数量: {len(converted_categories)}")
    print(f"网站数量: {len(converted_websites)}")
    
    return output_path


if __name__ == "__main__":
    # 示例用法
    db_file = "onenav.db3"
    
    if Path(db_file).exists():
        # 简化导出
        output = export_db3_simple(db_file)
    else:
        print(f"数据库文件 {db_file} 不存在")
    
    #转换onenav JSON格式
    if Path(output).exists():
        convert_onenav_to_websites(output)

