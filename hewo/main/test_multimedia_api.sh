### MULTIMEDIA TESTS BELOW ###
BASE_URL="http://majora-asus.local:8000"
echo "📺 set_layout → media"
curl -X POST "$BASE_URL/set_layout" \
  -H "Content-Type: application/json" \
  -d '{"name": "media"}'
echo -e "\n"

sleep 1

echo "🎵 add VideoObj1"
curl -X POST $BASE_URL/media/add \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/home/daiego/ThinThoughProjects/HeWo/modules/face/hewo_module_face/hewo/resources/test.mp4",
    "position": [100, 200],
    "velocity": [0, 0],
    "size": [300, 200],
    "loop": false,
    "audio": true,
    "autoplay": false,
    "name": "VideoObj1"
  }'

sleep 1

echo "🎮 move VideoObj1 by (50, 20)"
curl -X POST "$BASE_URL/media/move" \
  -H "Content-Type: application/json" \
  -d '{"name": "VideoObj1", "dx": 50, "dy": 20}'
echo -e "\n"

sleep 1

echo "📍 set VideoObj1 to (100, 100)"
curl -X POST "$BASE_URL/media/set_position" \
  -H "Content-Type: application/json" \
  -d '{"name": "VideoObj1", "x": 100, "y": 100}'
echo -e "\n"

sleep 2

echo "▶️ play VideoObj1"
curl -X POST "$BASE_URL/media/play" \
  -H "Content-Type: application/json" \
  -d '{"name": "VideoObj1"}'
echo -e "\n"

sleep 4

echo "⏸️ pause VideoObj1"
curl -X POST "$BASE_URL/media/pause" \
  -H "Content-Type: application/json" \
  -d '{"name": "VideoObj1"}'
echo -e "\n"

sleep 1

sleep 1

echo "❌ remove VideoObj1"
curl -X POST "$BASE_URL/media/remove" \
  -H "Content-Type: application/json" \
  -d '{"name": "VideoObj1"}'
echo -e "\n"
