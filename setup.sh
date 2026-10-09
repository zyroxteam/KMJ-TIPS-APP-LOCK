#!/data/data/com.termux/files/usr/bin/bash
# ZYROX LOCK BUILDER — One Click Setup | Made By KMJ TIPS CHANNEL
set -e
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'; RED='\033[0;31m'
clear
echo -e "${CYAN}${BOLD}=== ZYROX LOCK BUILDER Setup ===${NC}"
command -v python3 >/dev/null 2>&1 || { echo "python install..."; pkg install -y python >/dev/null 2>&1; }
echo -e "${GREEN}${BOLD}[✓]${NC} python ready"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$SCRIPT_DIR/build.py"
[ -f "$SCRIPT_DIR/template.apk" ] && echo -e "${GREEN}${BOLD}[✓]${NC} template.apk found" || { echo -e "${RED}${BOLD}[!]${NC} template.apk MISSING!"; exit 1; }
echo ""
echo -e "${GREEN}${BOLD}✅ SETUP COMPLETE — chalao: ${CYAN}${BOLD}python3 build.py${NC}"
echo -e "${BOLD}  Made By KMJ TIPS CHANNEL 💛${NC}"
