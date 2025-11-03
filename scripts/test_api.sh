#!/bin/bash

# Test script for Videogames Chatbot API

BASE_URL="${API_URL:-http://localhost:8000}"
API_BASE="$BASE_URL/api/v1"

echo "🎮 Testing Videogames Chatbot API"
echo "=================================="
echo "Base URL: $BASE_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "Test 1: Health Check"
response=$(curl -s "$API_BASE/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "$response"
fi
echo ""

# Test 2: Search Games
echo "Test 2: Search Games (Elden Ring)"
response=$(curl -s -X POST "$API_BASE/games/search" \
    -H "Content-Type: application/json" \
    -d '{"query":"Elden Ring", "limit":3}')
if echo "$response" | grep -q "Elden Ring"; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool | head -20
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "$response"
fi
echo ""

# Test 3: Get Game Details (Elden Ring app_id: 1245620)
echo "Test 3: Get Game Details (Elden Ring)"
response=$(curl -s -X POST "$API_BASE/games/details" \
    -H "Content-Type: application/json" \
    -d '{"app_id":1245620}')
if echo "$response" | grep -q "Elden Ring"; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool | head -30
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "$response"
fi
echo ""

# Test 4: Chat (simple query)
echo "Test 4: Chat - Simple Query"
response=$(curl -s -X POST "$API_BASE/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"Hola, ¿qué puedes hacer?", "use_tools":false}')
if echo "$response" | grep -q "response"; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "$response"
fi
echo ""

# Test 5: Knowledge Base Stats
echo "Test 5: Knowledge Base Stats"
response=$(curl -s "$API_BASE/knowledge/stats")
if echo "$response" | grep -q "total_documents"; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ FAIL${NC}"
    echo "$response"
fi
echo ""

echo "🎉 API Testing Complete!"
