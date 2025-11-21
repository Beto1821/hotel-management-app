#!/bin/bash
# Script para limpar cache e reiniciar o frontend

echo "🧹 Limpando cache do Nuxt..."
rm -rf .nuxt .output node_modules/.cache

echo "✅ Cache limpo!"
echo "🚀 Reinicie o servidor com: npm run dev"
