#!/bin/bash

echo "🔧 Configurando o banco de dados MySQL para Hotel Management App"
echo ""

# Verificar se MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL não está instalado."
    echo "📦 Instalando MySQL via Homebrew..."
    brew install mysql
fi

# Iniciar o serviço MySQL
echo "🚀 Iniciando serviço MySQL..."
brew services start mysql

# Aguardar alguns segundos para o serviço iniciar
echo "⏳ Aguardando serviço iniciar..."
sleep 3

# Verificar se está rodando
if brew services list | grep mysql | grep started > /dev/null; then
    echo "✅ MySQL está rodando!"
else
    echo "⚠️  MySQL pode não ter iniciado corretamente. Verifique com: brew services list"
fi

echo ""
echo "📝 Próximos passos:"
echo "1. Configure a senha do root do MySQL:"
echo "   mysql -u root"
echo "   ALTER USER 'root'@'localhost' IDENTIFIED BY 'sua_senha';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""
echo "2. Crie o banco de dados:"
echo "   mysql -u root -p"
echo "   CREATE DATABASE HOTEL_APP;"
echo "   EXIT;"
echo ""
echo "3. Atualize o arquivo backend/.env com sua senha"
echo ""
echo "4. Reinicie o servidor: uvicorn main:app --reload"
