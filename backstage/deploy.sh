#!/bin/bash

# 构建项目
echo "开始构建项目..."
npm run build

# 创建部署目录
echo "创建部署目录..."
sudo mkdir -p /var/www/html/admin

# 复制构建文件到部署目录
echo "复制构建文件..."
sudo cp -r dist/* /var/www/html/admin/

# 复制nginx配置
echo "复制nginx配置..."
sudo cp nginx.conf /etc/nginx/conf.d/admin.conf

# 重启nginx
echo "重启nginx..."
sudo nginx -t && sudo systemctl restart nginx

echo "部署完成！" 