import urllib.parse
import json
import base64
import requests

def parse_single_vless(vless_url):
    url = vless_url[len("vless://"):]
    user_host, _, rest = url.partition('@')
    host_port, _, query_fragment = rest.partition('?')
    query, _, fragment = query_fragment.partition('#')
    user_id = user_host
    host, _, port = host_port.partition(':')

    params = urllib.parse.parse_qs(query)
    params = {k: v[0] for k, v in params.items()}

    server_name = params.get("sni", "")

    frag_parts = fragment.split('&')
    public_key = None
    short_id = ""
    for part in frag_parts:
        if part.startswith("pbk="):
            public_key = part[4:]
        elif part.startswith("sid="):
            short_id = part[4:]

    config = {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "port": 10808,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {"udp": True}
            }
        ],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": host,
                            "port": int(port),
                            "users": [
                                {
                                    "id": user_id,
                                    "encryption": params.get("encryption", "none"),
                                    "flow": params.get("flow", "")
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": params.get("type", "tcp"),
                    "security": params.get("security", ""),
                    "realitySettings": {
                        "show": False,
                        "fingerprint": params.get("fp", ""),
                        "serverName": server_name,
                        "publicKey": public_key or "",
                        "shortId": short_id
                    }
                }
            }
        ]
    }
    return config

def parse_subscription(sub_url):
    resp = requests.get(sub_url)
    resp.raise_for_status()
    raw = resp.text.strip()

    # Если base64, раскодируем
    try:
        decoded = base64.b64decode(raw).decode('utf-8')
    except Exception:
        decoded = raw

    # Парсим все vless:// ссылки в decoded (по строкам)
    vless_links = [line.strip() for line in decoded.splitlines() if line.startswith('vless://')]
    if not vless_links:
        raise ValueError("В подписке нет vless ссылок")

    # Возьмём первую ссылку для примера (можно изменить логику)
    return parse_single_vless(vless_links[0])

def main():
    import os
    path = 'input.txt'
    with open(path, 'r') as f:
        source = f.read().strip()

    if source.startswith('vless://'):
        config = parse_single_vless(source)
    elif source.startswith('http'):
        config = parse_subscription(source)
    else:
        raise ValueError("Неподдерживаемый формат входных данных")

    config_json = json.dumps(config, indent=4)
    with open('xray_config.json', 'w') as f:
        f.write(config_json)
    print("Конфиг записан в xray_config.json")

if __name__ == "__main__":
    main()

