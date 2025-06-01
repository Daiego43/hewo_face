#!/bin/bash

BASE_URL="http://lattepanda.local:8000"
echo "📺 set_layout → media"
curl -X POST "$BASE_URL/set_layout" \
  -H "Content-Type: application/json" \
  -d '{"name": "hewo"}'
echo -e "\n"

echo "🔁 set_emotion_goal"
curl -X POST "$BASE_URL/face/set_emotion_goal" \
  -H "Content-Type: application/json" \
  -d '{"lps":100,"letl_a":0,"letl_b":0,"letl_c":0,"lebl_a":0,"lebl_b":0,"lebl_c":0,"rps":100,"retl_a":0,"retl_b":0,"retl_c":0,"rebl_a":0,"rebl_b":0,"rebl_c":0,"tl_a":0,"tl_b":0,"tl_c":0,"tl_d":0,"tl_e":0,"bl_a":0,"bl_b":0,"bl_c":0,"bl_d":0,"bl_e":0}'
echo -e "\n"

sleep 1

echo "🔍 get_emotion"
curl -X GET "$BASE_URL/face/get_emotion"
echo -e "\n"

sleep 1

echo "🗣️ toggle_talk"
curl -X POST "$BASE_URL/face/toggle_talk"
echo -e "\n"

sleep 1

echo "🗣️ toggle_talk"
curl -X POST "$BASE_URL/face/toggle_talk"
echo -e "\n"

sleep 1

echo "👁️ trigger_blink"
curl -X POST "$BASE_URL/face/trigger_blink"
echo -e "\n"

sleep 1

echo "🕹️ adjust_position"
curl -X POST "$BASE_URL/face/adjust_position" \
  -H "Content-Type: application/json" \
  -d '{"dx": 15, "dy": -10}'
echo -e "\n"

sleep 1

echo "📐 set_size"
curl -X POST "$BASE_URL/face/set_size" \
  -H "Content-Type: application/json" \
  -d '{"value": 300}'
echo -e "\n"

sleep 1

echo "🎲 set_random_emotion"
curl -X POST "$BASE_URL/face/set_random_emotion"
echo -e "\n"

sleep 1

echo "🔄 reset_emotion"
curl -X POST "$BASE_URL/face/reset_emotion"
echo -e "\n"

sleep 1

echo "🔧 adjust_emotion (lps to 73)"
curl -X POST "$BASE_URL/face/adjust_emotion/lps" \
  -H "Content-Type: application/json" \
  -d '{"value": 73}'
echo -e "\n"

sleep 1

echo "🔧 adjust_emotion (tl_a to 12)"
curl -X POST "$BASE_URL/face/adjust_emotion/tl_a" \
  -H "Content-Type: application/json" \
  -d '{"value": 12}'
echo -e "\n"

sleep 1

echo "🔄 reset_emotion"
curl -X POST "$BASE_URL/face/reset_emotion"
echo -e "\n"

sleep 1