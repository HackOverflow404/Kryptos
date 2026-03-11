#!/usr/bin/env bash
# CS 124 Honors — Cybersecurity Fundamentals Workshop Poster

clear

G=$'\033[0;32m'
GB=$'\033[1;32m'
C=$'\033[0;36m'
CB=$'\033[1;36m'
Y=$'\033[1;33m'
W=$'\033[1;37m'
DIM=$'\033[2;32m'
DIM2=$'\033[0;90m'
NC=$'\033[0m'
BLD=$'\033[1m'
YLBL=$'\033[0;33m'
TAGY=$'\033[30;43m'

echo -e "${DIM2}root@cs124:~\$${NC} ${W}sudo ./launch_workshop.sh --course=\"CS 124 Honors\"${NC}"
echo ""
echo -e "${GB}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${G}  ██████╗██╗   ██╗██████╗ ███████╗██████╗${NC}"
echo -e "${G} ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗${NC}"
echo -e "${G} ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝${NC}"
echo -e "${G} ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗${NC}"
echo -e "${G} ╚██████╗   ██║   ██████╔╝███████╗██║  ██║${NC}"
echo -e "${G}  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝${NC}"
echo -e "${CB} ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗${NC}"
echo -e "${CB} ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝${NC}"
echo -e "${CB} ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝${NC}"
echo -e "${CB} ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝${NC}"
echo -e "${CB} ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║${NC}"
echo -e "${CB} ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝${NC}"
echo -e "${Y} ███████╗██╗   ██╗███╗   ██╗██████╗  █████╗ ███╗   ███╗███████╗███╗   ██╗████████╗ █████╗ ██╗     ███████╗${NC}"
echo -e "${Y} ██╔════╝██║   ██║████╗  ██║██╔══██╗██╔══██╗████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║     ██╔════╝${NC}"
echo -e "${Y} █████╗  ██║   ██║██╔██╗ ██║██║  ██║███████║██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████║██║     ███████╗${NC}"
echo -e "${Y} ██╔══╝  ██║   ██║██║╚██╗██║██║  ██║██╔══██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║     ╚════██║${NC}"
echo -e "${Y} ██║     ╚██████╔╝██║ ╚████║██████╔╝██║  ██║██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║  ██║███████╗███████║${NC}"
echo -e "${Y} ╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝${NC}"
echo -e "${GB}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${DIM2}root@cs124:~\$${NC} ${W}cat event.conf${NC}"
echo ""
echo -e "${G}┌─ EVENT INFO ───────────────────────────────────────────────────────────────────────────────────┐${NC}"
echo -e "${G}│${NC}  ${DIM}HOST      :${NC}  ${BLD}${W}Medhansh Garg${NC}                                                                    ${G}│${NC}"
echo -e "${G}│${NC}  ${DIM}COURSE    :${NC}  ${C}CS 124 Honors ${NC}                                                                   ${G}│${NC}"
echo -e "${G}│${NC}  ${DIM}DATE      :${NC}  ${Y}Wednesday, March 11th, 2026${NC}                                                      ${G}│${NC}"
echo -e "${G}│${NC}  ${DIM}TIME      :${NC}  ${Y}6:00 PM  --  7:30 PM${NC}                                                             ${G}│${NC}"
echo -e "${G}│${NC}  ${DIM}LOCATION  :${NC}  ${G}Thomas M. Siebel Center for Computer Science, Room 2124${NC}                          ${G}│${NC}"
echo -e "${G}└────────────────────────────────────────────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${DIM2}root@cs124:~\$${NC} ${W}ls ./modules/${NC}"
echo ""
echo -e "${CB}─────────────────────────────────────────────────────────────────────────────────────────────────${NC}"
echo -e "  ${DIM2}01${NC}  ${G}cia_triad.sh         ${NC}  ${W}CIA Triad            ${NC}  ${DIM}Confidentiality · Integrity · Availability${NC}"
echo -e "  ${DIM2}02${NC}  ${G}attack_vectors.sh    ${NC}  ${W}Common Attack Types  ${NC}  ${DIM}phishing, MITM, SQLi, XSS, DoS/DDoS${NC}"
echo -e "  ${DIM2}03${NC}  ${G}network_security.sh  ${NC}  ${W}Network Security     ${NC}  ${DIM}firewalls, VPNs, packet sniffing, IDS${NC}"
echo -e "  ${DIM2}04${NC}  ${G}encryption.sh        ${NC}  ${W}Encryption           ${NC}  ${DIM}AES, RSA, hashing, TLS/SSL${NC}"
echo -e "  ${DIM2}05${NC}  ${G}authentication.sh    ${NC}  ${W}Authentication       ${NC}  ${DIM}MFA, OAuth, JWTs, session tokens${NC}"
echo -e "  ${DIM2}06${NC}  ${G}python_lab.py        ${NC}  ${W}Python Lab           ${NC}  ${YLBL}build your own encrypt/decrypt tool${NC}"
echo -e "${CB}─────────────────────────────────────────────────────────────────────────────────────────────────${NC}"
echo ""
echo ""
echo ""
echo -e "${GB}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -ne "${DIM2}root@cs124:~\$${NC} "
